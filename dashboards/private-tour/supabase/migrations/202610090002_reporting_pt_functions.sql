-- Private Tour 看板 · 指标函数
-- 在 202610090001_reporting_inputs.sql 之后执行。
--
-- 看板只调用两个函数(其余内部函数不对外):
--   reporting.pt_ad_performance(market, from, to)     表 1:广告
--   reporting.pt_sales_performance(market, from, to)  表 2:销售
-- 两个函数都是 SECURITY DEFINER:看板用户不直接读 tracking / reporting 的表,
-- 函数入口先查 reporting.dashboard_viewers 白名单 + 市场授权。输出不含任何客户 PII。
--
-- 口径(与 README 一致):
--   日期按市场本地时区切日(id = Asia/Jakarta,其余 = Asia/Singapore),区间两端都含。
--   SQL      = 首次进入 SQL 阶段落在区间内的联系人(去重,一个联系人只算一次)。
--   成交     = 区间内付款的订单(order_conversion_events.event_name = 'purchase',按 order_ref 去重)。
--   归因     = last-touch:事件的 short_code 连回 tracking_clicks,取事件发生前最近一次带 ad_id 的点击。
--   未归因到 PT 广告、但联系人/产品命中 Private Tour 规则的,单独一行,不丢。

begin;
set local lock_timeout = '5s';

-- ---------------------------------------------------------------------------
-- 小工具
-- ---------------------------------------------------------------------------
create or replace function reporting.market_tz(p_market text)
returns text language sql immutable set search_path = pg_catalog, pg_temp as $$
  select case p_market when 'id' then 'Asia/Jakarta' else 'Asia/Singapore' end
$$;

create or replace function reporting.market_currency(p_market text)
returns text language sql immutable set search_path = pg_catalog, pg_temp as $$
  select case p_market when 'sg' then 'SGD' when 'id' then 'IDR' when 'wetrip' then 'USD' end
$$;

create or replace function reporting.assert_viewer(p_market text, p_from date, p_to date)
returns void language plpgsql stable security definer set search_path = pg_catalog, pg_temp as $$
declare
  v_email text := lower(coalesce(auth.jwt() ->> 'email', ''));
begin
  if p_market is null or p_market not in ('sg', 'id', 'wetrip') then
    raise exception 'unknown market' using errcode = '22023';
  end if;
  if p_from is null or p_to is null or p_to < p_from or p_to - p_from > 366 then
    raise exception 'date range must be 1..367 days' using errcode = '22023';
  end if;
  if not exists (
    select 1 from reporting.dashboard_viewers v
    where v.email = v_email and p_market = any (v.markets)
  ) then
    raise exception 'not allowed' using errcode = '42501';
  end if;
end
$$;

-- ---------------------------------------------------------------------------
-- 内部:Private Tour 广告(按命名规则;取最近一次同步的名字)
-- ---------------------------------------------------------------------------
create or replace function reporting._pt_ads(p_market text)
returns table (ad_id text, platform text, campaign_name text, ad_name text)
language sql stable set search_path = pg_catalog, pg_temp as $$
  select distinct on (s.ad_id) s.ad_id, s.platform, s.campaign_name, s.ad_name
  from reporting.ad_spend_daily s
  where s.market = p_market
    and exists (
      select 1 from reporting.pt_rules r
      where r.active
        and ((r.rule_type = 'campaign_name_ilike' and s.campaign_name ilike r.pattern)
          or (r.rule_type = 'ad_name_ilike'       and s.ad_name       ilike r.pattern))
    )
  order by s.ad_id, s.report_date desc
$$;

-- 内部:按 lifecycle / travel_type 命中 Private Tour 的联系人
create or replace function reporting._pt_rule_contacts(p_market text)
returns table (contact_id text)
language sql stable set search_path = pg_catalog, pg_temp as $$
  select f.contact_id
  from reporting.lead_sales_facts f
  where f.market = p_market
    and exists (
      select 1 from reporting.pt_rules r
      where r.active
        and ((r.rule_type = 'lifecycle'   and lower(f.lifecycle)   = lower(r.pattern))
          or (r.rule_type = 'travel_type' and lower(f.travel_type) = lower(r.pattern)))
    )
$$;

-- 内部:联系人 → 最近一次广告点击的 ad_id(不限时间,用于判断联系人是否来自 PT 广告)
create or replace function reporting._contact_ad(p_market text)
returns table (contact_id text, ad_id text)
language sql stable set search_path = pg_catalog, pg_temp as $$
  select distinct on (l.contact_id) l.contact_id, k.ad_id
  from (
    select coalesce(h.contact_id, 'respondio:' || h.respond_io_contact_id) as contact_id, h.short_code
    from tracking.lead_stage_history h
    where h.market = p_market and h.short_code is not null
  ) l
  join tracking.tracking_clicks k
    on k.market = p_market and k.short_code = l.short_code
   and k.ad_id is not null and not k.is_test_traffic
  order by l.contact_id, k.event_time desc
$$;

-- 内部:区间内首次 SQL 的联系人 + last-touch 广告
create or replace function reporting._sql_attributed(p_market text, p_from date, p_to date)
returns table (contact_id text, sql_at timestamptz, ad_id text)
language sql stable set search_path = pg_catalog, pg_temp as $$
  with ev as (
    select coalesce(h.contact_id, 'respondio:' || h.respond_io_contact_id) as contact_id,
           h.stage, h.occurred_at, h.short_code
    from tracking.lead_stage_history h
    where h.market = p_market
  ), first_sql as (
    select e.contact_id, min(e.occurred_at) as sql_at
    from ev e
    where e.stage = 'SQL'
    group by e.contact_id
    having (min(e.occurred_at) at time zone reporting.market_tz(p_market))::date between p_from and p_to
  ), code as (
    -- 优先用 SQL 事件自己的 short_code,否则用此前最近一条带 short_code 的线索事件
    select distinct on (f.contact_id) f.contact_id, e.short_code
    from first_sql f
    join ev e on e.contact_id = f.contact_id and e.short_code is not null and e.occurred_at <= f.sql_at
    order by f.contact_id, (e.stage = 'SQL') desc, e.occurred_at desc
  )
  select f.contact_id, f.sql_at,
         (select k.ad_id
            from tracking.tracking_clicks k
           where k.market = p_market and k.short_code = c.short_code
             and k.ad_id is not null and not k.is_test_traffic
             and k.event_time <= f.sql_at
           order by k.event_time desc
           limit 1)
  from first_sql f
  left join code c on c.contact_id = f.contact_id
$$;

-- 内部:区间内付款订单 + last-touch 广告 + 对应联系人
create or replace function reporting._orders_attributed(p_market text, p_from date, p_to date)
returns table (order_ref text, paid_at timestamptz, value numeric, currency text,
               product_id text, contact_id text, ad_id text)
language sql stable set search_path = pg_catalog, pg_temp as $$
  with o as (
    select distinct on (e.order_ref) e.order_ref, e.occurred_at as paid_at, e.value, e.currency,
           e.product_id, e.short_code
    from tracking.order_conversion_events e
    where e.market = p_market and e.event_name = 'purchase'
      and (e.occurred_at at time zone reporting.market_tz(p_market))::date between p_from and p_to
    order by e.order_ref, e.occurred_at
  )
  select o.order_ref, o.paid_at, o.value, o.currency, o.product_id,
         (select coalesce(h.contact_id, 'respondio:' || h.respond_io_contact_id)
            from tracking.lead_stage_history h
           where h.market = p_market and h.short_code = o.short_code and h.occurred_at <= o.paid_at
           order by (h.stage = 'Deal') desc, (h.stage = 'SQL') desc, h.occurred_at desc
           limit 1),
         (select k.ad_id
            from tracking.tracking_clicks k
           where k.market = p_market and k.short_code = o.short_code
             and k.ad_id is not null and not k.is_test_traffic
             and k.event_time <= o.paid_at
           order by k.event_time desc
           limit 1)
  from o
$$;

-- ---------------------------------------------------------------------------
-- 表 1:Private Tour 广告
--   CPSQL = spend / sql_count;转化率 = orders / sql_count;ROI = revenue / spend
--   (派生指标在前端算,保证合计行与明细行口径一致)
-- ---------------------------------------------------------------------------
create or replace function reporting.pt_ad_performance(p_market text, p_from date, p_to date)
returns table (
  row_type         text,      -- 'ad' | 'unattributed'
  platform         text,
  campaign_name    text,
  ad_id            text,
  ad_name          text,
  spend            numeric,
  spend_currency   text,
  sql_count        bigint,
  orders           bigint,
  revenue          numeric,
  revenue_currency text
)
language plpgsql stable security definer set search_path = pg_catalog, pg_temp as $$
#variable_conflict use_column
begin
  perform reporting.assert_viewer(p_market, p_from, p_to);

  return query
  with pt_ads as (
    select * from reporting._pt_ads(p_market)
  ), spend as (
    select s.ad_id, sum(s.spend) as spend, max(s.currency) as currency
    from reporting.ad_spend_daily s
    where s.market = p_market and s.report_date between p_from and p_to
      and s.ad_id in (select a.ad_id from pt_ads a)
    group by s.ad_id
  ), sqls as (
    select * from reporting._sql_attributed(p_market, p_from, p_to)
  ), ords as (
    select * from reporting._orders_attributed(p_market, p_from, p_to)
  ), pt_contacts as (
    select c.contact_id from reporting._pt_rule_contacts(p_market) c
  ), pt_products as (
    select r.pattern from reporting.pt_rules r where r.active and r.rule_type = 'product_id'
  ), per_ad as (
    select 'ad'::text as row_type, a.platform, a.campaign_name, a.ad_id, a.ad_name,
           coalesce(sp.spend, 0)::numeric as spend,
           coalesce(sp.currency, reporting.market_currency(p_market)) as spend_currency,
           (select count(*) from sqls q where q.ad_id = a.ad_id) as sql_count,
           (select count(*) from ords o where o.ad_id = a.ad_id) as orders,
           (select coalesce(sum(o.value), 0) from ords o where o.ad_id = a.ad_id) as revenue,
           coalesce((select max(o.currency) from ords o where o.ad_id = a.ad_id),
                    reporting.market_currency(p_market)) as revenue_currency
    from pt_ads a
    left join spend sp on sp.ad_id = a.ad_id
  ), unattr_sql as (
    select q.* from sqls q
    where (q.ad_id is null or q.ad_id not in (select a.ad_id from pt_ads a))
      and q.contact_id in (select c.contact_id from pt_contacts c)
  ), unattr_ord as (
    select o.* from ords o
    where (o.ad_id is null or o.ad_id not in (select a.ad_id from pt_ads a))
      and (o.contact_id in (select c.contact_id from pt_contacts c)
        or o.product_id in (select p.pattern from pt_products p))
  )
  select * from per_ad p
  where p.spend > 0 or p.sql_count > 0 or p.orders > 0
  union all
  select 'unattributed'::text, null::text, null::text, null::text, null::text,
         0::numeric, reporting.market_currency(p_market),
         (select count(*) from unattr_sql),
         (select count(*) from unattr_ord),
         (select coalesce(sum(u.value), 0) from unattr_ord u),
         coalesce((select max(u.currency) from unattr_ord u), reporting.market_currency(p_market));
end
$$;

-- ---------------------------------------------------------------------------
-- 表 2:销售
--   Private Tour 联系人 = 命中 lifecycle/travel_type 规则 ∪ 最近一次广告点击是 PT 广告
--   会话 response time = first_agent_reply_at − first_customer_msg_at,
--     人群 = 首条客户消息落在区间内的 PT 联系人;未回复不进平均值,但计入 late_count
--   late_count = 未回复或首次响应 > 30 分钟(与 sales-leads-quality-hub 日报同阈值)
--   转化率 = orders / sql_count(前端算)
-- ---------------------------------------------------------------------------
create or replace function reporting.pt_sales_performance(p_market text, p_from date, p_to date)
returns table (
  sales_key                 text,
  sales_name                text,
  sql_count                 bigint,
  conversations             bigint,
  replied                   bigint,
  avg_first_response_sec    numeric,
  median_first_response_sec numeric,
  late_count                bigint,
  orders                    bigint,
  revenue                   numeric,
  revenue_currency          text
)
language plpgsql stable security definer set search_path = pg_catalog, pg_temp as $$
#variable_conflict use_column
begin
  perform reporting.assert_viewer(p_market, p_from, p_to);

  return query
  with pt_ads as (
    select a.ad_id from reporting._pt_ads(p_market) a
  ), pt as (
    select c.contact_id from reporting._pt_rule_contacts(p_market) c
    union
    select ca.contact_id from reporting._contact_ad(p_market) ca
    where ca.ad_id in (select a.ad_id from pt_ads a)
  ), pt_products as (
    select r.pattern from reporting.pt_rules r where r.active and r.rule_type = 'product_id'
  ), facts as (
    select f.* from reporting.lead_sales_facts f where f.market = p_market
  ), owner_of as (
    select f.contact_id, coalesce(f.sales_key, '__unassigned') as k, f.sales_name
    from facts f
  ), sql_by as (
    select coalesce(ow.k, '__unassigned') as k, count(*) as n
    from reporting._sql_attributed(p_market, p_from, p_to) q
    left join owner_of ow on ow.contact_id = q.contact_id
    where q.contact_id in (select pt.contact_id from pt)
       or q.ad_id in (select a.ad_id from pt_ads a)
    group by 1
  ), resp_by as (
    select coalesce(f.sales_key, '__unassigned') as k,
           count(*) as conversations,
           count(f.first_agent_reply_at) as replied,
           avg(extract(epoch from f.first_agent_reply_at - f.first_customer_msg_at))::numeric as avg_sec,
           (percentile_cont(0.5) within group (
              order by extract(epoch from f.first_agent_reply_at - f.first_customer_msg_at)))::numeric as median_sec,
           count(*) filter (where f.first_agent_reply_at is null
                               or f.first_agent_reply_at - f.first_customer_msg_at > interval '30 minutes') as late
    from facts f
    where f.contact_id in (select pt.contact_id from pt)
      and (f.first_customer_msg_at at time zone reporting.market_tz(p_market))::date between p_from and p_to
    group by 1
  ), ord_by as (
    select coalesce(ow.k, '__unassigned') as k, count(*) as n, coalesce(sum(o.value), 0) as revenue,
           max(o.currency) as currency
    from reporting._orders_attributed(p_market, p_from, p_to) o
    left join owner_of ow on ow.contact_id = o.contact_id
    where o.contact_id in (select pt.contact_id from pt)
       or o.ad_id in (select a.ad_id from pt_ads a)
       or o.product_id in (select p.pattern from pt_products p)
    group by 1
  ), keys as (
    select k from sql_by union select k from resp_by union select k from ord_by
  ), names as (
    select ow.k, max(ow.sales_name) as sales_name from owner_of ow group by ow.k
  )
  select ks.k,
         case when ks.k = '__unassigned' then '(未分配)' else coalesce(nm.sales_name, ks.k) end,
         coalesce(s.n, 0),
         coalesce(r.conversations, 0),
         coalesce(r.replied, 0),
         r.avg_sec,
         r.median_sec,
         coalesce(r.late, 0),
         coalesce(o.n, 0),
         coalesce(o.revenue, 0)::numeric,
         coalesce(o.currency, reporting.market_currency(p_market))
  from keys ks
  left join names   nm on nm.k = ks.k
  left join sql_by  s  on s.k  = ks.k
  left join resp_by r  on r.k  = ks.k
  left join ord_by  o  on o.k  = ks.k;
end
$$;

-- ---------------------------------------------------------------------------
-- 权限:只有两个看板函数对已登录用户开放;函数内部再查白名单
-- ---------------------------------------------------------------------------
revoke all on all functions in schema reporting from public, anon, authenticated;
grant usage on schema reporting to authenticated;
grant execute on function reporting.pt_ad_performance(text, date, date)    to authenticated;
grant execute on function reporting.pt_sales_performance(text, date, date) to authenticated;

-- 看板经 PostgREST 调用:需在 Supabase → API settings → Exposed schemas 加入 `reporting`
notify pgrst, 'reload schema';

commit;
