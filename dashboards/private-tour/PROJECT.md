# Project Metadata

## 基本信息

```yaml
name: private-tour-dashboard
description: Private Tour 广告 → SQL → 成交漏斗 + 销售跟进表现的内部看板
type: INTERNAL_TOOL
playbook:
  - PLAYBOOKS/04-internal-tool.md        # 看板本体
  - PLAYBOOKS/05-data-pipeline.md        # 广告花费 / 销售事实两张输入表的同步任务
```

## 业务信息

```yaml
owner: Jerry
owner_email: jerry@webuy.global
backup_contact: TBD
team: Commercial · Product
reviewers:
  data_platform_owner: 显方        # 执行 reporting 迁移、暴露 schema、维护白名单
  tracking_owner: Luna            # tracking schema(点击 / 线索阶段 / 订单事件)
lifecycle:
  status: planning
  expected_lifetime: 长期
```

## 用户与区域

```yaml
target_users: [Webuy 员工]          # Product / Marketing / Sales 主管
regions: [SG, ID, GLOBAL]           # 市场:sg / id / wetrip,按人按市场授权
expected_users:
  daily_active: "< 10"
  monthly_active: "< 30"
  peak_concurrent: "< 5"
```

## 数据与合规

```yaml
has_pii: NO
pii_details: >
  看板只读两个 SECURITY DEFINER 函数的聚合结果(按广告 / 按销售)。
  不返回任何客户手机号、邮箱、姓名、contact id。
  销售姓名属于员工信息,只对白名单内的人可见。
cross_region_data_transfer: NO      # 不复制数据;读的是数据平台已有的 market 分区数据
production_impact: NO               # 只读,不写 tracking / SkyBear / Respond.io
compliance_level: MEDIUM            # 含销售个人绩效
access_control:
  auth: Supabase Auth(公司邮箱登录链接)
  authorization: reporting.dashboard_viewers(email × markets 白名单),在函数入口校验
  bi_and_ai_readonly: 只读组 pt_dashboard_readonly(DBA 授给已有只读登录;只能 EXECUTE 两个看板函数)
  ai_data_access: SEABEAR 数据中台 MCP(飞书登录 / 个人 token,只读)
```

## 技术栈

```yaml
stack:
  frontend: Next.js 14 (App Router)
  backend: Next.js Server Components → Supabase RPC
  database: Supabase Postgres(数据平台 project,schema reporting;读 schema tracking)
  storage: 不需要
  auth: Supabase Auth
  hosting: Vercel(公司 team)
ai_apis: []
deviation_from_playbook:
  - "UI 未用 Tailwind + shadcn/ui:只有两张表 + 一排卡片,纯 CSS 更轻;页面变复杂再迁"
```

## 部署与运维

```yaml
deployment:
  platform: Vercel
  root_directory: dashboards/private-tour
  domain: "<pt-dashboard>.internal.webuy.global(待定)"
env_vars:
  - NEXT_PUBLIC_SUPABASE_URL        # Tier 3
  - NEXT_PUBLIC_SUPABASE_ANON_KEY   # Tier 3(权限靠函数白名单,不靠隐藏 key)
  - NEXT_PUBLIC_SITE_URL
monitoring: Vercel logs
```

## 成本

```yaml
estimated_monthly_cost:
  infrastructure: "< 5"     # 复用公司 Vercel Pro 与数据平台 Supabase
  ai_apis: 0
monthly_budget_cap_usd: 20
```
