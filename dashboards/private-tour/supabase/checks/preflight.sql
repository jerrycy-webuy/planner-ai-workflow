-- 执行迁移前的只读体检(不建表、不写数据,只输出聚合数,不含任何客户字段)
-- 用途:确认快照依赖的数据中台对象和列都在、数据是新鲜的。可在 SQL Editor 整段执行,
-- 也可以经 SEABEAR run_sql 逐段跑(每段都在 15 秒内)。

-- 1) 快照依赖的列是否都在(缺列会让 202610090002 的物化视图创建失败)
with need(obj, column_name) as (values
  ('curated.meta_ad_daily_metrics', 'date'), ('curated.meta_ad_daily_metrics', 'account_id'),
  ('curated.meta_ad_daily_metrics', 'campaign_name'), ('curated.meta_ad_daily_metrics', 'adset_name'),
  ('curated.meta_ad_daily_metrics', 'ad_id'), ('curated.meta_ad_daily_metrics', 'ad_name'),
  ('curated.meta_ad_daily_metrics', 'spend'), ('curated.meta_ad_daily_metrics', 'currency'),
  ('curated.meta_ad_dimension', 'account_region'), ('curated.meta_ad_dimension', 'last_seen_at'),
  ('curated.ad_campaigns', 'source_system'), ('curated.ad_campaigns', 'account_region'),
  ('curated.ad_campaigns', 'group_id'), ('curated.ad_campaigns', 'group_name'), ('curated.ad_campaigns', 'cost'),
  ('semantic.respondio_contact_attribution_fact', 'region'), ('semantic.respondio_contact_attribution_fact', 'respondio_contact_id'),
  ('semantic.respondio_contact_attribution_fact', 'lead_date'), ('semantic.respondio_contact_attribution_fact', 'ad_id'),
  ('semantic.respondio_contact_attribution_fact', 'adset_id'), ('semantic.respondio_contact_attribution_fact', 'confirmed_ad'),
  ('semantic.respondio_auto_sql_contact_fact', 'region'), ('semantic.respondio_auto_sql_contact_fact', 'auto_sql_date'),
  ('semantic.contact_order_link', 'region'), ('semantic.contact_order_link', 'order_business_entity'),
  ('semantic.contact_order_link', 'match_confidence'), ('semantic.contact_order_link', 'booking_date'),
  ('semantic.order_sales_view', 'is_effective'), ('semantic.order_sales_view', 'is_wetrip_order'),
  ('semantic.order_sales_view', 'pax_type'), ('semantic.order_sales_view', 'order_currency'),
  ('semantic.respondio_contact_assignee', 'assignee_id'), ('semantic.respondio_contact_assignee', 'assignee_name'),
  ('curated.respondio_sg_webuytravel_message_hot_30d', 'sender_role'),
  ('curated.respondio_wetrip_message_hot_30d', 'sender_role'),
  ('curated.respondio_id_webuytravel_message_hot_30d', 'sender_role')
)
-- 用 pg_attribute 而不是 information_schema:后者不列物化视图的列(归因事实、联系人订单匹配都是物化视图)
select n.obj, n.column_name,
       exists (select 1 from pg_attribute a
               where a.attrelid = to_regclass(n.obj) and a.attname = n.column_name and not a.attisdropped) as present
from need n
order by present, n.obj, n.column_name;

-- 2) reporting schema 是否已存在(已存在说明有人建过,迁移前先对一下)
select exists (select 1 from information_schema.schemata where schema_name = 'reporting') as reporting_exists;

-- 3) 数据新鲜度(以数据中台水位视图为准)
select object_name, column_group, data_as_of, is_stale
from semantic.data_freshness
where object_name ~* '(respond|attribution|contact_order|order_sales|meta_ad|auto_sql|ad_campaign|message)'
order by object_name;

-- 4) 各市场近 180 天有效 Private Tour 订单(团型口径与 reporting.pt_rules 一致)
select case when is_wetrip_order then 'wetrip' when legal_entity = 'wbt_id' then 'id' else 'sg' end as market,
       pax_type, order_currency, count(*) as orders, round(sum(total_amount)) as amount
from semantic.order_sales_view
where is_effective and booking_date >= current_date - 180
  and ((legal_entity = 'wbt_sg' and not is_wetrip_order and pax_type in (3, 6))
    or (is_wetrip_order and pax_type in (5, 9))
    or (legal_entity = 'wbt_id' and pax_type = 3))
group by 1, 2, 3 order by 1, 2;

-- 5) 近 90 天名字命中 PT 规则、且有花费的 Meta 广告(按账号)
select account_id, max(account_name) as account_name, currency,
       count(distinct ad_id) as pt_ads, round(sum(spend)) as spend
from curated.meta_ad_daily_metrics
where date >= current_date - 90 and spend > 0
  and (campaign_name ~* '(private|\mprv\M|\m[s]?pt\M|私家|定制)'
    or adset_name    ~* '(private|\mprv\M|\m[s]?pt\M|私家|定制)'
    or ad_name       ~* '(private|\mprv\M|\m[s]?pt\M|私家|定制)')
group by account_id, currency order by spend desc;
