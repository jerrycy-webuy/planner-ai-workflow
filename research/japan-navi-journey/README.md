# Japan Navi Journey（japan-navi-journey.com）线路与景点整理

> 抓取日期：2026-10-07 · 来源：https://japan-navi-journey.com（Japan Navi 集团的高端定制品牌，集团创立于新加坡、团队驻日本各地；产品为**私人定制团**：私家车 + 司机 + 英语导游 + 精选酒店/旅馆，按询价，不公开标价）
> 用途：A1 市场雷达 / 日本线产品立项参考。**私有仓库内部资料。** 两站合并结果见 `../japan_merged/`。

## 文件

| 文件 | 内容 |
|---|---|
| `tours_catalog.md` / `.csv` | Sample Itinerary 目录：12 条（索引页列 11 条 + 任务给定的睡魔祭 1 条） |
| `package_tours.md` / `.json` | 标准行程（与 selfguidejapan 同格式），7 条完整逐日 |
| `attractions.md` / `.csv` | 景点列表：242 个（来自行程页 + `/column/` 目的地攻略文章） |
| `raw/` | 原始抓取 JSON：`jnj_itineraries.json`（行程）、`jnj_destinations.json`（24 个目的地、159 个景点） |

## 覆盖情况

| 项 | 数量 |
|---|---|
| 站点索引页列出的行程 | 11 |
| 本次记录的行程 | **12**（含睡魔祭专线，页面未能验证） |
| 其中完整逐日行程 | **7**（AICHI-NAGOYA-CHITA, AOMORI-UNVEILED, DISCOVER-FUKUOKA, NAGANO-PREMIUM-RETREAT, OSAKA-5DAYS, PREMIUM-TOHOKU-GOURMET-TOUR, SADO-ISLAND） |
| 详情页未被搜索引擎收录、只有索引标题 | 4（津轻温泉 3 天、东京&东北树冰 10 天、栃木 4 天、东信州 5 天） |
| 来源可信度 | high 5 / low 5 / medium 2 |
| 景点 / 体验 | 242，覆盖 68 个城市/地点 |

区域分布：青森·东北 5 条、长野 2 条、福冈 1、爱知·知多 1、新潟佐渡 1、大阪 1、栃木 1。**与 selfguidejapan 几乎不重叠**（对方无东北、长野深度、佐渡、栃木线路），互补性强。

备注：osaka-5days 页面标题已由「Expo 2025 & The Soul of Osaka」改为「Discover Osaka: City Adventures, Skyline Views and Cultural Experiences」（世博结束后改题），两者均记录。仅 premium-tohoku-gourmet-tour 给出住宿参考价（下北旅馆 3–5 万日元/晚、普贤院宿坊 4–6 万、ReLabo Aomori 6 万）。

## 方法与限制（必读）

1. **两个域名都被本云端环境的出站网络策略拦截**（代理对 CONNECT 返回 403，WebFetch 报 EGRESS_BLOCKED），所以**没有直接读取任何网页**。
2. 全部数据来自 WebSearch 的**搜索索引摘要**（限定域名），由并行子任务逐线路搜索；只记录明确归属到该线路页面的信息，交叉来源（博客、主题页）在 `raw/*.json` 的 `sources` / `notes` 里标明。
3. 搜索额度每轮 200 次（子任务共用）。两轮共约 390 次：第一轮做存在性 + 名称/天数/价格/住宿骨架，第二轮补逐日行程。**没有被搜索引擎索引的产品页无法再通过搜索补齐**，剩余逐日空缺只能靠放行域名后直接抓取。
4. 搜索摘要由小模型生成，存在**代码↔名称串标**；冲突均写入 `notes` 并标 `low`。
5. 中文名为本仓库整理时的译名（线路名意译；景点用通用中文名），非站点官方译名。

## 补全路径

放行 `japan-navi-journey.com` 后直接抓取 `/itinerary/` 全部详情页（含 4 条未索引页）与 `/column/` 全部文章，再用 `../build/` 脚本重新生成。
