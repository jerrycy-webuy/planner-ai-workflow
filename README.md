# Planner AI Workflow

WEBUY Group Commercial · Product 线 Planner 工作流 AI 化项目。

把 Planner 从「市场洞察 → 构思立项 → 航司谈判 → 地接询价 → 成本定价 → 行程文件 → Skybear 上架 → 文案培训 → 在售运营」的全链路拆成可 AI 化的动作，目标是各自区域的 **Sales + Margin**。

**私有仓库** —— 含公司定价口径、组织信息、供应商结构，不对外。

---

## 现状

| 模块 | 状态 |
|---|---|
| 架构设计 v0.1 | ✅ 定稿（6 轮访谈 + 2 轮逐项拍板） |
| Lark Product Base schema | ✅ 定稿（8 项口径全部确认） |
| Lark Base 实建 | 🟡 8 张表已建；7 张字段 100%，Departures 25/29（剩 4 个公式列） |
| planner-suite skill 包 | ⬜ 未开始（A3 / A4 优先） |
| Skybear 写 API 联调 | ⬜ 等 IT 上线后启动 |

## 文档

| 文件 | 内容 |
|---|---|
| [docs/01_architecture.md](docs/01_architecture.md) | 总架构：9 步工作流 Input/Output/Goal + A1–A8 八个 AI 动作 + 分期路线 + 决策记录 |
| [docs/02_lark_product_base_schema.md](docs/02_lark_product_base_schema.md) | Lark Product Base 8 张表字段级设计 + 核心机制 + 视图 + 建表进度 |
| [docs/03_itinerary_skill_v3_proposal.md](docs/03_itinerary_skill_v3_proposal.md) | A5 行程 PDF skill v3 重设计（基于 5 份设计师成品逆向分析） |
| [docs/overview.html](docs/overview.html) | 一页总览（可直接在浏览器打开） |
| [research/](research/) | 竞品/参考站整理（直接抓取）：selfguidejapan.com（110 条自助游线路，全部含逐日/酒店/价格）、japan-navi-journey.com（11 条私人定制行程）、两站合并的 22 个行程家族 + 523 个按城市 tag 的可选景点（`research/japan_merged/`） |

## 架构一句话

**一份产品主数据，处处渲染。**

```
Lark Product Base（8 表）
├── Products      Tour Type 级产品档案
├── Departures    Tour Code 级 · 价格矩阵主战场
├── Quotes ─< Quote_Lines    地接/航司报价
├── Air_Blocks    机票批次（Base Fare 与税燃拆列）
├── Price_Rules   促销档位规则化
├── Suppliers     供应商档案
└── FX_Rates      汇率（变动重算开关）
        ↓ 同一份数据渲染出：
行程 PDF · Skybear API payload · 销售弹药三件套 · 培训材料
```

成本三来源分离（机票 / 地接 / 杂费），Departures 只做引用汇总 —— 改源头一处，所有引用它的出发日期自动重算、毛利红旗立刻显形。

## 八个 AI 动作

| ID | 动作 | 解决什么 | 优先级 |
|---|---|---|---|
| A1 | 市场雷达 | 竞品周扫描按区域推送 + 接入 Skybear 自有销售数据 | P2 |
| A2 | 立项一页纸 | 竞品价带 + 历史销售 + BU 定位校验 | 低 |
| A3 | 报价转录官 | 地接 Excel/Word/PDF 报价 → 归一化 + 漏项检查 + 比价 | **P0** |
| A4 | Costing 引擎 | 毛利倒推 + 多日期自动摊算 + 变动重算 + 低毛利红旗 | **P0** |
| A5 | Itinerary Studio | 中文行程底稿 → 双语 PDF（电子 + 印刷） | P1 |
| A6 | Skybear 发布器 | 一键建 Tour Type / 批量改价 / Package Content（带 diff 预览） | **P0→P1** |
| A7 | 销售弹药生成器 | 群发图文 + 卖点卡/FAQ/异议话术 + 培训材料 | P1 |
| A8 | 在售驾驶舱 | 收客 × 倒计时 × margin × 竞品价差 → 砍班/加班/调价建议 | P2 |

## 交付形态

- **A2–A7**：planner-suite 双平台包 —— Claude Skill + ChatGPT 移植版。**ChatGPT 可用是底线**（6 位 Planner 中 4 位双持 Codex + Cowork，2 位仅 ChatGPT），各 Planner 跑自己区域的产品。
- **A1 / A8**：中心化定时任务，产出推 Lark。
- **数据在 Lark，智能在 Skill，写入走 API** —— Planner 换 Claude 还是 ChatGPT 都不影响资产沉淀。

## 关键口径（2026-07-18 定稿）

- **Target Margin 默认**：China 18% · Europe 12% · Asia（日韩台越）15% · SEA 15% · Exotic 15%；**ALTITUDE = 对应区域基准 + 5pp**
- **建议售价**：`Cost ÷ (1 − Target Margin%)`，向上取整到**尾数 88**
- **汇率**：始终引用最新，成本自动重算 + 红旗；售价 Planner 手填不自动变
- **价格档 5 种**：成人双人房 / 儿童占床 / 儿童不占床 / 单房差 / 三人房
- **Golden Circle 会员价不进 Base**（由销售端/CRM 处理）
- 表名字段名**纯英文**，与 Skybear 后台术语对齐

## 下一步

1. Departures 剩余 4 个公式列（Total Cost / Suggested Price / Margin % / Margin Flag）
2. A3 报价转录官 + A4 Costing 引擎的提示词包
3. Bernice 中国线试点迁移（从 All China Costing Sheet）
4. Skybear 写 API 上线后 A6 联调

## 相关

- 源文档同步自 Obsidian vault `Jerry_AI_Brain/00_Inbox/AI_Capture/`
- Lark Base：WEBUY Product Base
