---
name: planner-itinerary-korea
description: 用韩国线知识包（53 条在售线路骨架、14 个行程家族、城市交通图、359 个带 tag 景点、分档酒店、季节约束、购物站统计）生成合理可售的韩国行程草案（ItinerarySpec JSON + house grammar 逐日表），并用确定性校验器检查节奏、路线、景点归属、济州跨海交通、季节与购物站。用于 A2 立项与 A5 行程文件底稿。
---

# planner-itinerary-korea：从立项简报生成合理的韩国行程

## 输入
一份立项简报（见 `examples/brief_example.json`）：天数、BU、产品形态（group_coach / self_guided / private_custom / join_in_group）、进出机场、出行月份、主题、必含城市/景点、避免项、客群、目标价、是否要纯玩版。

## 流程（必须按顺序）

1. **检索底稿**：
   `python3 -I scripts/retrieve.py --days <N> --entry "<进>" --exit "<出>" --themes "<主题>" --cities "<必含城市>" --season <spring|summer|autumn|winter> --top 2`
   选一个家族作底稿，写进 `family` 与 `based_on`。
2. **只做增删节点**：在底稿骨架上加减城市或调夜数；移动只用 `kb/city_graph.json` 出现过的城市对，新组合在 `transport` 写「需核实」。**济州 / 郁陵岛进出必须写航班（GMP-CJU、CJU-PUS…）或船。**
3. **填逐日**：景点从 `kb/attractions.json` 按当天城市选（移动日可放出发城市或顺路景点），core/common 优先，optional 放进 `optional`。密度建议每天 4–6 个（市场中位 4、P90 6），硬上限跟团 10（含购物站）/ 拼团 8 / 自由行 7，移动日 ≤4。
   - 新加坡出发：Day 1 多为红眼航班（`stay: null`，酒店夜数 = days−2），或夜抵住仁川/金浦；首尔通常放最后 2–3 晚。
   - 购物站：常规版 3 个（人参 / 护肝宝 / 化妆品，市场 91% 跟团含购物站）；纯玩版写明不进。
   - 酒店从 `hotels.json` 选并加 "or similar"：WEBUY_SG 用 group_standard，ALTITUDE 用 premium。
   - 季节看 `seasons.json`（樱花 3 月底–4 月上旬、镇海军港节、赏枫 10 月中–11 月中、滑雪 12–2 月、牛岛 12–3 月常停航改城山日出峰）。
4. **输出** 符合 `scripts/tourspec.schema.json` 的 JSON，再渲染逐日表（`CITY_EN 中文 (2N)`、`>` 陆路、`✈` 航班、只列含餐）。
5. **校验**：`python3 -I scripts/validate_itinerary.py <spec.json> --tour-type <形态> --month <月>`。error 改到零；warn 逐条判断，保留的写进 `assumptions_cn`。
6. **交付**：spec.json + itinerary.md + 校验摘要 + 对标价格带（家族 USD 区间，新加坡竞品价含机票）+ 需要地接报价的项目清单（对应 `dmc_templates` 的「9 行程报价 / 10 逐日行程」）。

## 硬规则
- 景点只能属于当天城市、出发城市（移动日）或一日游范围（校验器内置首尔放射圈、釜山—庆州—蔚山、济州全岛等表）。
- 不在景点池里的景点可以用，但必须列入 `assumptions_cn` 待核实（并提醒地接在模板里补价）。
- 竞品价格只用于对标，定价走 A4 Costing（目标毛利 Asia 15%，建议价尾数 88）。

## 全自动用法
`python3 scripts/generate_itinerary.py --brief brief.json --out out/`：检索 → 结构化输出 → 校验 → 最多 3 轮修复。无凭证时加 `--dry-run` 只生成提示词上下文（样例见 `examples/prompt_context_example.md`）。
