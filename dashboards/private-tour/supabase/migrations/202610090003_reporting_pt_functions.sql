-- Private Tour 看板 · 指标函数(在小时快照上汇总,毫秒级)
-- 在 202610090002_reporting_pt_facts.sql 之后执行。
--
-- 对外只有两个函数(SECURITY DEFINER,调用方不直接读任何表 / 快照):
--   reporting.pt_ad_performance(market, from, to)     表 1:Private Tour 广告
--   reporting.pt_sales_performance(market, from, to)  表 2:销售
-- 入口放行两类调用方:
--   ① 数据库只读登录,DBA 授予了 pt_dashboard_readonly 组(BI / AI 只读体检;全部市场)
--   ② 看板网页经 PostgREST 来的已登录用户,按 reporting.dashboard_viewers 白名单 + 市场授权
-- 输出只有聚合数,不含客户姓名 / 电话 / contact id。
--
-- 口径(沿用数据中台 catalog 的业务铁律,详见 README):
--   市场   sg = wbt_sg 非 WeTrip 订单 + Respond sg_webuytravel;wetrip = is_wetrip_order + Respond wetrip;
--          id = wbt_id + Respond id_webuytravel。币种按市场各自展示,不跨币种相加。
--   表 1 用 cohort:区间 = 联系人成为 lead 的日期;SQL / 成交统计这些联系人之后的全部结果
--          (数据中台 ad_business_attribution 的默认口径)。只算 confirmed_ad 的硬归因。
--          "未归因"行 = 区间内下单、但不是从 PT 广告进来的 PT 订单(含链不到 Respond 的门店 / 线下单)。
--   表 2 用 SQL 日期:区间 = 联系人首次 AUTO SQL 的日期;订单 = 这些 SQL 联系人之后下的 PT 订单;
--          销售 = Respond 当前分配人。首响只覆盖近 30 天,且含自动回复。
--          "未链接 Respond"行 = 区间内下单、链不到本市场 Respond 联系人的 PT 订单。

begin;
set local lock_timeout = '5s';

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
  -- ① 只读登录。SECURITY DEFINER 里 current_user 是函数 owner,所以看 session_user;
  --   USAGE = 继承了组权限(DBA 自己因建角色得到的 ADMIN 成员资格不继承,不会命中)。
  --   PostgREST 请求的 session_user 是 authenticator,不会命中这里,走下面的白名单。
  if pg_has_role(session_user, 'pt_dashboard_readonly', 'USAGE') then
    return;
  end if;
  -- ② 看板网页用户
  if not exists (
    select 1 from reporting.dashboard_viewers v
    where v.email = v_email and p_market = any (v.markets)
  ) then
    raise exception 'not allowed' using errcode = '42501';
  end if;
end
$$;

create or replace function reporting.market_currency(p_market text)
returns text language sql immutable set search_path = pg_catalog, pg_temp as $$
  select case p_market when 'sg' then 'SGD' when 'wetrip' then 'USD' when 'id' then 'IDR' end
$$;

-- ---------------------------------------------------------------------------
-- 表 1:Private Tour 广告
-- ---------------------------------------------------------------------------
create or replace function reporting.pt_ad_performance(p_market text, p_from date, p_to date)
returns table (
  row_type         text,      -- 'ad' | 'unattributed'
  platform         text,
  campaign_name    text,
  ad_id            text,
  ad_name          text,
  spend            numeric,   -- 区间内花费(广告账户原币)
  spend_currency   text,
  contacts         bigint,    -- cohort 线索数
  sql_count        bigint,    -- cohort 里后来成为 AUTO SQL 的
  orders           bigint,    -- cohort 里后来下的 PT 订单
  other_orders     bigint,    -- cohort 里后来下的其他团型订单
  revenue          numeric,   -- PT 订单金额(订单原币)
  revenue_currency text,
  snapshot_at      timestamptz
)
language plpgsql stable security definer set search_path = pg_catalog, pg_temp as $$
#variable_conflict use_column
begin
  perform reporting.assert_viewer(p_market, p_from, p_to);

  return query
  with spend as (
    select s.ad_id, sum(s.spend) as spend, max(s.currency) as currency
    from reporting.pt_ad_spend_mv s
    where s.market = p_market and s.date between p_from and p_to
    group by s.ad_id
  ), cohort as (
    select c.cid, c.ad_id, c.lead_date, c.sql_date
    from reporting.pt_contact_mv c
    where c.market = p_market and c.ad_id is not null and c.lead_date between p_from and p_to
  ), ords as (
    select o.order_id, o.total_amount, o.is_pt, c.ad_id
    from reporting.pt_order_mv o
    join cohort c on c.cid = o.cid
    where o.market = p_market and o.booking_date >= c.lead_date
  ), unattr as (
    select o.total_amount
    from reporting.pt_order_mv o
    where o.market = p_market and o.is_pt and o.booking_date between p_from and p_to and o.ad_id is null
  ), snap as (
    select max(c.snapshot_at) as at from reporting.pt_contact_mv c
  ), per_ad as (
    select 'ad'::text as row_type, a.platform, a.campaign_name, a.ad_id, a.ad_name,
           coalesce(sp.spend, 0)::numeric as spend,
           coalesce(sp.currency, case p_market when 'id' then 'IDR' else 'SGD' end) as spend_currency,
           (select count(*) from cohort c where c.ad_id = a.ad_id) as contacts,
           (select count(*) from cohort c where c.ad_id = a.ad_id and c.sql_date >= c.lead_date) as sql_count,
           (select count(*) from ords o where o.ad_id = a.ad_id and o.is_pt) as orders,
           (select count(*) from ords o where o.ad_id = a.ad_id and not o.is_pt) as other_orders,
           (select coalesce(sum(o.total_amount), 0) from ords o where o.ad_id = a.ad_id and o.is_pt)::numeric as revenue,
           reporting.market_currency(p_market) as revenue_currency,
           (select at from snap) as snapshot_at
    from reporting.pt_ads_mv a
    left join spend sp on sp.ad_id = a.ad_id
    where a.market = p_market
  )
  select * from per_ad p
  where p.spend > 0 or p.contacts > 0
  union all
  select 'unattributed', null, null, null, null,
         0::numeric, reporting.market_currency(p_market),
         null::bigint, null::bigint,
         (select count(*) from unattr), null::bigint,
         (select coalesce(sum(u.total_amount), 0) from unattr u)::numeric,
         reporting.market_currency(p_market),
         (select at from snap);
end
$$;

-- ---------------------------------------------------------------------------
-- 表 2:销售
-- ---------------------------------------------------------------------------
create or replace function reporting.pt_sales_performance(p_market text, p_from date, p_to date)
returns table (
  sales_key                 text,      -- Respond assignee_id;'__unassigned' / '__offline'
  sales_name                text,
  sql_count                 bigint,
  conversations             bigint,    -- 首响口径:区间内首次来消息的会话(近 30 天内,不限 PT)
  replied                   bigint,
  avg_first_response_sec    numeric,
  median_first_response_sec numeric,
  late_count                bigint,    -- 未回复或首响 > 30 分钟
  orders                    bigint,
  revenue                   numeric,
  revenue_currency          text,
  snapshot_at               timestamptz
)
language plpgsql stable security definer set search_path = pg_catalog, pg_temp as $$
#variable_conflict use_column
begin
  perform reporting.assert_viewer(p_market, p_from, p_to);

  return query
  with first_sql as (
    select c.cid, c.sql_date, c.owner_key, c.owner_name
    from reporting.pt_contact_mv c
    where c.market = p_market and c.sql_date between p_from and p_to
  ), sql_by as (
    select q.owner_key as k, count(*) as n from first_sql q group by 1
  ), ord_by as (
    select q.owner_key as k, count(*) as n, sum(o.total_amount) as revenue
    from reporting.pt_order_mv o
    join first_sql q on q.cid = o.cid
    where o.market = p_market and o.is_pt and o.booking_date >= q.sql_date
    group by 1
  ), resp_by as (
    select r.owner_key as k,
           count(*) as conversations,
           count(r.reply_sec) as replied,
           avg(r.reply_sec) as avg_sec,
           (percentile_cont(0.5) within group (order by r.reply_sec))::numeric as median_sec,
           count(*) filter (where r.reply_sec is null or r.reply_sec > 1800) as late
    from reporting.pt_response_mv r
    where r.market = p_market and r.c_date between p_from and p_to
    group by 1
  ), names as (
    select x.k, max(x.name) as name from (
      select q.owner_key as k, q.owner_name as name from first_sql q
      union all
      select r.owner_key, r.owner_name from reporting.pt_response_mv r where r.market = p_market
    ) x group by x.k
  ), keys as (
    select k from sql_by union select k from ord_by union select k from resp_by
  ), offline as (
    select count(*) as n, coalesce(sum(o.total_amount), 0) as revenue
    from reporting.pt_order_mv o
    where o.market = p_market and o.is_pt and o.booking_date between p_from and p_to and o.cid is null
  ), snap as (
    select max(c.snapshot_at) as at from reporting.pt_contact_mv c
  )
  select ks.k,
         case when ks.k = '__unassigned' then '(未分配)' else coalesce(nm.name, ks.k) end,
         coalesce(s.n, 0), coalesce(r.conversations, 0), coalesce(r.replied, 0),
         r.avg_sec, r.median_sec, coalesce(r.late, 0),
         coalesce(o.n, 0), coalesce(o.revenue, 0)::numeric,
         reporting.market_currency(p_market), (select at from snap)
  from keys ks
  left join names   nm on nm.k = ks.k
  left join sql_by  s  on s.k  = ks.k
  left join resp_by r  on r.k  = ks.k
  left join ord_by  o  on o.k  = ks.k
  union all
  select '__offline', '未链接 Respond 的 PT 订单',
         null, null, null, null, null, null,
         off.n, off.revenue::numeric, reporting.market_currency(p_market), (select at from snap)
  from offline off
  where off.n > 0;
end
$$;

-- ---------------------------------------------------------------------------
-- 权限:只有两个看板函数对外;函数内部再分辨调用方(见文件头)
-- ---------------------------------------------------------------------------
revoke all on all functions in schema reporting from public, anon, authenticated, pt_dashboard_readonly;
grant usage on schema reporting to authenticated, pt_dashboard_readonly;
grant execute on function reporting.pt_ad_performance(text, date, date)    to authenticated, pt_dashboard_readonly;
grant execute on function reporting.pt_sales_performance(text, date, date) to authenticated, pt_dashboard_readonly;

-- 看板经 PostgREST 调用:需在 Supabase → API settings → Exposed schemas 加入 `reporting`
notify pgrst, 'reload schema';

commit;

-- DBA:把只读组授给已有的专用只读登录(用它的真实名字;脚本不造登录、不放密码):
--   GRANT pt_dashboard_readonly TO "<existing_reader_login>";
--
-- 验证授权(预期 true, true, false, false):
--   select has_schema_privilege('pt_dashboard_readonly', 'reporting', 'USAGE')                                 as schema_usage,
--          has_function_privilege('pt_dashboard_readonly', 'reporting.pt_ad_performance(text,date,date)', 'EXECUTE') as can_read_report,
--          has_table_privilege('pt_dashboard_readonly', 'reporting.pt_contact_mv', 'SELECT')                  as can_read_snapshot,
--          has_table_privilege('pt_dashboard_readonly', 'reporting.dashboard_viewers', 'SELECT')              as can_read_whitelist;
-- 用该只读登录连上后:
--   select * from reporting.pt_ad_performance('wetrip', current_date - 30, current_date - 1);
