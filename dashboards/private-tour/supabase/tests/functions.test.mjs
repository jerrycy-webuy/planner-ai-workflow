// 用 PGlite(内嵌 Postgres)跑三份迁移 + 合成数据,校验快照与两个看板函数的口径和权限。
// 运行:npm run test:sql
// semantic / curated 只建了函数用到的列;auth.jwt() 用 request.jwt.claims 模拟 Supabase。
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PGlite } from '@electric-sql/pglite';

const here = path.dirname(fileURLToPath(import.meta.url));
const migrations = path.join(here, '..', 'migrations');
const db = new PGlite();

const hot = (name) => `create table curated.${name} (contact_id text, sender_role text, message_at timestamptz, date_sgt date);`;
await db.exec(`
  create role anon; create role authenticated;
  create schema auth;
  create function auth.jwt() returns jsonb language sql stable as $$
    select coalesce(nullif(current_setting('request.jwt.claims', true), ''), '{}')::jsonb $$;
  create schema curated; create schema semantic;
  create table curated.meta_ad_daily_metrics (date date, account_id text, campaign_id text, campaign_name text,
    adset_id text, adset_name text, ad_id text, ad_name text, currency text, spend numeric);
  create table curated.meta_ad_dimension (account_id text, account_region text, campaign_name text, adset_name text,
    ad_id text, ad_name text, last_seen_at timestamptz);
  create table curated.ad_campaigns (source_system text, account_id text, account_region text, campaign_id text,
    campaign_name text, group_id text, group_name text, date date, cost numeric, currency text);
  create table semantic.respondio_contact_attribution_fact (region text, respondio_contact_id text, lead_date date,
    ad_id text, adset_id text, campaign_id text, confirmed_ad boolean);
  create table semantic.respondio_auto_sql_contact_fact (region text, respondio_contact_id text, auto_sql_date date);
  create table semantic.contact_order_link (region text, respondio_account text, respondio_contact_id text,
    order_business_entity text, order_id bigint, booking_date date, match_confidence numeric);
  create table semantic.order_sales_view (legal_entity text, order_id bigint, booking_date date, total_amount numeric,
    order_currency text, pax_type int, is_effective boolean, is_wetrip_order boolean);
  create table semantic.respondio_contact_assignee (account_id text, contact_id text, assignee_id text, assignee_name text);
  ${hot('respondio_sg_webuytravel_message_hot_30d')}
  ${hot('respondio_wetrip_message_hot_30d')}
  ${hot('respondio_id_webuytravel_message_hot_30d')}
`);
for (const f of fs.readdirSync(migrations).sort()) await db.exec(fs.readFileSync(path.join(migrations, f), 'utf8'));

await db.exec(`
  insert into reporting.dashboard_viewers (email, markets) values ('viewer@webuy.global', '{wetrip,sg}');

  -- 广告:W1 = WeTrip 账号,S1 = SG 账号。A1 / A2 / SA 命中 PT 正则,N1 不命中
  insert into curated.meta_ad_dimension values
    ('W1','wetrip','[Standard PT]-WhatsApp-US','set','A1','pt video', now()),
    ('W1','wetrip','SPT-在投','set','A2','x', now()),
    ('W1','wetrip','Group Tour Bali','set','N1','bali', now()),
    ('S1','sg','[NP01]Private tour - 17 Apr','set','SA','guangzhou', now());
  insert into curated.meta_ad_daily_metrics (date, account_id, campaign_name, adset_name, ad_id, ad_name, currency, spend) values
    ('2026-10-01','W1','[Standard PT]-WhatsApp-US','set','A1','pt video','SGD',100),
    ('2026-10-02','W1','[Standard PT]-WhatsApp-US','set','A1','pt video','SGD',50),
    ('2026-09-01','W1','[Standard PT]-WhatsApp-US','set','A1','pt video','SGD',999),
    ('2026-10-01','W1','SPT-在投','set','A2','x','SGD',30),
    ('2026-10-01','W1','Group Tour Bali','set','N1','bali','SGD',80),
    ('2026-10-01','S1','[NP01]Private tour - 17 Apr','set','SA','guangzhou','SGD',40);

  insert into semantic.respondio_contact_attribution_fact values
    ('wetrip','c1','2026-10-01','A1',null,null,true),
    ('wetrip','c2','2026-10-02','A1',null,null,true),
    ('wetrip','c3','2026-10-03','A2',null,null,true),
    ('wetrip','c4','2026-10-03','N1',null,null,true),    -- 不是 PT 广告,但后来买了 PT
    ('wetrip','c5','2026-09-01','A1',null,null,true),    -- lead 在区间前:不进 cohort,但首次 SQL 在区间内
    ('wetrip','c6','2026-10-02','A1',null,null,false),   -- 非硬归因,不算
    ('sg','c7','2026-10-01','SA',null,null,true);
  insert into semantic.respondio_auto_sql_contact_fact values
    ('wetrip','c1','2026-10-02'), ('wetrip','c1','2026-10-06'),
    ('wetrip','c3','2026-10-05'), ('wetrip','c4','2026-10-04'), ('wetrip','c5','2026-10-03'),
    ('sg','c7','2026-10-02');

  insert into semantic.order_sales_view values
    ('wbt_sg',1,'2026-10-10',8000,'USD',5,true,true),    -- c1 的 PT 单
    ('wbt_sg',2,'2026-10-11',2000,'USD',4,true,true),    -- c1 的 W-Group:其他团型
    ('wbt_sg',3,'2026-10-12',5000,'USD',5,true,true),    -- 链不到联系人
    ('wbt_sg',4,'2026-10-13',3000,'USD',5,true,true),    -- c4(非 PT 广告)的 PT 单
    ('wbt_sg',5,'2026-10-14',9999,'USD',5,false,true),   -- 已取消,不算
    ('wbt_sg',6,'2026-10-14',1000,'USD',9,true,true),    -- WFIT,只有低置信匹配
    ('wbt_sg',7,'2026-10-05',1500,'SGD',1,true,false),   -- SG:c7 的跟团单(其他团型)
    ('wbt_sg',8,'2026-10-06',7000,'SGD',6,true,false);   -- SG:Altitude PRV,链不到
  insert into semantic.contact_order_link values
    ('wetrip','wetrip','c1','wbt_sg',1,'2026-10-10',0.95),
    ('wetrip','wetrip','c1','wbt_sg',2,'2026-10-11',0.95),
    ('wetrip','wetrip','c4','wbt_sg',4,'2026-10-13',0.95),
    ('wetrip','wetrip','c1','wbt_sg',5,'2026-10-14',0.95),
    ('wetrip','wetrip','c3','wbt_sg',6,'2026-10-14',0.60),
    ('sg','sg_webuytravel','c7','wbt_sg',7,'2026-10-05',0.95);

  insert into semantic.respondio_contact_assignee values
    ('wetrip','c1','u1','Amy'), ('wetrip','c3','u2','Ben'), ('wetrip','c4','u1','Amy'), ('wetrip','c5','u2','Ben');
  insert into curated.respondio_wetrip_message_hot_30d values
    ('c1','customer','2026-10-01 10:00+08','2026-10-01'), ('c1','sales-agent','2026-10-01 10:10+08','2026-10-01'),
    ('c2','customer','2026-10-02 10:00+08','2026-10-02'),
    ('c3','customer','2026-10-03 10:00+08','2026-10-03'), ('c3','sales-agent','2026-10-03 11:00+08','2026-10-03'),
    ('c4','sales-agent','2026-10-04 09:00+08','2026-10-04'),   -- 客户来消息之前的销售消息不算回复
    ('c4','customer','2026-10-04 10:00+08','2026-10-04'), ('c4','sales-agent','2026-10-04 10:01+08','2026-10-04');

  select reporting.refresh_pt_facts();
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
  set session authorization postgres;
  set session authorization ${role};
  set request.jwt.claims = '${JSON.stringify(claims)}';
`);
const num = (v) => (typeof v === 'string' && /^-?\d+(\.\d+)?$/.test(v) ? Number(v) : v);
const rows = async (sql) => (await db.query(sql)).rows.map((r) => Object.fromEntries(Object.entries(r).map(([k, v]) => [k, num(v)])));
const pick = (r, keys) => keys.map((k) => r[k]);

await switchTo('web_user', { email: 'Viewer@webuy.global' }); // 邮箱大小写不敏感

// ---- 表 1:WeTrip ----
const ads = await rows(`select * from reporting.pt_ad_performance('wetrip', '2026-10-01', '2026-10-31')`);
const byAd = Object.fromEntries(ads.map((r) => [r.ad_id ?? r.row_type, r]));
assert.deepEqual(Object.keys(byAd).sort(), ['A1', 'A2', 'unattributed'], 'N1 不是 PT 广告,SA 是 SG 的');
const KEYS = ['spend', 'contacts', 'sql_count', 'orders', 'other_orders', 'revenue', 'revenue_currency'];
assert.deepEqual(pick(byAd.A1, KEYS), [150, 2, 1, 1, 1, 8000, 'USD'],
  'A1:区间内花费;cohort c1+c2(c5 lead 在区间前、c6 非硬归因不算);c1 成为 SQL;PT 单 1、其他团型 1;取消单不算');
assert.deepEqual(pick(byAd.A2, KEYS), [30, 1, 1, 0, 0, 0, 'USD'], 'A2:c3 的 WFIT 单只有低置信匹配,不算成交');
assert.equal(byAd.A1.spend_currency, 'SGD', '花费按广告账户原币');
assert.deepEqual(pick(byAd.unattributed, ['sql_count', 'orders', 'revenue']), [null, 3, 9000],
  '未归因:区间内 PT 单里不是从 PT 广告来的 —— 3 号(无链接)、4 号(c4 来自非 PT 广告)、6 号(低置信)');
assert.ok(byAd.A1.snapshot_at, '带快照时间');

// ---- 表 1:SG(市场隔离)----
const sgAds = await rows(`select * from reporting.pt_ad_performance('sg', '2026-10-01', '2026-10-31')`);
const sgBy = Object.fromEntries(sgAds.map((r) => [r.ad_id ?? r.row_type, r]));
assert.deepEqual(pick(sgBy.SA, KEYS), [40, 1, 1, 0, 1, 0, 'SGD'], 'SG:PT 广告带来的人买了跟团单 → 其他团型 1');
assert.deepEqual(pick(sgBy.unattributed, ['orders', 'revenue']), [1, 7000], 'SG:Altitude PRV 算 PT');

// ---- 表 2:WeTrip ----
const sales = await rows(`select * from reporting.pt_sales_performance('wetrip', '2026-10-01', '2026-10-31')`);
const bySales = Object.fromEntries(sales.map((r) => [r.sales_key, r]));
const SK = ['sales_name', 'sql_count', 'conversations', 'replied', 'avg_first_response_sec', 'median_first_response_sec', 'late_count', 'orders', 'revenue'];
assert.deepEqual(pick(bySales.u1, SK), ['Amy', 2, 2, 2, 330, 330, 0, 2, 11000],
  'Amy:SQL c1 + c4(c4 因买了 PT 算 PT 联系人);首响 600s / 60s;SQL 之后的 PT 单 1 号 + 4 号');
assert.deepEqual(pick(bySales.u2, SK), ['Ben', 2, 1, 1, 3600, 3600, 1, 0, 0],
  'Ben:SQL c3 + c5(c5 lead 早但首次 SQL 在区间内);c3 首响 1 小时算超时');
assert.deepEqual(pick(bySales.__unassigned, ['sales_name', 'sql_count', 'conversations', 'replied', 'late_count']),
  ['(未分配)', 0, 1, 0, 1], '未分配:c2 没回复,计入超时');
assert.deepEqual(pick(bySales.__offline, ['sql_count', 'orders', 'revenue']), [null, 2, 6000],
  '未链接 Respond:3 号(无链接)+ 6 号(只有低置信)');

// ---- 权限与参数 ----
await assert.rejects(db.query(`select * from reporting.pt_ad_performance('id', '2026-10-01', '2026-10-31')`), /not allowed/, '没授权的市场');
await assert.rejects(db.query(`select * from reporting.pt_ad_performance('sg', '2026-10-31', '2026-10-01')`), /date range/, '日期倒置');
await assert.rejects(db.query(`select count(*) from reporting.pt_contact_mv`), /permission denied/, '网页用户读不到快照');
await switchTo('web_user', { email: 'someone@webuy.global' });
await assert.rejects(db.query(`select * from reporting.pt_sales_performance('wetrip', '2026-10-01', '2026-10-31')`), /not allowed/, '不在白名单');

await switchTo('bi_reader');
assert.equal((await rows(`select * from reporting.pt_ad_performance('wetrip', '2026-10-01', '2026-10-31')`)).length, 3, '只读登录看 WeTrip');
assert.ok(await rows(`select * from reporting.pt_sales_performance('id', '2026-10-01', '2026-10-31')`), '只读登录看 ID');
await assert.rejects(db.query(`select count(*) from semantic.contact_order_link`), /permission denied/, '只读登录读不到语义层原表');
await assert.rejects(db.query(`select count(*) from reporting.pt_order_mv`), /permission denied/, '只读登录读不到快照');
await assert.rejects(db.query(`select count(*) from reporting.dashboard_viewers`), /permission denied/, '只读登录读不到白名单');
await assert.rejects(db.query(`select reporting.refresh_pt_facts()`), /permission denied/, '只读登录不能刷新快照');

await switchTo('other_login');
await assert.rejects(db.query(`select * from reporting.pt_ad_performance('sg', '2026-10-01', '2026-10-31')`), /not allowed/, '普通登录被拒');

// ---- 快照可重复刷新(第二次走 CONCURRENTLY)----
await db.exec('set session authorization postgres');
await db.exec('select reporting.refresh_pt_facts()');

console.log('reporting snapshots + functions: all assertions passed');
