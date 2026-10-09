-- 接入数据中台前的只读体检(不建表、不写数据,只输出聚合数,不含任何客户字段)
-- 用途:执行 reporting 迁移之前,确认 tracking schema 的字段和数据量撑得起看板口径。
-- 可在 Supabase SQL Editor 里整段执行,也可以用只读连接逐段跑。

-- 1) 函数依赖的列是否都在(缺列会让迁移里的函数创建失败)
with need(table_name, column_name) as (values
  ('tracking_clicks', 'market'), ('tracking_clicks', 'event_time'), ('tracking_clicks', 'short_code'),
  ('tracking_clicks', 'ad_id'), ('tracking_clicks', 'is_test_traffic'),
  ('lead_stage_history', 'market'), ('lead_stage_history', 'contact_id'),
  ('lead_stage_history', 'respond_io_contact_id'), ('lead_stage_history', 'stage'),
  ('lead_stage_history', 'occurred_at'), ('lead_stage_history', 'short_code'),
  ('order_conversion_events', 'market'), ('order_conversion_events', 'event_name'),
  ('order_conversion_events', 'occurred_at'), ('order_conversion_events', 'order_ref'),
  ('order_conversion_events', 'value'), ('order_conversion_events', 'currency'),
  ('order_conversion_events', 'short_code'), ('order_conversion_events', 'product_id')
)
select n.table_name, n.column_name, (c.column_name is not null) as present
from need n
left join information_schema.columns c
  on c.table_schema = 'tracking' and c.table_name = n.table_name and c.column_name = n.column_name
order by present, n.table_name, n.column_name;

-- 2) reporting schema 是否已存在(已存在说明有人建过,迁移前先对一下)
select exists (select 1 from information_schema.schemata where schema_name = 'reporting') as reporting_exists;

-- 3) 近 30 天广告点击:总量、带 ad_id 的比例、测试流量比例、名称字段是否有值
select market,
       count(*)                                              as clicks,
       count(*) filter (where ad_id is not null)             as clicks_with_ad_id,
       count(*) filter (where is_test_traffic)               as test_clicks,
       count(*) filter (where short_code is not null)        as clicks_with_short_code,
       count(*) filter (where campaign_name is not null)     as clicks_with_campaign_name,
       min(event_time)::date as first_day, max(event_time)::date as last_day
from tracking.tracking_clicks
where event_time >= now() - interval '30 days'
group by market order by market;

-- 4) 线索阶段的取值(确认 'SQL' / 'Deal' 拼写)和近 30 天人数
select market, stage,
       count(distinct coalesce(contact_id, 'respondio:' || respond_io_contact_id)) as contacts,
       count(*) filter (where short_code is not null) as events_with_short_code
from tracking.lead_stage_history
where occurred_at >= now() - interval '30 days'
group by market, stage order by market, stage;

-- 5) 近 30 天首次 SQL 的联系人里,能连回带 ad_id 点击的比例(= 广告表能归因的上限)
with first_sql as (
  select market, coalesce(contact_id, 'respondio:' || respond_io_contact_id) as cid, min(occurred_at) as sql_at
  from tracking.lead_stage_history
  where stage = 'SQL'
  group by 1, 2
  having min(occurred_at) >= now() - interval '30 days'
), codes as (
  select distinct h.market, coalesce(h.contact_id, 'respondio:' || h.respond_io_contact_id) as cid, h.short_code
  from tracking.lead_stage_history h
  where h.short_code is not null
)
select f.market,
       count(distinct f.cid) as sql_contacts,
       count(distinct f.cid) filter (where exists (
         select 1 from codes c
         join tracking.tracking_clicks k
           on k.market = c.market and k.short_code = c.short_code
          and k.ad_id is not null and not k.is_test_traffic and k.event_time <= f.sql_at
         where c.market = f.market and c.cid = f.cid)) as sql_attributable_to_ad
from first_sql f
group by f.market order by f.market;

-- 6) 近 30 天订单事件:各市场有没有 purchase、带 short_code 的比例、币种
select market, event_name, currency,
       count(distinct order_ref)                              as orders,
       count(distinct order_ref) filter (where short_code is not null) as orders_with_short_code,
       sum(value)                                             as total_value
from tracking.order_conversion_events
where occurred_at >= now() - interval '30 days'
group by market, event_name, currency order by market, event_name;
