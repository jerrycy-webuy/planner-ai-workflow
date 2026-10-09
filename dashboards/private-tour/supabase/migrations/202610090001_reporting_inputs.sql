-- Private Tour 看板 · 输入层
-- 目标库:数据平台 Supabase(与 webuy-tracking-system 同一个 project,已有 schema `tracking`)。
-- 由数据平台 DBA review 后执行;本文件只新增 schema `reporting`,不改 `tracking` 任何对象。
--
-- tracking 里已有、可以直接用的:
--   tracking.tracking_clicks         广告点击(ad_id / campaign_id / short_code / is_test_traffic)
--   tracking.lead_stage_history      线索阶段(WA_Contact / SQL / Deal),short_code 可连回点击
--   tracking.order_conversion_events 已付款订单(purchase,value,currency,short_code)
--
-- tracking 里没有、本文件补的三张输入表:
--   reporting.ad_spend_daily    广告花费(CPSQL / ROI 的分母)
--   reporting.lead_sales_facts  线索归属销售 + 首次响应时间
--   reporting.pt_rules          什么算 Private Tour(规则可在表里改,不用改代码)

begin;
set local lock_timeout = '5s';

create schema if not exists reporting;
revoke all on schema reporting from public;

-- ---------------------------------------------------------------------------
-- 1) 广告花费:日 × 广告
--    写入方:每日同步 Worker(PLAYBOOK 05)
--      Meta     → Marketing API /insights level=ad,fields=spend,impressions,clicks,campaign_name,adset_name,ad_name
--      Google   → Google Ads API ad_group_ad + metrics.cost_micros / 1e6
--    如果数据平台已有广告维表 / 花费表,直接建成同名 view 指过去即可,函数不用改。
-- ---------------------------------------------------------------------------
create table if not exists reporting.ad_spend_daily (
  report_date   date        not null,
  market        text        not null check (market in ('sg', 'id', 'wetrip')),
  platform      text        not null check (platform in ('meta', 'google_ads', 'tiktok', 'other')),
  campaign_id   text,
  campaign_name text,
  adset_id      text,
  adset_name    text,
  ad_id         text        not null,
  ad_name       text,
  spend         numeric(18,2) not null check (spend >= 0),
  currency      text        not null check (currency ~ '^[A-Z]{3}$'),
  impressions   bigint,
  clicks        bigint,
  synced_at     timestamptz not null default now(),
  primary key (market, platform, ad_id, report_date)
);
create index if not exists ad_spend_daily_market_date_idx
  on reporting.ad_spend_daily (market, report_date);

-- ---------------------------------------------------------------------------
-- 2) 线索 × 销售:每个联系人一行
--    写入方:Respond.io 轮询(已有 poller 可顺带写)
--      sales_key / sales_name ← contact.assignee.email → sales-mapping(SkyBear salesId)
--      lifecycle               ← contact.lifecycle(例:'tour private')
--      travel_type             ← 自定义字段 / LLM 抽取('Private Trip' 等)
--      first_customer_msg_at   ← 第一条客户入站消息时间
--      first_agent_reply_at    ← 其后第一条销售出站消息时间(未回复 = null)
--    contact_id 与 tracking.lead_stage_history.contact_id 同一命名空间,例如 'respondio:123456'。
--    不存手机号 / 邮箱 / 姓名。
-- ---------------------------------------------------------------------------
create table if not exists reporting.lead_sales_facts (
  market                 text        not null check (market in ('sg', 'id', 'wetrip')),
  contact_id             text        not null,
  sales_key              text,
  sales_name             text,
  assigned_at            timestamptz,
  lifecycle              text,
  travel_type            text,
  first_customer_msg_at  timestamptz,
  first_agent_reply_at   timestamptz,
  updated_at             timestamptz not null default now(),
  primary key (market, contact_id),
  check (first_agent_reply_at is null or first_customer_msg_at is not null)
);
create index if not exists lead_sales_facts_first_msg_idx
  on reporting.lead_sales_facts (market, first_customer_msg_at);

-- ---------------------------------------------------------------------------
-- 3) Private Tour 识别规则(命中任意一条 active 规则即算)
--    *_ilike 用 Postgres ILIKE 语法(% 通配);其余为不区分大小写的完全匹配。
-- ---------------------------------------------------------------------------
create table if not exists reporting.pt_rules (
  id        serial primary key,
  rule_type text    not null check (rule_type in
              ('campaign_name_ilike', 'ad_name_ilike', 'lifecycle', 'travel_type', 'product_id')),
  pattern   text    not null,
  active    boolean not null default true,
  note      text,
  unique (rule_type, pattern)
);

insert into reporting.pt_rules (rule_type, pattern, note) values
  ('campaign_name_ilike', '%private%',   '广告系列命名含 private'),
  ('ad_name_ilike',       '%private%',   '广告命名含 private'),
  ('lifecycle',           'tour private','Respond.io lifecycle'),
  ('travel_type',         'Private Trip','SkyBear travelType / LLM 抽取值')
on conflict (rule_type, pattern) do nothing;

-- ---------------------------------------------------------------------------
-- 4) 看板访问白名单。销售个人绩效属于内部敏感数据,不按域名放开。
--    markets 控制能看哪个市场(SG / ID 数据分开授权)。
-- ---------------------------------------------------------------------------
create table if not exists reporting.dashboard_viewers (
  email    text primary key check (email = lower(email)),
  markets  text[] not null default array[]::text[],
  added_at timestamptz not null default now(),
  note     text
);

-- ---------------------------------------------------------------------------
-- 5) 只读组(与 IDN 漏斗看板的 idn_funnel_readonly 同一做法):不能登录、没有密码、
--    读不到任何原始表,只能调下一份迁移里的两个看板函数(全部市场)。
--    用途:BI 工具 / AI 只读体检。DBA 把它授给已有的专用只读登录,见下一份迁移末尾。
-- ---------------------------------------------------------------------------
do $$ begin
  if not exists (select 1 from pg_roles where rolname = 'pt_dashboard_readonly') then
    create role pt_dashboard_readonly nologin nosuperuser nocreatedb nocreaterole nobypassrls;
  end if;
end $$;

alter table reporting.ad_spend_daily    enable row level security;
alter table reporting.lead_sales_facts  enable row level security;
alter table reporting.pt_rules          enable row level security;
alter table reporting.dashboard_viewers enable row level security;

-- 看板用户(authenticated)和只读组都不直接读任何表,只能调下一份迁移里的两个函数。
revoke all on all tables in schema reporting from public, anon, authenticated, pt_dashboard_readonly;
-- 写入方角色的 grant 由 DBA 按环境单独下发(与 tracking_worker 同样做法)。

commit;
