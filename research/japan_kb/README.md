# japan_kb：生成行程用的日本线知识包

由 `research/build/build_kb.py` 从两站整理结果生成（2026-10-07）。全部为机器可读 JSON，供 A5 行程生成与 A2 立项检索使用。

| 文件 | 内容 | 条数 |
|---|---|---|
| `families.json` | 22 个标准行程家族：骨架（城市+夜数）、天数带、USD 价格带、成员线路、主题、覆盖城市、归并说明 | 22 |
| `tours.json` | 121 条在售线路紧凑版：route、逐日（城市/交通/景点/含餐）、酒店、含项、价格 | 121 |
| `city_graph.json` | 城市节点（中文、区域、典型夜数、过夜线路数）+ 交通边（出现次数、模式、示例线路） | 110 节点 / 244 边 |
| `attractions.json` | 景点池：城市、类别、核心/常见/可选、出现线路、家族、来源站 | 596 |
| `hotels.json` | 分城市分档（standard / deluxe / onsen plan / family）酒店名 | 89 城 |
| `stats.json` | 节奏先验：每天景点数分布、天数→城市数、1 晚停留占比、移动日占比、常见首站 | — |
| `seasons.json` | 硬日期约束（雪猴、立山、睡魔祭、樱花、滑雪、世博闭幕等） | 12 |

校验器标定：把 121 条真实线路转成 ItinerarySpec 跑一遍，报错的只剩站点数据本身不一致的几条（如酒店夜数与天数不符、酒店表顺序与行程顺序不同），其余全部通过；篡改样本能抓出跨区域景点、城市序列错位、密度超标、季节封闭等问题。

配套脚本（`research/build/`）：
- `retrieve.py`：简报 → 候选家族与参考线路（规则打分，无需模型）
- `validate_itinerary.py`：ItinerarySpec 校验器（夜数、路线边、景点归属、密度、季节、机场、价格带），可作库函数 `validate_spec()` 调用
- `generate_itinerary.py`：全自动驱动（检索 → Claude 结构化输出 → 校验 → 修复循环），`--dry-run` 不调用模型
- `tourspec.schema.json`：生成目标 schema

使用方式见 `research/itinerary_skill/SKILL.md`（Claude）与 `prompt_chatgpt.md`（ChatGPT）。

## 口径说明
- 价格为站点标价（每人、两人一房、不含国际机票；JNJ 为日元参考价），只作对标。
- 节奏统计以自助游为主，跟团大巴可更密；建议把 WEBUY 自家历史行程按同一 schema 导入后重算。
- 交通边表示「有在售产品这样走过」，不含用时；景点无坐标与开放时间。
