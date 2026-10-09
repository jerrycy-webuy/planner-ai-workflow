-- Private Tour 看板 · 配置与权限
-- 目标库:数据中台 Supabase(Webuy Data Platform Prod)。由数据中台 DBA review 后执行;
-- 本文件只新增 schema `reporting`,不改 semantic / curated / tracking 任何对象。
--
-- 看板的数全部来自数据中台已有的语义层(与 SEABEAR MCP 同一套口径):
--   curated.meta_ad_daily_metrics                Meta 日 × 广告花费
--   curated.ad_campaigns                         Google 日 × 系列 × 广告组花费
--   semantic.respondio_contact_attribution_fact  联系人 → 广告(campaign / adset / ad)
--   semantic.respondio_auto_sql_contact_fact     AUTO SQL 事件
--   semantic.contact_order_link                  联系人 ↔ 订单(电话匹配)
--   semantic.order_sales_view                    订单真值(团型 pax_type、有效单、币种)
--   semantic.respondio_contact_assignee          联系人 → 当前销售
--   curated.respondio_*_message_hot_30d          近 30 天消息(首响)
-- 所以这里不建输入表,只放 Private Tour 识别规则、看板白名单和只读组。

begin;
set local lock_timeout = '5s';

create schema if not exists reporting;
revoke all on schema reporting from public;

-- ---------------------------------------------------------------------------
-- 1) Private Tour 识别规则
--    ad_name_regex : 广告系列 / 广告组 / 广告名称任一命中即算 PT 广告(Postgres ~* 正则)
--    pax_type      : 订单团型,按市场区分,与 order_sales_view 口径一致:
--                    sg = WebuyTravel PRV(3) + Altitude PRV(6);wetrip = WPRV(5) + WFIT(9);id = PRV(3)
-- ---------------------------------------------------------------------------
create table if not exists reporting.pt_rules (
  id        serial primary key,
  rule_type text    not null check (rule_type in ('ad_name_regex', 'pax_type')),
  market    text    check (market is null or market in ('sg', 'wetrip', 'id')),  -- null = 所有市场
  pattern   text    not null,
  active    boolean not null default true,
  note      text,
  unique nulls not distinct (rule_type, market, pattern)
);

insert into reporting.pt_rules (rule_type, market, pattern, note) values
  ('ad_name_regex', null,     '(private|\mprv\M|\m[s]?pt\M|私家|定制)', 'Private Tour / [Standard PT] / SPT / 品质私家定制'),
  ('pax_type',      'sg',     '3', 'WebuyTravel PRV'),
  ('pax_type',      'sg',     '6', 'Altitude PRV'),
  ('pax_type',      'wetrip', '5', 'WeTrip WPRV'),
  ('pax_type',      'wetrip', '9', 'WeTrip WFIT(WeTrip 统一口径计入 Private Tour)'),
  ('pax_type',      'id',     '3', 'Indonesia PRV')
on conflict do nothing;

-- ---------------------------------------------------------------------------
-- 2) 看板网页访问白名单。销售个人绩效属于内部敏感数据,不按域名放开。
--    markets 控制能看哪个市场(SG / ID / WeTrip 分开授权)。
-- ---------------------------------------------------------------------------
create table if not exists reporting.dashboard_viewers (
  email    text primary key check (email = lower(email)),
  markets  text[] not null default array[]::text[],
  added_at timestamptz not null default now(),
  note     text
);

-- ---------------------------------------------------------------------------
-- 3) 只读组(与 IDN 漏斗看板的 idn_funnel_readonly 同一做法):不能登录、没有密码、
--    读不到任何原始表,只能调下一份迁移里的两个看板函数(全部市场)。
--    用途:BI 工具 / AI 只读体检。DBA 把它授给已有的专用只读登录,见下一份迁移末尾。
-- ---------------------------------------------------------------------------
do $$ begin
  if not exists (select 1 from pg_roles where rolname = 'pt_dashboard_readonly') then
    create role pt_dashboard_readonly nologin nosuperuser nocreatedb nocreaterole nobypassrls;
  end if;
end $$;

alter table reporting.pt_rules          enable row level security;
alter table reporting.dashboard_viewers enable row level security;

-- 看板用户(authenticated)和只读组都不直接读任何表,只能调下一份迁移里的两个函数。
revoke all on all tables in schema reporting from public, anon, authenticated, pt_dashboard_readonly;

commit;
