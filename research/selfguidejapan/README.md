# Self-Guided Japan（selfguidejapan.com）线路与景点整理

> 抓取日期：2026-10-07 · 来源站点：https://selfguidejapan.com（BluePlanet「Self-Guided Japan」，自助游套餐：酒店 + 新干线 + 行李托运 + 机场接站 + 24/7 支援，不含国际机票）
> 用途：A1 市场雷达 / 日本线产品立项参考。**私有仓库内部资料。**

## 文件

| 文件 | 内容 |
|---|---|
| `tours_catalog.md` / `.csv` | 线路目录：88 条（代码 / 名称 EN+CN / 天数 / 住宿骨架 / 价格 / 主题 / 可信度 / URL），按系列分组 |
| `package_tours.md` / `.json` | **标准行程（Package Tour 格式）**：每条线路一节，house grammar（`CITY_EN 中文 (2N)`、`>` 陆路 / `✈` 航班），有逐日表的 9 条附 Day-by-Day |
| `merged_itineraries.md` / `.json` | **行程归并**：88 条线路 → 15 个「标准行程家族」，每家族给标准骨架、价格带、成员变体差异、家族景点池 |
| `attractions.md` / `.csv` | 景点列表：257 个景点/体验（EN / 中文 / 城市 / 区域 / 类别 / 出现线路） |
| `attractions_by_city.md` / `.csv` | **可选景点池**：按区域 → 城市分组，每个景点带 tag（类别、线路数、核心/常见/可选、家族） |
| `raw/` | 子任务原始抓取 JSON（按系列）+ 目的地页景点 JSON，可追溯每个字段来源 |
| `build/` | 生成脚本：`consolidate.py`（汇总）、`build_families.py`（归并 + tag）、`geo.py` / `names.py`（中英对照表） |

## 覆盖情况

| 项 | 数量 |
|---|---|
| 站点自称线路数 | 111（/tours 页）～113（博客） |
| 本次确认存在的线路 | **88** |
| 其中拿到完整住宿骨架（城市 + 夜数） | 67 |
| 其中拿到逐日行程 | **9**（BF001, BF002, FG005, GR002, KA003, KY003, LX001, LX002, LX003） |
| 来源可信度 | high 13 / low 27 / medium 48 |
| 景点 / 体验 | 257（核心 ≥3 条线路 25 个，常见 2 条 27 个），覆盖 78 个城市/地点 |

系列分布：BF 5 · FG 5 · GR 18 · HD 2 · HK 8 · HS 3 · KA 3 · KM 4 · KR 1 · KY 5 · LX 3 · NT 9 · SE 5 · SK 5 · SL 6 · TP 6

- 探测过、判定不存在：HS004, HS005, HS006, HS101, HS102, HS103, LX004, LX005, SE006, SE101, SE102, SE103, SL002, SL006, SL008, SL009, SL010
- 探测过一次未命中、未二次确认（倾向不存在）：BF006, BF007, BF008, BF101, BF102, BF103, BF104, BF105, BF106, FG006, FG007, FG008, FG101, FG102, FG103, FG104, FG105, FG106, GR011, GR012, GR109, GR110, GR111, GR112, HD003, HD004, HD005, HD006, HK009, HK010, KA004, KA005, KA006, KA101, KA102, KA103, KA104, KY006, KY101, KY102, KY103, KY104, NT001, NT003, NT010, SL101, SL102, SL104, SL105, SL106, SL107, SL108, SL109, SL110, TP005, TP006, TP103, TP104, TP105, TP106

## 方法与限制（必读）

1. **域名被本云端环境的出站网络策略拦截**（代理对 CONNECT 返回 403，WebFetch 报 EGRESS_BLOCKED），所以**没有直接读取任何网页**。
2. 全部数据来自 WebSearch 的**搜索索引摘要**（限定 `selfguidejapan.com` 域）：9 个并行子任务按系列逐代码搜索 `/tours/<CODE>`，只记录明确归属到该代码页面的信息；交叉来源（博客、主题页）在 `raw/*.json` 的 `sources` / `notes` 里标明。
3. 搜索额度为每轮 200 次（子任务共用），本轮在第一遍「存在性 + 名称/天数/价格/城市」之后耗尽，**第二遍逐日行程大多未执行**。因此：
   - `package_tours.md` 里「逐日行程未能取得」= 来源未给出，**不是**该线路没有行程；
   - 搜索摘要由小模型生成，存在**代码↔名称串标**（已知冲突：SL003 页面标题显示「SOLO/Timeless Traditions」但博客称其为「SOLO Koyasan」；GR005/GR006、SE003/SE004、KM001/KM002、KY004/KY005 的名称/价格在不同摘要间互换），冲突均写入 `notes` 并标 `low`。
4. 价格：站点标价，每人、两人一房、不含国际机票；SOLO 系列为单人单房价；SL103 为澳元。
5. 中文名为本仓库整理时的译名（线路名意译；景点用通用中文名），非站点官方译名。

## 补全路径

- **方案 A（推荐）**：在云端环境设置 → Network access 里放行 `selfguidejapan.com`（以及 `japan-navi-journey.com`），之后可直接抓取 111 条线路的完整逐日行程、酒店、含项，并复用 `build/` 脚本重新生成全部文件。
- **方案 B**：不放行域名，下一轮对话继续用搜索补第二遍（约 150 次搜索，可补齐大部分逐日骨架，但精度仍受摘要限制）。

## 待办

- [ ] japan-navi-journey.com 同格式整理（域名同样被拦截；等放行或下一轮搜索额度）
- [ ] 两站行程对比归并（`merged_itineraries.md` 目前只含 selfguidejapan；第二站数据到位后合并家族并补齐景点池）
