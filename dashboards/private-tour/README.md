# Private Tour 数据看板

盯 Private Tour 的投放和销售跟进:哪条广告带来 SQL、每个 SQL 花多少钱、最后成交多少;每个销售接了多少 SQL、回复多快、成交多少。数据来自**数据中台**(与 SEABEAR 同一套语义层口径)。

![示例数据预览](docs/preview.png)

> 截图是**示例数据**(合成的广告、销售和数字)。没配数据中台连接时看板自动进入示例模式,用来确认版式和口径。

## 看板内容

**顶部 6 个数**:广告花费 · SQL · CPSQL · 成交 · 成交金额 · ROI,和表 1 的“广告合计”同一口径。

**表 1:Private Tour 广告**(cohort 口径:日期 = 线索进来的日期)

| 列 | 算法 |
|---|---|
| 广告名称 | 广告名 + 平台 + 广告系列 |
| 花费 | 区间内该广告花费(广告账户原币) |
| 线索 | 区间内成为 lead、**硬归因**(广告 ID 匹配)到这条广告的 Respond 联系人 |
| SQL | 上述线索里后来成为 AUTO SQL 的人数 |
| CPSQL | 花费 ÷ SQL |
| 成交 | 上述线索后来下的 Private Tour 有效订单 |
| 金额 | 上述订单金额(订单原币) |
| 转化率 | 成交 ÷ SQL |
| ROI | 金额 ÷ 花费(倍数,未扣成本;花费和订单币种不同时不计算) |
| 其他团型成交 | 上述线索后来买的**不是** Private Tour(跟团 / 单项等) |

末尾固定一行 **“其他来源的 PT 订单”**:按下单日期统计、不是从 PT 广告进来的 Private Tour 订单(其他广告 / 自然流量 / 门店 / 链不到 Respond),不丢。

**表 2:销售表现**(日期 = 首次 AUTO SQL 的日期)

| 列 | 算法 |
|---|---|
| 销售 | Respond 当前分配人;没分配的归“(未分配)” |
| SQL | 区间内首次成为 AUTO SQL 的 Private Tour 联系人(来自 PT 广告,或后来买了 PT) |
| 会话数 | 区间内客户首次来消息的会话(近 30 天内,不限 Private Tour) |
| 平均首响 / 中位首响 | 客户第一条消息 → 之后第一条销售消息;未回复不进平均值 |
| 超时率 | 未回复或首响 > 30 分钟的会话占比(与 sales-leads-quality-hub 日报同阈值) |
| 订单 / 销售额 | 这些 SQL 联系人之后下的 Private Tour 有效订单 |
| 转化率 | 订单 ÷ SQL |

末尾固定一行 **“未链接 Respond 的 PT 订单”**:按下单日期统计、电话匹配不到本市场 Respond 联系人的 PT 订单(门店 / 线下 / 缺电话)。

两张表都能点表头排序、导出 CSV;可切市场(Webuy SG / Webuy ID / WeTrip)和日期(近 7 天 / 近 30 天 / 本月 / 上月 / 自定义)。

## 口径

全部沿用数据中台 catalog 的业务铁律(`describe` 里的 business_rules):

- **市场**:SG = `wbt_sg` 非 WeTrip 订单(WebuyTravel + Altitude,SGD)+ Respond `sg_webuytravel`;WeTrip = `is_wetrip_order`(USD)+ Respond `wetrip`;ID = `wbt_id`(IDR)+ Respond `id_webuytravel`。不同币种不相加。
- **Private Tour 订单** = `order_sales_view.is_effective` 且团型命中规则:SG 的 WebuyTravel PRV(3)、Altitude PRV(6);WeTrip 的 WPRV(5)、WFIT(9,WeTrip 统一口径计入 Private Tour);ID 的 PRV(3)。
- **Private Tour 广告** = 广告系列 / 广告组 / 广告名命中正则(Private Tour、[Standard PT]、SPT、私家定制)。
- 规则都在 `reporting.pt_rules`,改规则不用改代码,下次快照刷新生效。
- **SQL** = `respondio_auto_sql_contact_fact`(Respond AUTO SQL,已排除人工剔除的误报)。
- **成交**:`contact_order_link` 高置信匹配(`match_confidence >= 0.95`),下单不早于咨询;一张订单只记给一个联系人,不在广告之间重复计。
- **归因**:默认 cohort(数据中台 `ad_business_attribution` 的默认口径),只算 `confirmed_ad` 的硬归因。

## 数据怎么连

按 `webuytravel/ai-project-template` 的决策树:内部 dashboard = **INTERNAL_TOOL → PLAYBOOK 04 → Vercel + Supabase**,数据读公司**数据中台 Supabase**,不直连华为云 Travel MySQL,不新建账号或新库。

```
数据中台语义层(semantic / curated,只读)
  meta_ad_daily_metrics · ad_campaigns           广告与花费
  respondio_contact_attribution_fact            联系人 → 广告
  respondio_auto_sql_contact_fact               AUTO SQL
  contact_order_link · order_sales_view         联系人 ↔ 订单、订单真值(团型)
  respondio_contact_assignee · message_hot_30d  销售归属、首响
        │  pg_cron 每小时 reporting.refresh_pt_facts()
        ▼
reporting.pt_*_mv  五张小快照(只含 Private Tour 相关行)
        │  SECURITY DEFINER,入口查白名单 / 只读组
        ▼
reporting.pt_ad_performance · reporting.pt_sales_performance
        │
        ├── Next.js 看板(Vercel,Supabase Auth 公司邮箱登录,PostgREST)
        └── BI / AI 只读体检(专用只读登录 + pt_dashboard_readonly 组)
```

**为什么用快照**:口径要串好几个大视图,现场算一次 10–20 秒,超过 PostgREST 给网页请求的超时。快照和数据中台 V194 联系人匹配快照是同一做法,看板只在小表上汇总,页面打开是毫秒级。

**权限**:看板用户和只读组都读不到任何表和快照,只能调两个函数。网页用户按 `reporting.dashboard_viewers`(邮箱 × 市场)放行,SG / ID / WeTrip 分开授权;数据库只读登录要被 DBA 授予 `pt_dashboard_readonly` 组(和 IDN 漏斗看板的 `idn_funnel_readonly` 同一做法)。输出只有聚合数,不含客户姓名、电话、contact id。

**AI 问数**走数据中台的 SEABEAR MCP:claude.ai → Settings → Connectors → SEABEAR → Connect(飞书登录);Claude Code 等命令行工具用个人 token(找 Vincent 要)。步骤见飞书文档《SEABEAR 数据中台 · 接入指南》。token 不进 git、不贴聊天;Claude Code 云端会话把 token 配在环境变量 `SEABEAR_MCP_TOKEN`。

## 已知缺口

- **AI Sales 平台的会话 / SQL 还没算进来**。数据中台把 AI Sales 和 Respond 当成两个独立来源,规定分开统计。部分广告(如 WeTrip `SPT-在投`、带 `AI-WA` 的)把会话引到 AI Sales,在 Respond 里没有线索,所以表 1 会低估这些广告。要补的话,按数据中台规则单独加一套 AI Sales 口径(`semantic.ai_sales_*`),和 Respond 并列展示。
- **首响含自动回复**:消息表 `sender_name` 采集侧为空,分不出人工 / 自动回复 / AI;而且只保留近 30 天。要算真人首响,需要数据中台在消息表补发送方类型。
- **WeTrip 的 ROI 不显示**:广告花费是 SGD、订单是 USD,数据中台规定未换汇不能相除。需要数据中台提供汇率表,或约定固定汇率。
- **很多 SG 的 PT 订单链不到 Respond**(门店 / 线下 / 缺电话),这些单进了“其他来源”和“未链接 Respond”两行,算不到具体广告和销售头上。
- **Google Ads 目前没有命中 PT 规则的系列**;代码已支持 Google 广告组粒度,有了就会出现。

## 上线步骤

按先后顺序。括号里是建议的负责人。

1. **只读体检**(任何人,经 SEABEAR 或 SQL Editor):跑 `supabase/checks/preflight.sql`,确认依赖的列都在、数据新鲜。
2. **执行迁移**(数据中台 DBA · 显方):按顺序执行 `supabase/migrations/` 的三个文件,然后:
   - `select reporting.refresh_pt_facts();` 首次填充快照(联系人快照全量约 15 秒);
   - `select cron.schedule('reporting-pt-refresh', '35 * * * *', 'select reporting.refresh_pt_facts()');` 每小时刷新(错开数据中台 :25 的联系人快照);
   - Supabase → API settings → Exposed schemas 加 `reporting`;
   - 把看板用户加进 `reporting.dashboard_viewers`,BI 只读登录 `GRANT pt_dashboard_readonly TO "<已有只读登录>"`(验证语句在第三份迁移末尾)。
3. **确认 Private Tour 规则**(Product + Marketing):团型和广告命名正则是否符合业务;有新的命名约定,往 `reporting.pt_rules` 加一行。
4. **部署**(owner):公司 Vercel team 新建项目 `private-tour-dashboard`,Root Directory 选 `dashboards/private-tour`,配 `.env.example` 里的 3 个变量。Supabase 凭据按 `ai-project-template/COMPLIANCE/access-request.md` 申请,不要自己注册账号。

## 本地运行

```bash
cd dashboards/private-tour
npm ci
npm run dev          # http://localhost:3000;不配 .env.local 就是示例数据模式
npm run typecheck
npm run test:sql     # 内嵌 Postgres 跑三份迁移 + 合成数据,校验快照、两个函数的口径和权限
```

连真实数据:复制 `.env.example` 为 `.env.local`(已 gitignore),填数据中台 Supabase URL 和 anon key,用白名单里的公司邮箱登录。

## 文件

```
dashboards/private-tour/
├── app/
│   ├── page.tsx                 看板页(服务端取数)
│   ├── components/              KPI 卡片、两张表、筛选条、通用排序表
│   ├── login/ · auth/           Supabase 邮件链接登录 / 回调 / 退出
│   └── globals.css              浅色 / 深色主题
├── lib/
│   ├── data.ts                  调 reporting 函数;没配置时走示例数据
│   ├── metrics.ts               CPSQL / 转化率 / ROI / 合计与格式化
│   ├── query.ts                 URL 参数 → 市场与日期
│   └── demo-data.ts             合成示例数据
├── supabase/
│   ├── migrations/
│   │   ├── …0001_reporting_config.sql     PT 规则、白名单、只读组
│   │   ├── …0002_reporting_pt_facts.sql   五张小时级快照 + 刷新函数
│   │   └── …0003_reporting_pt_functions.sql  两个看板函数 + 权限
│   ├── checks/preflight.sql     执行迁移前的只读体检
│   └── tests/functions.test.mjs SQL 口径与权限测试
├── CLAUDE.md · PROJECT.md       ai-project-template 要求的项目文件
└── .env.example
```
