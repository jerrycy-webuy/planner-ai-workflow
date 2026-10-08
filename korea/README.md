# Korea Tour Planner（韩国线行程知识库）

按 [Japan-Tour-Planner](https://github.com/webuytravel/Japan-Tour-Planner) 的同一套方法做的韩国版：用真实在售线路做底稿，让 AI 生成**合理、可售、可报价**的韩国行程。

- **知识库**：53 条在售线路（新加坡 Chan Brothers 31 条、EU Holidays 7 条、Dynasty Travel 9 条 + 首尔地接 KoreaTravelEasy 6 条多日团）→ 14 个标准行程家族、城市交通图（27 个过夜城市 / 48 条边 / 96 组一日游可达关系）、359 个按城市打 tag 的景点（核心 87 · 常见 84 · 可选 188）、分档酒店、19 条季节/节庆约束、节奏统计先验（含购物站占比）
- **脚本**：解析 → 统一线路 JSON → 家族归并 → 知识包；简报检索器；确定性校验器（用 48 条有住宿的真实线路回归）；Claude 生成驱动
- **skill**：Claude 版 SKILL.md 与 ChatGPT 版提示词，输入立项简报，输出 ItinerarySpec JSON + 双语逐日表
- **地接填写模板**：见仓库根目录 [`dmc_templates/`](../dmc_templates/)（韩国版按本知识库预填酒店、景点、路段、季节）

> 数据抓取日期 2026-10-08。新加坡三站价格为站点标价（每人、两人一房、含新加坡往返机票，税燃另计），USD 按 1 SGD = 0.78 USD 折算；KTE 为首尔出发地接拼团价（不含国际机票）。只作对标。中文名为整理时的通用译名。**内部资料。**

## 和日本版的差异

| 项 | 日本版 | 韩国版 |
|---|---|---|
| 数据源 | 日本自助游 / 私人定制站（SGJ、JNJ） | **新加坡出发跟团为主**（与 WEBUY 同市场的直接竞品）+ 首尔地接拼团 |
| 景点抽取 | 站点结构化「推荐景点」 | 自建韩国景点词典 `scripts/names_kr.py`（360 条正则 → 标准英文名 / 中文 / 城市 / 类别），从逐日描述抽取 |
| 节奏 | 每日景点 p50 4 / p90 6 | 同为 p50 4 / p90 6，但跟团最多 11（含购物站），**91% 的跟团含购物站** |
| 校验器新增 | — | 红眼航班（Day 1 机上过夜）、**济州/郁陵岛跨海必须写航班或船**、购物站数量、移动日途经景点 |
| 季节 | 12 条 | 19 条（樱花、镇海军港节、赏枫、滑雪、华川冰钓节、牛岛冬季停航等） |

## 目录

```
kb/                      生成行程用知识包（JSON）：families / tours / city_graph / attractions / hotels / stats / seasons
skill/                   SKILL.md（Claude）· prompt_chatgpt.md · examples/（示例简报、篡改样本、模型看到的知识上下文）
scripts/                 parse_sources.py · kte_multiday.py · names_kr.py · geo_kr.py · families_def_kr.py · seasons_kr.py · build_kb_kr.py
                         retrieve.py · validate_itinerary.py · regress_kr.py · generate_itinerary.py · tourspec.schema.json
data/chanbrothers/       31 条线路目录 / 标准行程 / 景点列表 + raw/
data/euholidays/         7 条（含逐出发日期价格矩阵、航班）
data/dynastytravel/      9 条（高端小团）
data/koreatraveleasy/    6 条首尔出发多日拼团
data/merged/             14 个行程家族归并 · 359 个景点按区域→城市 tag
```

## 快速开始

```bash
# 1 简报 → 候选家族与参考线路（无需模型）
python3 -I scripts/retrieve.py --days 8 --entry "Incheon (ICN)" --exit "Incheon (ICN)" --themes "family,heritage" --cities "Jeju,Busan" --season spring

# 2 校验一份行程 JSON（schema 见 scripts/tourspec.schema.json）
python3 -I scripts/validate_itinerary.py skill/examples/spec_bad_example.json --tour-type group_coach --month 7

# 3 回归：用真实线路检查校验器误报
python3 -I scripts/regress_kr.py kb

# 4 全自动生成（需 pip install anthropic 与凭证；--dry-run 只组装提示词）
python3 scripts/generate_itinerary.py --brief skill/examples/brief_example.json --out out/ --dry-run
```

## 14 个行程家族

| ID | 家族 | 骨架 | 成员 |
|---|---|---|---|
| K01 | 首尔 + 京畿深度（跟团） | 首尔 5N 放射 | 5 |
| K02 | 首尔自由行 | 首尔 4N | 5 |
| K03 | 济州 + 首尔 | 济州 2N > 首尔 4N | 4 |
| K04 | 济州 > 釜山 > 首尔（两段内陆航班） | 济州 2N > 釜山 2N > 首尔 2N | 4 |
| K05 | 大韩全景（济州 > 庆尚 > 全州/江原 > 首尔） | 济州 2N > 大邱 1N > 全州 1N > 首尔 2N | 5 |
| K06 | 釜山 + 庆州 + 首尔（南北纵贯） | 釜山 2N > 庆州 1N > 首尔 3N | 4 |
| K07 | 江原道季节线（滑雪/赏花/赏枫）+ 首尔 | 平昌 2N > 首尔 3N | 6 |
| K08 | 全罗道美食慢游 | 全州 2N > 首尔 3N | 4 |
| K09 | 南部海岸（釜山 + 全南/庆南） | 釜山 2N > 丽水 2N > 釜山 3N | 2 |
| K10 | 釜山自由行 | 釜山 3N | 3 |
| K11 | 济州单岛 | 济州 5N | 4 |
| K12 | 韩国环线拼团（首尔地接英文团） | 全州 > 光州 > 釜山 2N > 庆州 > 平昌 | 4 |
| K13 | 忠清道深度 | 大田 2N > 扶余 2N > 首尔 1N | 2 |
| K14 | 东海岸短线（江陵 / 东海 / 郁陵岛） | 江陵 1N | 3 |

完整说明与成员变体见 `data/merged/merged_itineraries.md`。货架空白提示：K09 南部海岸、K13 忠清道、K14 东海岸目前只有高端小团或地接拼团形态。

## 校验器检查什么

夜数合计（支持红眼航班）、相邻城市是否在真实线路中出现过、**景点是否属于当天城市**（以词典城市为准；移动日允许出发城市与途经；同区域提示为一日游，跨区域报错）、每日景点密度、1 晚停留占比、季节约束、进出机场与首末站、**济州/郁陵岛跨海交通**、**购物站数量**、价格带对标。

48 条有住宿的真实线路回归：44 条无 error；剩下 4 条均为站点数据自身问题（同一天写了两套季节方案导致景点数超限、站点漏写济州出岛航班、页头天数与逐日表不一致）。篡改样本（`skill/examples/spec_bad_example.json`）能抓出跨区域景点、济州走陆路、7 月排滑雪与冰钓节、购物站过多。

## 重新生成

```bash
# 下载（需网络）：Chan Brothers 用 https://cms.chanbrothers.com/api/trip-detail/<entity_id>（entity_id 在产品页 __NEXT_DATA__ 里）
#                EU Holidays /tours/<slug>、Dynasty /tour/<slug> 直接 curl（Next.js RSC，解析器自带 RSC 文本块解码）
python3 -I scripts/parse_sources.py <fetch_dir> data      # fetch_dir 下 cb/*.json  eu/*.html  dyn/*.html
python3 -I scripts/build_kb_kr.py data kb
python3 -I scripts/regress_kr.py kb
```
家族定义在 `scripts/families_def_kr.py`，景点词典在 `scripts/names_kr.py`，城市表在 `scripts/geo_kr.py`，季节在 `scripts/seasons_kr.py`。KTE 多日团页面排版不规则，结构化结果人工写在 `scripts/kte_multiday.py`。

## 已知局限与下一步

- 新加坡竞品以 8 天跟团为主，自由行与私人定制样本少；台湾 / 马来西亚出发的韩国团未覆盖。
- 景点词典按出现过的景点 + 常识补齐，**未在词典里的景点不会被抽出**（`data/merged` 里看不到）；地接填回模板后应把新景点并入词典。
- 交通边只有「出现过」没有用时（`city_graph.json` 的 `transport_notes_cn` 给了主要路段参考时长）；景点无坐标与开放时间——这两项正好由地接模板的「5 用车交通」「3 景点门票」补齐。
- 竞品价格「From」价为促销价，max 为原价（Chan Brothers）或按出发日期最高价（EU）。
