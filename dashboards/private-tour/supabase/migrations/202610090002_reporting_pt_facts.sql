-- Private Tour 看板 · 小时级物化快照
-- 在 202610090001_reporting_config.sql 之后执行。
--
-- 为什么物化:看板口径要串 归因事实 × AUTO SQL × 联系人订单匹配 × 订单真值 几个大视图,
-- 现场算一次 10–20 秒,超过 PostgREST 给网页请求的超时。和数据中台 V194 联系人匹配快照同一做法:
-- pg_cron 每小时刷新这几张小表,看板函数只在快照上汇总。快照只含 Private Tour 相关的行。
--
-- 快照(全部 with no data 创建,首次由 reporting.refresh_pt_facts() 填充):
--   reporting.pt_ads_mv        市场 × PT 广告(按 pt_rules 正则)
--   reporting.pt_ad_spend_mv   市场 × PT 广告 × 日 花费
--   reporting.pt_contact_mv    市场 × PT 联系人:lead 日期、PT 广告、首次 AUTO SQL、当前销售
--   reporting.pt_order_mv      市场 × 订单:全部有效 PT 订单 + PT 广告联系人的其他团型订单,各记给一个联系人
--   reporting.pt_response_mv   市场 × 联系人:近 30 天首条客户消息 → 首条销售消息(源表 30 天滚动)
-- 快照里有 contact id(内部 ID,不含姓名 / 电话),只给函数 owner 读,看板用户和只读组都读不到。

begin;
set local lock_timeout = '5s';

-- ---------------------------------------------------------------------------
-- 1) PT 广告
-- ---------------------------------------------------------------------------
create materialized view if not exists reporting.pt_ads_mv as
with markets(m) as (values ('sg'), ('wetrip'), ('id')),
rx as (
  select mk.m, coalesce(string_agg('(' || r.pattern || ')', '|'), '$^') as re
  from markets mk
  left join reporting.pt_rules r
    on r.active and r.rule_type = 'ad_name_regex' and (r.market is null or r.market = mk.m)
  group by mk.m
), acct as (
  select distinct account_id, account_region from curated.meta_ad_dimension
  union
  select distinct account_id, account_region from curated.ad_campaigns
), ads as (
  select 'meta' as platform, d.ad_id, d.campaign_name, d.adset_name, d.ad_name, d.account_id, d.date as seen
  from curated.meta_ad_daily_metrics d
  union all
  select 'meta', a.ad_id, a.campaign_name, a.adset_name, a.ad_name, a.account_id, a.last_seen_at::date
  from curated.meta_ad_dimension a
  union all
  select 'google_ads', g.group_id, g.campaign_name, g.group_name, g.group_name, g.account_id, g.date
  from curated.ad_campaigns g
  where g.source_system = 'GOOGLE_ADS' and g.group_id is not null
)
select distinct on (acct.account_region, x.ad_id)
       acct.account_region as market, x.platform, x.ad_id, x.campaign_name, x.ad_name
from ads x
join acct on acct.account_id = x.account_id
join rx on rx.m = acct.account_region
where x.ad_id is not null
  and (x.campaign_name ~* rx.re or x.adset_name ~* rx.re or x.ad_name ~* rx.re)
order by acct.account_region, x.ad_id, x.seen desc nulls last
with no data;
create unique index if not exists pt_ads_mv_key on reporting.pt_ads_mv (market, ad_id);

-- ---------------------------------------------------------------------------
-- 2) PT 广告日花费(账户原币)
-- ---------------------------------------------------------------------------
create materialized view if not exists reporting.pt_ad_spend_mv as
select a.market, s.ad_id, s.date, sum(s.spend) as spend, max(s.currency) as currency
from (
  select d.ad_id, d.date, d.spend, d.currency from curated.meta_ad_daily_metrics d
  union all
  select g.group_id, g.date, g.cost, g.currency from curated.ad_campaigns g
  where g.source_system = 'GOOGLE_ADS' and g.group_id is not null
) s
join reporting.pt_ads_mv a on a.ad_id = s.ad_id
group by a.market, s.ad_id, s.date
with no data;
create unique index if not exists pt_ad_spend_mv_key on reporting.pt_ad_spend_mv (market, ad_id, date);

-- ---------------------------------------------------------------------------
-- 3) PT 联系人 = 硬归因到 PT 广告 ∪ 高置信链到 PT 订单
-- ---------------------------------------------------------------------------
create materialized view if not exists reporting.pt_contact_mv as
with pax as (
  select r.market, r.pattern::int as pax_type
  from reporting.pt_rules r where r.active and r.rule_type = 'pax_type'
), pt_orders as (
  select v.legal_entity, v.order_id,
         case when v.is_wetrip_order then 'wetrip' when v.legal_entity = 'wbt_id' then 'id' else 'sg' end as market,
         v.pax_type
  from semantic.order_sales_view v
  where v.is_effective
), attr as (
  -- 每个 (region, contact) 一行;只取硬归因(confirmed_ad)到 PT 广告的
  select f.region as market, f.respondio_contact_id as cid, a.ad_id, f.lead_date
  from semantic.respondio_contact_attribution_fact f
  join reporting.pt_ads_mv a on a.market = f.region and a.ad_id = f.ad_id
  where f.confirmed_ad
  union all
  select f.region, f.respondio_contact_id, a.ad_id, f.lead_date
  from semantic.respondio_contact_attribution_fact f
  join reporting.pt_ads_mv a on a.market = f.region and a.platform = 'google_ads'
   and f.ad_id is null and f.adset_id = a.ad_id
  where f.confirmed_ad
), contacts as (
  select market, cid from attr
  union
  select l.region, l.respondio_contact_id
  from semantic.contact_order_link l
  join pt_orders o on o.legal_entity = l.order_business_entity and o.order_id = l.order_id and o.market = l.region
  join pax p on (p.market is null or p.market = o.market) and p.pax_type = o.pax_type
  where l.match_confidence >= 0.95
), sql_first as (
  select s.region as market, s.respondio_contact_id as cid, min(s.auto_sql_date) as sql_date
  from semantic.respondio_auto_sql_contact_fact s
  group by 1, 2
), owner as (
  select case ca.account_id when 'sg_webuytravel' then 'sg' when 'id_webuytravel' then 'id' else ca.account_id end as market,
         ca.contact_id as cid, ca.assignee_id, ca.assignee_name
  from semantic.respondio_contact_assignee ca
)
-- lead_date 只对 PT 广告联系人有值(表 1 cohort 只用它们);逐联系人回查归因事实太慢,不补
select c.market, c.cid, a.lead_date, a.ad_id,
       q.sql_date,
       coalesce(ow.assignee_id, '__unassigned') as owner_key, ow.assignee_name as owner_name,
       now() as snapshot_at
from contacts c
left join (select distinct on (market, cid) market, cid, ad_id, lead_date from attr order by market, cid, lead_date) a
  on a.market = c.market and a.cid = c.cid
left join sql_first q on q.market = c.market and q.cid = c.cid
left join owner ow on ow.market = c.market and ow.cid = c.cid
with no data;
create unique index if not exists pt_contact_mv_key on reporting.pt_contact_mv (market, cid);

-- ---------------------------------------------------------------------------
-- 4) 订单:全部有效 PT 订单 + PT 广告联系人的其他团型订单
--    每张订单只记给一个高置信联系人:优先 PT 广告联系人里下单不早于其 lead 的、lead 最晚的那个
-- ---------------------------------------------------------------------------
create materialized view if not exists reporting.pt_order_mv as
with pax as (
  select r.market, r.pattern::int as pax_type
  from reporting.pt_rules r where r.active and r.rule_type = 'pax_type'
), mo as (
  select v.legal_entity, v.order_id, v.booking_date, v.total_amount, v.order_currency, v.pax_type,
         case when v.is_wetrip_order then 'wetrip' when v.legal_entity = 'wbt_id' then 'id' else 'sg' end as market
  from semantic.order_sales_view v
  where v.is_effective
), mo2 as (
  select mo.*, exists (
           select 1 from pax p where (p.market is null or p.market = mo.market) and p.pax_type = mo.pax_type
         ) as is_pt
  from mo
), pt_ad_links as (
  -- PT 广告联系人高置信链到的订单(可能是其他团型)
  select l.order_business_entity as legal_entity, l.order_id
  from semantic.contact_order_link l
  join reporting.pt_contact_mv pc
    on pc.market = l.region and pc.cid = l.respondio_contact_id and pc.ad_id is not null
  where l.match_confidence >= 0.95
), rel as materialized (
  -- 先把范围缩到 PT 订单 + PT 广告联系人的订单,再去挑联系人(全量有效单逐张挑太慢)
  select o.* from mo2 o
  where o.is_pt or (o.legal_entity, o.order_id) in (select legal_entity, order_id from pt_ad_links)
), pick as (
  -- 只在订单所属市场的 Respond 账号里挑联系人
  select distinct on (o.legal_entity, o.order_id)
         o.legal_entity, o.order_id, l.respondio_contact_id as cid
  from rel o
  join semantic.contact_order_link l
    on l.order_business_entity = o.legal_entity and l.order_id = o.order_id and l.region = o.market
  left join reporting.pt_contact_mv f on f.market = l.region and f.cid = l.respondio_contact_id
  where l.match_confidence >= 0.95
  order by o.legal_entity, o.order_id,
           (f.lead_date is not null and l.booking_date >= f.lead_date) desc, f.lead_date desc nulls last
)
select o.market, o.legal_entity, o.order_id, o.booking_date, o.total_amount, o.order_currency, o.is_pt,
       p.cid, pc.ad_id, pc.lead_date,
       now() as snapshot_at
from rel o
left join pick p on p.legal_entity = o.legal_entity and p.order_id = o.order_id
left join reporting.pt_contact_mv pc on pc.market = o.market and pc.cid = p.cid
where o.is_pt or pc.ad_id is not null
with no data;
create unique index if not exists pt_order_mv_key on reporting.pt_order_mv (legal_entity, order_id);

-- ---------------------------------------------------------------------------
-- 5) 首响(近 30 天):客户第一条消息 → 之后第一条销售消息
--    源消息表是 30 天滚动窗口;sender_name 采集侧为空,分不出人工 / 自动回复 / AI。
-- ---------------------------------------------------------------------------
create materialized view if not exists reporting.pt_response_mv as
with msgs as (
  select 'sg' as market, contact_id, sender_role, message_at, date_sgt from curated.respondio_sg_webuytravel_message_hot_30d
  union all
  select 'wetrip', contact_id, sender_role, message_at, date_sgt from curated.respondio_wetrip_message_hot_30d
  union all
  select 'id', contact_id, sender_role, message_at, date_sgt from curated.respondio_id_webuytravel_message_hot_30d
), fc as (
  select market, contact_id as cid, min(message_at) as c_at, min(date_sgt) as c_date
  from msgs where sender_role = 'customer'
  group by 1, 2
), r as (
  select fc.market, fc.cid, fc.c_at, fc.c_date,
         extract(epoch from min(m.message_at) - fc.c_at)::numeric as reply_sec
  from fc
  left join msgs m on m.market = fc.market and m.contact_id = fc.cid
                  and m.sender_role = 'sales-agent' and m.message_at > fc.c_at
  group by fc.market, fc.cid, fc.c_at, fc.c_date
)
select r.market, r.cid, r.c_date, r.reply_sec,
       coalesce(ca.assignee_id, '__unassigned') as owner_key, ca.assignee_name as owner_name,
       now() as snapshot_at
from r
left join semantic.respondio_contact_assignee ca
  on ca.contact_id = r.cid
 and ca.account_id = case r.market when 'sg' then 'sg_webuytravel' when 'id' then 'id_webuytravel' else 'wetrip' end
with no data;
create unique index if not exists pt_response_mv_key on reporting.pt_response_mv (market, cid);

-- ---------------------------------------------------------------------------
-- 刷新:按依赖顺序;首次(未填充)用普通刷新,之后 CONCURRENTLY 不挡读
-- ---------------------------------------------------------------------------
create or replace function reporting.refresh_pt_facts()
returns void language plpgsql security definer set search_path = pg_catalog, pg_temp as $$
declare
  v text;
begin
  foreach v in array array['pt_ads_mv', 'pt_ad_spend_mv', 'pt_contact_mv', 'pt_order_mv', 'pt_response_mv'] loop
    if (select ispopulated from pg_matviews where schemaname = 'reporting' and matviewname = v) then
      execute format('refresh materialized view concurrently reporting.%I', v);
    else
      execute format('refresh materialized view reporting.%I', v);
    end if;
  end loop;
end
$$;

revoke all on all tables in schema reporting from public, anon, authenticated, pt_dashboard_readonly;
revoke all on function reporting.refresh_pt_facts() from public, anon, authenticated, pt_dashboard_readonly;

commit;

-- DBA:执行完先手动填充一次,再挂 pg_cron(每小时第 35 分钟,错开数据中台 :25 的联系人快照):
--   select reporting.refresh_pt_facts();
--   select cron.schedule('reporting-pt-refresh', '35 * * * *', 'select reporting.refresh_pt_facts()');
