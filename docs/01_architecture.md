---
type: note
status: draft
created: 2026-07-17
updated: 2026-07-17
source: Claude
owner: [Jerry]
bu: [WEBUY_SG, ALTITUDE, WETRIP, Group]
tags: [Planner, Workflow, AI, Architecture, Skybear, Costing, Product]
confidence: high
last_reviewed: 2026-07-17
---

# Planner 工作流 AI 化架构方案 v0.1

> 基于 2026-07-17 [[Jerry]] 六轮访谈拆解。目标：把 Planner（[[Bernice]] / [[Jasmin]] / [[Dorothy]] / [[Jaccy]] / [[Leen]]）从构思到上架到培训的全链路拆成可 AI 化的动作，让 Planner 更快完成工作，服务各自区域的 sales + margin 目标。

---

## 1. 访谈确认的事实基线（2026-07-17 Jerry 口径）

| # | 问题 | Jerry 确认 |
|---|---|---|
| 1 | 立项决策 | Planner 自主决定，无正式审批 |
| 2 | 洞察信息源 | 竞品官网价格 / 销售一线反馈 / 供应商与行业推介（**未用 Skybear 自有销售数据 — 机会点**） |
| 3 | 对外沟通渠道 | Email + WhatsApp/微信 |
| 4 | 最痛环节（优先 AI 化） | ① 成本核算+定价 ② Skybear 上架配置 ③ 行程文件+文案培训（地接询价**不是**最痛） |
| 5 | Costing 工具现状 | 各 Planner 自己的 Excel，格式不统一 |
| 6 | 定价逻辑 | 目标毛利率倒推 + 竞品对标；**无需审批** |
| 7 | 价格矩阵复杂度 | 出发日期多、档位也多（早鸟/促销/会员等叠加），维护量大 |
| 8 | Costing 具体痛点 | 地接报价转录 / 多日期摊算重复劳动 / 变动（汇率、燃油、地接涨价）重算 |
| 9 | Skybear 建产品 | 后台 UI 逐字段手填 |
| 10 | Tour Code 改价 | 逐个手填、**频繁改** |
| 11 | 前台关系 | **Skybear 即 CMS**：Package Content 在 Skybear 填，webuytravel.sg 直接读 |
| 12 | 上架端到端耗时 | 1–2 天 |
| 13 | 行程文件源头 | 地接社行程（多中文）为底稿，Planner 改写双语+加卖点 |
| 14 | 文案/培训现状 | Lark 群发图文 + 培训 session + 卖点卡/FAQ 文档，三样都在做 |
| 15 | 航司环节 | 看区域混合（自谈 series / 票务协助 / 票代报价） |
| 16 | 上线后运营 | 纳入 AI 化范围，但**低优先** |
| 17 | Skybear 写入通道 | **推动 IT 开写 API**（token/接口找 Vincent 一线） |
| 18 | 地接报价格式 | Excel 报价表 + Word/PDF 行程带报价（无需 OCR IM 截图） |
| 19 | 使用入口 | **Planner 自己用 Claude+Skill 或 ChatGPT+Skill**，已有账号，自己跑自己的产品 |
| 20 | Costing 收敛 | 愿意统一新模板，载体选 **Lark 多维表格** |
| 21 | 品牌定位含义 | BU 定位硬约束（[[WEBUY_SG]] mass / [[ALTITUDE]] 高端轻奢 / [[WETRIP]] 入境中国） |
| 22 | 销售弹药沉淀 | 统一 Lark 知识库（同步一份进 vault `30_Sales_Knowledge/`） |
| 23 | 上新节奏 | 看季节批量（如 [[NATAS]] 前集中上新，平时以维护为主）→ 架构要扛峰值批量 |

---

## 2. Planner 工作流全景 — 每步 Input / Output / Goal

```
①洞察 → ②构思立项 → ③航司谈判 → ④地接询价 → ⑤成本定价 → ⑥行程文件
                                                      ↓
        ⑨在售运营 ← ⑧文案+培训 ← ⑦Skybear 上架（Tour Type + Tour Code 价格 + Package Content）
```

| 步骤 | Input | Output | Goal | AI 化动作 |
|---|---|---|---|---|
| ① 市场趋势洞察 | 竞品官网价格、销售反馈、供应商推介、（补：Skybear 自有销售/lost deal） | 区域机会判断（补货架/调价/新线） | 找到能卖、有毛利的方向 | **A1 市场雷达** |
| ② 构思立项 | ①的机会 + BU 定位约束 + 航线可行性 | 产品概念（目的地/天数/目标价带/预期 margin） | 立一个值得做的产品 | **A2 立项一页纸** |
| ③ 航司谈判 | 班期需求、目标成本 | series fare / 票代价 + 班期 + 出票条款 | 锁定有竞争力的机票成本和班期 | A3 辅助（邮件起草/条款提取/比价记录） |
| ④ 地接询价 | 行程需求单 | 各家报价（Excel / Word / PDF） | 拿到最优地接成本和行程执行方案 | **A3 报价转录官**（转录+比价+漏项检查） |
| ⑤ 成本核算+定价 | 机票价 + 地接价 + 汇率 + 杂费 + 目标 margin + 竞品对标价 | 每出发日期成本 + 各档售价矩阵 | 每个日期每个档位都算对、达标 margin | **A4 Costing 引擎** |
| ⑥ 行程文件 | 地接中文行程底稿 + 照片 | 双语行程 PDF（电子版+印刷版） | 客户可看、销售可发、可印刷 | **A5 Itinerary Studio**（[[webuy-itinerary]] skill，v3 提案在案） |
| ⑦ Skybear 上架 | ⑤价格矩阵 + ⑥行程内容 + 图文素材 | Tour Type + 全部 Tour Code 价格 + Package Content（= webuytravel.sg 前台可见） | 上架快、字段准、改价不漏 | **A6 Skybear 发布器** |
| ⑧ 文案+培训 | ProductSpec + costing + 竞品对标 | Lark 群发图文 + 卖点卡/FAQ/异议话术 + 培训材料 | 上架当天销售有弹药、会卖 | **A7 销售弹药生成器** |
| ⑨ 在售运营 | 收客进度、竞品价差、毛利实况 | 砍班/加班/调价/复盘决策 | 收客率和毛利守住 target | **A8 在售驾驶舱**（低优先） |

---

## 3. 架构核心：一份产品主数据，处处渲染

**ProductSpec = 唯一事实源**（沿用 [[2026-07-17_Itinerary_Skill_v3_Redesign_Proposal]] 的 TourSpec 思路，扩展价格与卖点）：

```
Lark Product Base（多维表格，全区域统一）
├── Products 表      Tour Type 级：代码/BU/目的地/天数/定位/状态
├── Departures 表    Tour Code 级：出发日期 × 成本构成 × 各档售价 × margin
├── Quotes 表        地接/航司报价：供应商 × 报价版本 × 有效期
└── Suppliers 表     地接社/航司/票代档案

ProductSpec（每产品一份结构化档案，存 Lark/文件均可）
= 行程（days/hotels/meals）+ 价格矩阵引用 + 卖点/USP + 素材（照片/地图）

下游全部从 ProductSpec + Lark Base 渲染，不再各处手抄：
→ 行程 PDF（A5）   → Skybear 字段（A6）   → 文案三件套（A7）   → 培训材料（A7）
```

**原则**：Planner 改数据只改一处（Lark Base / ProductSpec），所有产物重新渲染即得。这直接消灭「变动重算」和「多处手抄不一致」两大痛点。

## 4. 八个 AI 动作详述

### A1 市场雷达（升级已有周扫描）
- **现状**：[[2026-07-13_Competitor_Price_Scan]] 已每周抓 5 家竞对 vs Skybear（440 匹配 / 1481 gap）。
- **升级**：① 按 Planner 区域切分订阅，推送到 Lark（Jaccy 只看 Asia、Jasmin 只看欧美…）；② 接入 Skybear 自有数据（`order_sales_view` / `lost_deal_analysis`，走 [[webuy-data]]）——目前 Planner 完全没在用自己家的销售数据；③ 销售一线反馈半自动汇集（销售群/Respond.io 摘要进 `00_Inbox/Sales_Feedback/`）。
- **Output**：每周一早（配合 [[Product_Committee]] 例会）每人一份区域机会简报：补货架机会 / 该调价产品 / 竞品新动作。

### A2 立项一页纸
- Planner 给一句话方向 → AI 拉竞品同类价格带 + Skybear 历史同区域销售 + BU 定位校验 → 产出立项 brief（目的地/天数/目标价带/预期 margin/竞品对比表）。
- 低优先（立项本身不痛），作为 skill 内一个子命令即可。

### A3 报价转录官
- **Input**：地接社 Excel 报价表 / Word/PDF 行程带报价（各家模板不同）。
- **动作**：解析 → 归一化写入 Lark Quotes 表 → 输出：① 与需求单的差异清单（漏报项、单房差、自费项、不含项）② 多家比价表 ③ 待砍价点提示。
- **Goal**：消灭人工转录；比价从「肉眼对 Excel」变成「看一张归一化表」。
- 附带：航司报价/条款同样入 Quotes 表（邮件贴进来即可），沉淀历史价格供下次谈判对标。

### A4 Costing 引擎（最痛，P0）
- **载体**：统一 Lark 多维表格模板（对齐并升级 [[Lark_Costing_Sheet_2026]] 思路，全区域一套结构；2026-07-17 [[Jerry]] 拍板：**Jerry 先定稿直接发布，用中迭代**，不开全员工作坊）。
- **能力**：
  1. 从 Quotes 表带入地接/机票成本，按出发日期自动摊算全部 Tour Code；
  2. 售价 = 成本 ÷ (1−目标 margin) 倒推 + 竞品对标价并排显示（接 A1 数据），Planner 只做最后判断；
  3. 档位矩阵（成人/儿童/单房差/早鸟/促销）一次定义规则、全日期生成；
  4. **变动重算**：改任一成本字段（汇率/燃油/地接涨价）→ 全日期重算 + 输出影响清单（哪些日期 margin 跌破 target 红旗，如日韩台 15% / SEA 20%）；
  5. 低毛利防线：margin 低于 BU target 自动标红（吸取 Costing Sheet 312 低毛利行教训）。
- **Goal**：多日期摊算和变动重算零手工、口径统一、错不过夜。

### A5 Itinerary Studio
- 即 [[webuy-itinerary]] skill，按 [[2026-07-17_Itinerary_Skill_v3_Redesign_Proposal]] 落地：地接中文行程 → TourSpec → 双语 PDF（电子版 + 印刷版），Proof 可编辑校样。
- 本方案不重复展开，只定关系：**TourSpec 并入 ProductSpec 体系**，行程数据同时供 A6（Package Content 逐日行程）和 A7（文案素材）复用。

### A6 Skybear 发布器
- **2026-07-17 更新**：[[Cheng_Tai]] 确认 Skybear 写 API **下周（2026-07-20 当周）上线**，A6 直接按 API 版实施，原「填写包」方案降级为 API 覆盖不到字段时的 fallback。
- **能力**：从 ProductSpec + Lark Base 一键：建 Tour Type / 批量 upsert Tour Code 价格 / 上传 Package Content（highlights/逐日行程/T&C）。每次写入前出 **diff 预览**（现价 vs 新价，读现状走 [[webuy-data]]），Planner 确认后执行。
- **Goal**：上架从 1–2 天 → 1 小时内；改价从逐个手填 → 批量一次过；改价频繁不再是负担。
- **API 上线后第一件事**：拿接口文档核对覆盖面（create tour type / 批量改价 / package content / 读接口），并与 Lark Base 字段做映射表（见 [[2026-07-17_Lark_Product_Base_Schema_v0.1]] §7）。

### A7 销售弹药生成器
- **Input**：ProductSpec + costing 卖价 + A1 竞品对标。
- **Output 三件套**（一次生成，同源一致）：
  1. Lark/WhatsApp 群发图文（新品内部推广）；
  2. 卖点卡 + FAQ + 异议处理话术（套用 `80_Templates/Product_Sales_Card_Template.md` / `Objection_Handling_Template.md`，含"vs Chan Brothers 怎么讲"竞品对比话术）；
  3. 培训材料（PPT 大纲 + 讲稿要点）。
- **沉淀**：统一 Lark 知识库（销售自查）+ 同步一份进 vault `30_Sales_Knowledge/`（也为 §15.4 Sales Enablement Agent 攒知识密度）。
- **Goal**：上架当天弹药同步到位，销售不用等、不用问。

### A8 在售驾驶舱（低优先，P2）
- 定时扫 [[webuy-data]]：`seat_availability_view`（收客进度）× `departure_countdown`（起飞倒计时）× margin 实况 × A1 竞品价差变化。
- **Output**：每周每 Planner 一份在售清单：建议砍班/加班/调价/加推的产品，附数据依据；lost deal 摘要供 [[Product_Committee]] 复盘。
- 闭环回 A1，形成「洞察 → 上新 → 在售 → 洞察」循环。

---

## 5. 交付形态与运行位置

| 组件 | 形态 | 运行者 |
|---|---|---|
| A2–A7 | **planner-suite 双平台包**：Claude Skill（Cowork）+ ChatGPT 移植版（GPT/提示词包 + 同一套模板）。**ChatGPT 可用是底线**（2 位 Planner 仅有 ChatGPT），Claude Skill 为功能上限版本 | **各 Planner 自己跑**（账号现状：6 位 Planner 中 4 位同时用 ChatGPT Codex + Claude Cowork，2 位仅 ChatGPT — 2026-07-17 Jerry 口径） |
| A1 / A8 | 定时任务（cron / 周日大整理节奏），产出推 Lark | 中心化跑（Jerry 侧 / JClaw） |
| 数据底座 | Lark Product Base + ProductSpec | 全体共用，Lark OpenAPI 可读写 |
| Skybear 写 API | IT 排期（Vincent） | 服务端 |

设计原则：**数据在 Lark（工具无关、可协作、可监控），智能在 Skill（各家 AI 都能跑），写入走 API（可审计）**。Planner 换 Claude 还是 ChatGPT 都不影响资产沉淀。

## 6. 分期路线（对齐季节批量节奏，目标下一个批量上新窗口前 P0+P1 可用）

| 期 | 内容 | 依赖 |
|---|---|---|
| **P0（2–3 周）** | ① Lark Product Base + 统一 costing 模板设计（**Jerry 定稿直接发，用中迭代**）② A3 报价转录官 ③ A4 Costing 引擎 ④ A6 填写包版 | Jerry 定稿 |
| **P1（+3–4 周）** | ① Skybear 写 API 联调（**Cheng Tai 确认 2026-07-20 当周上线**，上线即对接）② A7 弹药三件套 + Lark 知识库结构 ③ A5 itinerary v3 P0/P1（TourSpec 正式化 + Proof 校样） | API 已确认上线 |
| **P2（后续）** | ① A1 市场雷达升级（分区订阅 + 自有销售数据接入）② A8 在售驾驶舱 ③ itinerary v3 P2（视觉对齐成品） | P0/P1 数据沉淀 |

**优先级依据**：Jerry 痛点排序（成本定价 > 上架 > 文案培训）+ 地接询价不痛只做转录不做谈判 + 上线后运营纳入但殿后。

## 7. 决策记录（2026-07-17 Jerry 逐项拍板）

- [x] **模板定稿方式** → 不开工作坊：Jerry + Claude 先把表结构定稿，直接发给 Planner 用，用中迭代
- [x] **Skybear 写 API** → 走 **IT 条线**；**2026-07-17 更新：[[Cheng_Tai]] 已确认下周（2026-07-20 当周）上线写 API**，无需另行提需求单。A6 直接对接正式 API，「填写包」降级为 API 覆盖不到字段时的 fallback。API 上线后需核对覆盖面：建 Tour Type / 批量 upsert Tour Code 价格 / Package Content 上传 / 读接口（diff 预览）
- [x] **统一 Lark 销售知识库** → 建在 **Group Commercial 空间**，Planner 可写、全体销售**只读**，口径由 Product 线把控
- [x] **Planner AI 账号现状** → **6 位 Planner：4 位同时用 ChatGPT Codex + Claude Cowork，2 位仅 ChatGPT** → 交付定为双平台，ChatGPT 可用为底线
- [x] **A1 分区周报去向** → **先独立推送试运行 3–4 周**，看质量和使用情况再决定是否挂进 [[Product_Committee]] 周一例会

## 7.1 新增待确认

- ~~第 6 位 Planner 是谁~~ → **2026-07-17 已确认：[[Xinmei]] 由 OP 升职为 Junior Planner + OP**，Planner 团队 6 人；Xinmei 的区域 / target / 汇报线细节见其实体卡待确认项
- **仅有 ChatGPT 的 2 位是谁**：决定双平台铺设顺序和培训安排

## 相关内容

- [[2026-07-17_Itinerary_Skill_v3_Redesign_Proposal]] — A5 详细设计
- [[2026-07-13_Competitor_Price_Scan]]（60_Reports/Weekly/）— A1 现状基线
- [[Lark_Costing_Sheet_2026]] — A4 前身参照
- [[webuy-data]] · [[Skybear]] · [[Product_Committee]] · [[Commercial_Platform]]
