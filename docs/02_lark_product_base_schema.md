---
type: note
status: active
created: 2026-07-17
updated: 2026-07-17
source: Claude
owner: [Jerry]
bu: [WEBUY_SG, ALTITUDE, WETRIP, Group]
tags: [Planner, Lark, Base, Costing, Schema, ProductBase]
confidence: high
last_reviewed: 2026-07-17
---

# Lark Product Base 表结构草案 v0.1（统一 costing 模板）

> [[2026-07-17_Planner_Workflow_AI_Architecture_v0.1]] P0 地基。2026-07-17 [[Jerry]] 拍板：**Jerry 先定稿直接发给 Planner 用，用中迭代**。**§9 全部 8 项已于 2026-07-18 定稿，本 schema 可直接建 Base**（仅余 2 个口径小旗待 Jerry 顺手确认，见 §9.1）。
> 覆盖 6 位 Planner（[[Bernice]] / [[Jasmin]] / [[Dorothy]] / [[Jaccy]] / [[Leen]] / [[Xinmei]]）全区域，替代各自 Excel。

---

## 0. 设计原则

1. **一份数据处处渲染**：Departures 表就是价格矩阵的唯一事实源。行程 PDF、Skybear API payload、销售弹药都从这里 + ProductSpec 生成，Planner 不再多处手抄。
2. **成本三来源分离**：机票（Air_Blocks）、地接（Quotes/Quote_Lines）、杂费（Departures 直填）各有归属，Departure 只做引用和汇总 — 改源头，全部引用它的日期自动重算。
3. **档位规则化**：促销/早鸟/会员价不逐格手填，写成 Price_Rules 规则，由 AI 生成最终矩阵。
4. **AI 读写友好**：表名/字段名**纯英文**（与 Skybear 后台术语对齐，2026-07-18 定稿）、枚举值固定、公式列与人填列严格分开（AI 只写「AI 填」和「回填」列，绝不碰 Planner 判断列）。
5. **红旗前置**：margin 低于 BU target 在表内直接标红，不等月底对账（吸取 [[Lark_Costing_Sheet_2026]] 312 低毛利行教训）。

## 1. 表清单与关系

```
① Products 产品表 (Tour Type)
   ├─< ② Departures 出发日期表 (Tour Code)   ←─ 引用 ⑦ Air_Blocks / ⑤ Quote_Lines / ⑧ FX_Rates
   ├─< ③ Price_Rules 档位规则表
   └─< ④ Quotes 报价单表 ──< ⑤ Quote_Lines 报价明细行
⑥ Suppliers 供应商表 ──< ④ Quotes / ⑦ Air_Blocks
⑦ Air_Blocks 机票批次表
⑧ FX_Rates 汇率表
```

8 张表一个 Base。①②是每天用的主战场；④⑤⑥⑦是弹药库；③⑧是规则/参数表。

## 2. ① Products 产品表（Tour Type 级，一产品一行）

| 字段 | Lark 类型 | 谁填 | 说明 |
|---|---|---|---|
| Product Code 产品代码 | 文本（主键） | Planner | 如 `WBKMG8`，与 Skybear Tour Type 代码一致 |
| Name EN / Name CN | 文本 ×2 | Planner | 与前台展示名一致 |
| BU | 单选：WEBUY_SG / ALTITUDE / WETRIP | Planner | 定位硬约束来源 |
| Planner | 人员 | Planner | 每人默认视图按此过滤 |
| Region 区域 | 单选：China / Japan / Korea / Taiwan / Vietnam / SEA / Cruise / Europe / Americas / Exotic | Planner | 与 6 位 Planner 分工对齐（[[Xinmei]] 区域定了后补枚举） |
| Destinations 目的地 | 多选 | Planner | 国家/城市标签，供 A1 竞品匹配 |
| Days / Nights | 数字 ×2 | Planner | 拆成数字便于比价（8D6N → 8 / 6） |
| Target Margin % | 数字（带默认公式） | 默认+Planner | **默认 = Region 基准 + (BU=ALTITUDE 加 5pp)**：China 18 / Europe & Americas 12 / Asia（日韩台越）15 / SEA 15 / Exotic 15（2026-07-18 Jerry 定稿）；可按产品覆盖。⚠️ 两个小旗见 §9.1 |
| Status | 单选：构思 / 询价中 / Costing / 待上架 / 在售 / 停售 / 归档 | Planner | 待上架视图的驱动字段 |
| Main Airline 主航司 | 关联 ⑥ | Planner | |
| Competitor Benchmark 竞品对标 | 文本+数字 | AI（A1 回填） | 同类竞品名 + 中位价，定价时并排看 |
| ProductSpec 链接 | URL/附件 | AI | 行程 spec（对接 [[webuy-itinerary]] TourSpec） |
| Sales Kit 链接 | URL | AI（A7 回填） | Lark 知识库弹药页 |
| Skybear Tour Type ID | 文本 | AI（A6 回填） | API 建成后回写 |
| Created / Updated | 自动 | — | |

## 3. ② Departures 出发日期表（Tour Code 级，一日期一行）— 主战场

| 字段 | Lark 类型 | 谁填 | 说明 |
|---|---|---|---|
| Tour Code | 文本（主键） | Planner/AI | 与 Skybear Tour Code 一致 |
| Product | 关联 ① | Planner/AI | |
| Departure / Return Date | 日期 ×2 | Planner/AI | 班期定稿后 AI 可按 Air_Block 批量生成行 |
| Season 季节档 | 单选：淡 / 平 / 旺 / 节假 | Planner | 影响地接报价行匹配 |
| Group Size / Min Pax | 数字 ×2 | Planner | 计划收客 / 成团人数 |
| Air Block | 关联 ⑦ | Planner | 机票成本来源 |
| Air Cost/pax SGD | 查找引用（⑦ Base Fare + Airport Tax & Fuel） | 公式 | 税燃在⑦单列，航司调税只改一处 |
| Land Quote Line | 关联 ⑤ | Planner | 选用的地接报价行（按日期段+人数档） |
| Land Cost 原币 / Currency | 查找引用（⑤） | 公式 | |
| FX Rate | 查找引用（⑧ active）或快照数字 | 公式/AI | 口径见 §9 待定稿 |
| Land Cost/pax SGD | 公式 = 原币 × FX | 公式 | |
| Tips / Visa / Insurance / Tour Leader Cost / Other | 数字 ×5 | Planner | 已定稿（§9）；Tour Leader Cost 按成团人数摊 /pax |
| **Total Cost/pax SGD** | 公式 = Air + Land + 杂费合计 | 公式 | |
| Suggested Price 建议售价 | 公式 = Cost ÷ (1 − Target Margin%)，**向上取整到尾数 88**（如 2,014 → 2,088） | 公式 | AI 出「建议价 vs 竞品对标」参考 |
| **Adult Twin Price 成人价** | 数字 | **Planner 定稿** | 最终判断永远在人 |
| Child w/ Bed / Child no Bed | 数字 ×2 | Planner | |
| Single Supplement 单房差 | 数字 | Planner | |
| Triple Room Price 三人房价 | 数字 | Planner | 2026-07-18 新增第 5 档 |
| **Margin %** | 公式 = (Adult − Cost) ÷ Adult | 公式 | |
| **Margin Flag** | 公式：Margin < Target → 🔴 | 公式 | 红旗视图驱动字段 |
| Status | 单选：未开放 / 在售 / 热卖 / 满位 / 砍班风险 / 已砍班 / 已出发 | Planner/AI | A8 可回填建议 |
| Seats Sold / Seats Left | 数字 ×2 | AI（webuy-data 定时回填） | `seat_availability_view` |
| Skybear Synced / Last Sync | 复选 + 时间 | AI（A6 回填） | 改价后自动置未同步 |
| Sync Diff | 文本 | AI | 「表内价 vs Skybear 现价」差异摘要，同步前必看 |

## 4. ③④⑤⑥⑦⑧ 支撑表

### ③ Price_Rules 档位规则表（促销不逐格手填）
Rule Name（Early Bird / NATAS Promo…；**[[Golden_Circle]] 会员价不进 Base**，由销售端/CRM 处理 — 2026-07-18 定稿）· Product（关联①，留空=通用）· Type（单选：减固定额 / 减% / 覆盖价）· Value · Applies To（多选：Adult / Child / Single Supp）· Booking Window（预订日期起止）· Departure Filter（出发日期起止）· Stackable 可叠加（复选）· Priority · Status（启用/停用）。
→ **AI 用 ②×③ 生成最终价格矩阵**（Skybear payload / 弹药里的促销话术同源）。

### ④ Quotes 报价单表（A3 报价转录官的落点）
Quote ID（自动编号）· Supplier（关联⑥）· Product（关联①）· Type（单选：地接 / 机票 / 门票 / 其他）· Received / Valid Until（日期）· Currency（单选）· Original File（附件，原始 Excel/Word/PDF）· Inclusions / Exclusions（多选：酒店/餐/门票/车/导游/小费/单房差…）· Meals 含餐数 · Hotel Level · **Gap Notes 漏项差异**（文本，AI 填：与需求单比对结果）· Status（收到 / 比价中 / 选用 / 淘汰）。

### ⑤ Quote_Lines 报价明细行（地接报价常是「日期段 × 人数档」矩阵，摊平成行）
Quote（关联④）· Date Range 适用出发期 · Pax Tier 人数档（如 16–20 / 21–25）· Unit Price/pax 原币 · Single Supp 原币 · Child Price 原币 · Notes（旺季/节假附加）。

### ⑥ Suppliers 供应商表
Name · Type（单选：地接社 / 航司 / GSA / 票代 / 门票商）· Regions Covered（多选）· Contacts（文本：人 + WhatsApp/微信/Email）· Rating（A/B/C）· Cooperation Status（合作中 / 新接触 / 黑名单）· Notes（历史表现，复盘链接 → `40_Operations/`）。

### ⑦ Air_Blocks 机票批次表（航司谈判的输出落点）
Block ID · Airline（关联⑥）· Route（如 SIN-KMG-SIN）· Flight Nos & 时刻 · Period 适用期间 · **Base Fare /pax SGD** · **Airport Tax & Fuel /pax SGD**（拆列，调税只改一列 — 2026-07-18 定稿）· Seats 团位 · **Deposit Deadline / Name List Deadline**（日期 — A8 可做到期提醒）· Payment Terms · Status（谈判中 / 已锁定 / 已用完 / 已释放）。

### ⑧ FX_Rates 汇率表（变动重算的开关）
Currency（单选）· Rate to SGD · Effective Date · Source · Active（复选）。
→ 更新汇率 = 改一行，所有引用该币种的 Departure 自动重算，Margin Flag 立刻显形。

## 5. 核心机制

1. **成本公式链**：⑦机票 + ⑤地接×⑧汇率 + 杂费 → Total Cost → 建议售价（毛利倒推）→ Planner 定稿成人价 → Margin% → 红旗。全链公式列，零手工摊算。
2. **变动重算**：改 FX / Quote_Line / Air_Block 任一源头 → 引用它的全部日期自动重算 → AI 每日扫红旗视图，产出**影响清单**（哪些日期跌破 target、建议动作）推给对应 Planner。
3. **档位生成**：标准档在②（4 个价格列），促销档在③规则化；AI 合成最终矩阵后走 A6 API 上 Skybear。
4. **Skybear 同步闭环**：②表价格改动 → Synced 自动置否 → 「待同步」视图 → AI 出 Sync Diff → Planner 确认 → API 批量写入 → 回填 Synced 时间。

## 6. 视图设计（开箱即用）

| 视图 | 表 | 过滤/用途 |
|---|---|---|
| 我的产品 | ① | Planner = 当前人（每人默认首页） |
| 🔴 低毛利红旗 | ② | Margin Flag = 🔴，AI 影响清单数据源 |
| 待上架 | ① | Status = 待上架 |
| 改价待同步 | ② | Synced = 否，A6 的工作队列 |
| 报价比价台 | ⑤ | 按 Product 分组，多家并排 |
| 机票到期提醒 | ⑦ | Deposit / Name List deadline 临近 |
| 本周出发 | ② | 出发日 7 天内（OP 协同用，[[Xinmei]] 双角色场景） |

## 7. Skybear API 字段映射（占位）

[[Cheng_Tai]] 确认 API 2026-07-20 当周上线。**拿到接口文档后在此补三张映射表**：① Products → create tour type 字段、② Departures×Price_Rules → 价格 payload、③ ProductSpec → Package Content。映射表定稿即 A6 开发完成大半。

## 8. 落地步骤

1. Jerry 勾完 §9 → 定稿（目标本周）
2. 建 Base + 权限：Planner 全员可写，销售/OP 只读特定视图；6 人各建默认视图
3. **试点 1**：[[Bernice]] 中国线 1–2 个产品，从 All China Costing Sheet 2026 迁移（AI 做搬运）
4. **试点 2**：[[Jaccy]] 日韩台 1 个高频改价产品（验证同步闭环）
5. Skybear API 上线 → §7 映射 → A6 联调
6. 全量铺开：双平台提示词包（Claude Skill + ChatGPT 版）+ 一次 30 分钟 Planner 培训

## 9. 定稿记录（2026-07-18 Jerry 逐项拍板，8/8 完成）

- [x] **杂费拆列** → Tips / Visa / Insurance / **Tour Leader Cost** / Other 五列；**机场税燃油**在 Air_Blocks 拆单列（Base Fare 与 Airport Tax & Fuel 分开）
- [x] **标准价格档** → 5 档：Adult Twin / Child w Bed / Child no Bed / Single Supplement / **Triple Room**
- [x] **Golden Circle 会员价** → **不进 Product Base**，定价表只管门市价，会员优惠由销售端/CRM 处理
- [x] **汇率口径** → **始终引用最新汇率**，成本自动重算 + margin 红旗 + AI 影响清单；售价 Planner 手填不自动变
- [x] **建议售价取整** → 向上取整到**尾数 88**（如 2,014 → 2,088）
- [x] **Target Margin 默认** → China 18% / Europe 12% / Asia（日韩台越）15% / SEA 15% / Exotic 15%；**ALTITUDE = 对应 WEBUY TRAVEL 区域基准 + 5pp**（如 ALTITUDE Europe 17%、ALTITUDE China 23%）
- [x] **Xinmei 区域** → **协助中国线**（跟 [[Bernice]]，WEBUY TRAVEL + WETRIP）+ 兼 OP；Region 枚举不新增，她默认视图 = China
- [x] **命名语言** → 表名/字段名**纯英文**（与 Skybear 后台术语对齐）

## 9.1 定稿带出的两个口径小旗（待 Jerry 顺手确认）

- **SEA margin 15% vs 旧口径 20%**：[[Jaccy]] 卡片与 [[2026Q2_Commercial_Platform_KPI]] 记录的年度 target 为「日韩台 15% / SEA 20%」，本次 Product Base 默认给了 SEA 15% — 是产品定价基准与年度 KPI target 双口径并存，还是 SEA 口径下调、需同步更新 Jaccy 卡？
- **Americas 归入 Europe 12%**：Jerry 未单独提 Americas，暂按 [[Jasmin]]「欧洲+美洲」同一条线套 Europe 12% — 若美洲要单独基准请补一句

## 10. 建表进度（2026-07-18 Claude 经 Chrome 实建于 Jerry 提供的 Base）

Base: `WEBUY Product Base`（https://x5mcu0hena.sg.larksuite.com/base/WcsIbxs1CakUK9sWxjDlvWMfg2d）

| 表 | 状态 | 说明 |
|---|---|---|
| Products | ✅ 完成 15 字段 | 含 Quotes/Price_Rules 自动反向关联；ProductSpec Link / Sales Kit Link 暂为 Text（贴 URL 即可）；Main Airline 关联未建（可经 Departures→Air_Blocks 达） |
| Suppliers | ✅ 完成 7 字段 | |
| Quotes | ✅ 完成 14 字段 | |
| Quote_Lines | ✅ 完成 9 字段 | |
| Air_Blocks | ✅ 完成 13 字段 | Base Fare 与 Airport Tax & Fuel 已拆列 |
| Price_Rules | ✅ 完成 12 字段 | |
| FX_Rates | ✅ 完成 5 字段 | |
| Departures | ✅ 结构字段 25/29 完成（2026-07-19 续建）：Tour Code / Product / 日期×2 / Air Block / Land Quote Line / Season（4 档）/ Group Size / Min Pax / FX Rate / Air·Land Cost SGD / 杂费 5 列 / 5 价格档 / Seats Sold / Status（7 态）/ Skybear Synced / Last Sync / Sync Diff | **仅剩 4 个公式列**：Total Cost SGD（=Air+Land+杂费5列）、Suggested Price（=Cost÷(1−Target Margin%)向上取整尾88）、Margin Pct（=(Adult−Cost)÷Adult）、Margin Flag（=Margin<Target→🔴）。公式编辑器已试开，Lark Formula editor 支持字段名自动补全，手工补约 10 分钟 |

其余待办：§6 的 7 个视图、权限设置（Planner 可写/销售只读）、数字列货币格式微调。

## 相关内容

- [[2026-07-17_Planner_Workflow_AI_Architecture_v0.1]] — 总架构（本表是 P0 地基）
- [[Lark_Costing_Sheet_2026]] — 前身，中国线迁移数据源
- [[Skybear]] · [[webuy-data]] · [[webuy-itinerary]]
