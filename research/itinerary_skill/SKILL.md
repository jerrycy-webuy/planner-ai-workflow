---
name: planner-itinerary
description: 用日本线知识包（121 条在售线路骨架、城市交通图、523 个带 tag 景点、酒店、季节约束）生成合理可售的行程草案（ItinerarySpec JSON + house grammar 逐日表），并用确定性校验器检查节奏、路线、景点归属与季节。用于 A2 立项与 A5 行程文件底稿。
---

# planner-itinerary：从立项简报生成合理行程

## 输入
一份立项简报（见 `examples/brief_example.json`）：天数、BU、产品形态（group_coach / self_guided / private_custom）、进出机场、出行月份、主题、必含城市/景点、避免项、客群、目标价。

## 流程（必须按顺序）

1. **检索底稿**：运行
   `python3 -I research/build/retrieve.py --days <N> --entry "<进>" --exit "<出>" --themes "<主题,逗号分隔>" --cities "<必含城市>" --season <季节> --top 2`
   读结果里的家族骨架、参考线路逐日表、价格带。选一个家族作为底稿，写进 `family` 和 `based_on`。
2. **只做增删节点**：在底稿骨架上加减城市或调整夜数，不要重新发明路线。每一次移动只用 `research/japan_kb/city_graph.json` 里出现过的城市对；新组合要在 `transport` 写「需核实」。
3. **填逐日**：景点从 `research/japan_kb/attractions.json` 里按当天城市选，core/common 优先，optional 放进 `optional`（自费/升级）。密度：每天建议 4–6 个景点（市场中位 4、P90 6），硬上限大巴 8 / 自助 8 / 私人定制 7，移动日 ≤4。酒店从 `hotels.json` 选并加 "or similar"，按 BU 定档。季节看 `seasons.json`。
4. **输出** 一份符合 `research/build/tourspec.schema.json` 的 JSON，再渲染成 house grammar 逐日表（`CITY_EN 中文 (2N)`、`>` 陆路、`✈` 航班、只列含餐）。
5. **校验**：`python3 -I research/build/validate_itinerary.py <spec.json> --tour-type <形态> --month <月>`。有 error 就改到为零；warn 逐条判断，保留的写进 `assumptions_cn`。
6. **交付**：spec.json + itinerary.md + 校验结果摘要 + 对标价格带（家族 USD 区间，换算 SGD 供 A4 参考）。

## 硬规则
- route 夜数合计 = days − 1；最后一天为离境日。
- 主要枢纽（东京/京都/大阪/福冈/札幌）至少 2 晚；1 晚停留占比 ≤ 40%。
- 景点只能属于当天城市或其一日游范围（校验器内置同城/一日游表）。
- 不在景点池里的景点可以用，但必须列入 `assumptions_cn` 待核实。
- 立山 4 月中–11 月、滑雪 12–3 月、睡魔祭 8 月 2–7 日、大阪世博已闭幕，这类硬约束不可违反。
- 不要把竞品价格直接当售价：家族价格带只用于对标，定价走 A4 Costing。

## 输出格式
- `spec.json`：ItinerarySpec（schema 见 build/tourspec.schema.json）
- `itinerary.md`：逐日表 + 亮点 + 含/不含 + 假设清单
- 一段话：选了哪个家族、改了什么、校验结果、还需人工核实什么

## 已知局限
- 知识包按自助游和私人定制产品校准，跟团大巴可以更密；WEBUY 自家历史行程导入后应重算 `stats.json`。
- 交通边只有「出现过」没有用时；景点无坐标与开放时间；这三项是下一步要补的数据。

## 全自动用法（需 Python + anthropic SDK + 凭证）
`python3 research/build/generate_itinerary.py --brief brief.json --out out/` ：检索 → 结构化输出 → 校验 → 最多 3 轮自动修复。无凭证时加 `--dry-run` 只生成提示词上下文。
