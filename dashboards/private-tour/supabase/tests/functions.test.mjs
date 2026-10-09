// 用 PGlite(内嵌 Postgres)跑两份迁移 + 合成数据,校验两个看板函数的口径。
// 运行:npm run test:sql
// tracking.* 只建了函数用到的列;auth.jwt() 用 request.jwt.claims 模拟 Supabase。
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PGlite } from '@electric-sql/pglite';

const here = path.dirname(fileURLToPath(import.meta.url));
const migrations = path.join(here, '..', 'migrations');
const db = new PGlite();

await db.exec(`
  create role anon; create role authenticated;
  create schema auth;
  create function auth.jwt() returns jsonb language sql stable as $$
    select coalesce(nullif(current_setting('request.jwt.claims', true), ''), '{}')::jsonb $$;
  create schema tracking;
  create table tracking.tracking_clicks (event_id text primary key, market text, event_time timestamptz,
    short_code text, ad_id text, is_test_traffic boolean not null default false);
  create table tracking.lead_stage_history (event_id text primary key, market text, respond_io_contact_id text,
    contact_id text, stage text, occurred_at timestamptz, short_code text);
  create table tracking.order_conversion_events (event_id text, market text, event_name text, occurred_at timestamptz,
    order_ref text, value numeric(18,2), currency text, short_code text, product_id text, primary key (market, event_id));
`);
for (const f of fs.readdirSync(migrations).sort()) await db.exec(fs.readFileSync(path.join(migrations, f), 'utf8'));

await db.exec(`
  insert into reporting.pt_rules (rule_type, pattern) values ('product_id', 'PT-001');
  insert into reporting.dashboard_viewers (email, markets) values ('viewer@webuy.global', '{sg}');

  -- A1 / A2 命中 private 命名规则;N1 不是 PT 广告;A1 的 9 月花费不在区间内
  insert into reporting.ad_spend_daily (report_date, market, platform, campaign_name, ad_id, ad_name, spend, currency) values
    ('2026-10-01','sg','meta','SG_PrivateTour_Japan','A1','JP family video',100,'SGD'),
    ('2026-10-02','sg','meta','SG_PrivateTour_Japan','A1','JP family video',100,'SGD'),
    ('2026-09-01','sg','meta','SG_PrivateTour_Japan','A1','JP family video',999,'SGD'),
    ('2026-10-01','sg','google_ads','Search KR','A2','Private Tour Korea',50,'SGD'),
    ('2026-10-01','sg','meta','Group Tour Bali','N1','Bali group',80,'SGD');

  insert into tracking.tracking_clicks (event_id, market, event_time, short_code, ad_id, is_test_traffic) values
    ('c1','sg','2026-10-01 02:00+00','AAAA1111','A1',false),
    ('c2','sg','2026-10-01 03:00+00','BBBB2222','A2',false),
    ('c3','sg','2026-10-01 04:00+00','CCCC3333','N1',false),
    ('c4','sg','2026-10-01 05:00+00','DDDD4444','A1',true);   -- 测试流量,必须忽略

  insert into tracking.lead_stage_history (event_id, market, respond_io_contact_id, contact_id, stage, occurred_at, short_code) values
    ('l1a','sg','1',null,'WA_Contact','2026-10-01 02:05+00','AAAA1111'),       -- SQL 事件本身没码,沿用此前的码
    ('l1b','sg','1',null,'SQL','2026-10-02 02:00+00',null),
    ('l2','sg','2','respondio:2','SQL','2026-10-02 03:00+00','BBBB2222'),
    ('l3','sg','3','respondio:3','SQL','2026-10-03 03:00+00','CCCC3333'),       -- 非 PT 广告,但 lifecycle = tour private
    ('l4','sg','4','respondio:4','SQL','2026-10-03 03:00+00','DDDD4444'),       -- 只有测试流量点击,且不是 PT 联系人
    ('l5a','sg','5','respondio:5','SQL','2026-09-03 03:00+00','EEEE5555'),      -- 首次 SQL 在区间前,不算
    ('l5b','sg','5','respondio:5','SQL','2026-10-03 03:00+00','EEEE5555');

  insert into tracking.order_conversion_events (event_id, market, event_name, occurred_at, order_ref, value, currency, short_code, product_id) values
    ('o1','sg','purchase','2026-10-05 03:00+00','O1',8000,'SGD','AAAA1111',null),
    ('o1dup','sg','purchase','2026-10-05 04:00+00','O1',8000,'SGD','AAAA1111',null),  -- 同一订单重复事件
    ('o2','sg','purchase','2026-10-05 03:00+00','O2',5000,'SGD','CCCC3333',null),
    ('o3','sg','purchase','2026-10-06 03:00+00','O3',3000,'SGD',null,'PT-001'),       -- 靠产品规则算 PT
    ('o4','sg','deposit_paid','2026-10-06 03:00+00','O4',500,'SGD','AAAA1111',null);  -- 订金不算成交

  insert into reporting.lead_sales_facts (market, contact_id, sales_key, sales_name, lifecycle, travel_type, first_customer_msg_at, first_agent_reply_at) values
    ('sg','respondio:1','s1','Amy',null,null,'2026-10-01 02:06+00','2026-10-01 02:16+00'),
    ('sg','respondio:2','s2','Ben',null,null,'2026-10-01 03:01+00','2026-10-01 03:46+00'),
    ('sg','respondio:3','s1','Amy','Tour Private',null,'2026-10-01 04:01+00',null),
    ('sg','respondio:6',null,null,null,'private trip','2026-10-02 04:01+00','2026-10-02 04:06+00');
`);

// 三类调用方(PGlite 默认是超级用户,超级用户对 pg_has_role 恒为 true,所以测试都切到普通登录):
//   web_user    看板网页经 PostgREST 来的已登录用户(authenticated),靠 JWT 邮箱白名单
//   bi_reader   DBA 授予了 pt_dashboard_readonly 的只读登录,没有 JWT
//   other_login 普通已登录角色,既不在白名单也不在只读组
await db.exec(`
  create role web_user login;    grant authenticated to web_user;
  create role bi_reader login;   grant pt_dashboard_readonly to bi_reader;
  create role other_login login; grant authenticated to other_login;
`);
const switchTo = (role, claims = {}) => db.exec(`
  reset session authorization;
  set session authorization ${role};
  set request.jwt.claims = '${JSON.stringify(claims)}';
`);
const as = (email) => switchTo('web_user', { email });
const rows = async (sql) => (await db.query(sql)).rows.map((r) =>
  Object.fromEntries(Object.entries(r).map(([k, v]) => [k, typeof v === 'string' && /^-?\d+(\.\d+)?$/.test(v) ? Number(v) : v])));

await as('Viewer@webuy.global'); // 邮箱大小写不敏感

const ads = await rows(`select * from reporting.pt_ad_performance('sg', '2026-10-01', '2026-10-31') order by row_type, ad_id`);
const byAd = Object.fromEntries(ads.map((r) => [r.ad_id ?? r.row_type, r]));
assert.equal(ads.length, 3, 'A1、A2、未归因三行;N1 不是 PT 广告');
assert.deepEqual(
  [byAd.A1.spend, byAd.A1.sql_count, byAd.A1.orders, byAd.A1.revenue], [200, 1, 1, 8000],
  'A1:区间内花费、SQL(联系人 1)、订单 O1 去重');
assert.deepEqual([byAd.A2.spend, byAd.A2.sql_count, byAd.A2.orders, byAd.A2.revenue], [50, 1, 0, 0]);
assert.deepEqual(
  [byAd.unattributed.sql_count, byAd.unattributed.orders, byAd.unattributed.revenue], [1, 2, 8000],
  '未归因:联系人 3(lifecycle)+ 订单 O2(联系人 3)+ O3(产品规则)');

const sales = await rows(`select * from reporting.pt_sales_performance('sg', '2026-10-01', '2026-10-31')`);
const bySales = Object.fromEntries(sales.map((r) => [r.sales_key, r]));
assert.deepEqual(
  [bySales.s1.sql_count, bySales.s1.conversations, bySales.s1.replied, bySales.s1.avg_first_response_sec, bySales.s1.late_count, bySales.s1.orders, bySales.s1.revenue],
  [2, 2, 1, 600, 1, 2, 13000], 'Amy:联系人 1+3;未回复计入超时;订单 O1+O2');
assert.deepEqual(
  [bySales.s2.sql_count, bySales.s2.avg_first_response_sec, bySales.s2.late_count, bySales.s2.orders], [1, 2700, 1, 0],
  'Ben:45 分钟回复算超时');
assert.deepEqual(
  [bySales.__unassigned.sales_name, bySales.__unassigned.conversations, bySales.__unassigned.late_count, bySales.__unassigned.orders, bySales.__unassigned.revenue],
  ['(未分配)', 1, 0, 1, 3000], '未分配:联系人 6 + 没有联系人的订单 O3');

await assert.rejects(db.query(`select * from reporting.pt_ad_performance('id', '2026-10-01', '2026-10-31')`), /not allowed/, '没授权的市场');
await assert.rejects(db.query(`select * from reporting.pt_ad_performance('sg', '2026-10-31', '2026-10-01')`), /date range/, '日期倒置');
await as('someone@webuy.global');
await assert.rejects(db.query(`select * from reporting.pt_sales_performance('sg', '2026-10-01', '2026-10-31')`), /not allowed/, '不在白名单');

// 只读登录:不需要 JWT,能看全部市场;但读不到原始表、白名单表和内部函数
await switchTo('bi_reader');
assert.equal((await rows(`select * from reporting.pt_ad_performance('sg', '2026-10-01', '2026-10-31')`)).length, 3, '只读登录看 SG');
assert.ok(await rows(`select * from reporting.pt_sales_performance('id', '2026-10-01', '2026-10-31')`), '只读登录看 ID');
await assert.rejects(db.query(`select count(*) from tracking.lead_stage_history`), /permission denied/, '只读登录读不到原始表');
await assert.rejects(db.query(`select count(*) from reporting.dashboard_viewers`), /permission denied/, '只读登录读不到白名单');
await assert.rejects(db.query(`select * from reporting._sql_attributed('sg', '2026-10-01', '2026-10-31')`), /permission denied/, '内部函数不对外');

// 普通登录:没有白名单邮箱也不在只读组
await switchTo('other_login');
await assert.rejects(db.query(`select * from reporting.pt_ad_performance('sg', '2026-10-01', '2026-10-31')`), /not allowed/, '普通登录被拒');
await db.exec('reset session authorization');

console.log('reporting functions: all assertions passed');
