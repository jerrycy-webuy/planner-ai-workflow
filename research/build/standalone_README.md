# Japan Tour Planner

用真实在售线路做底稿，让 AI 生成**合理、可售、可报价**的日本行程。

- **知识库**：121 条在售线路（selfguidejapan.com 110 条自助游套餐 + japan-navi-journey.com 11 条私人定制团）→ 22 个标准行程家族、城市交通图、596 个按城市打 tag 的景点、分档酒店、季节硬约束、节奏统计先验
- **脚本**：抓取解析 → 汇总 → 家族归并 → 知识包；简报检索器；确定性校验器（用 121 条真实线路标定）；Claude 生成驱动（检索 → 结构化输出 → 校验 → 修复循环）
- **skill**：Claude Cowork 版 SKILL.md 与 ChatGPT 版提示词，输入立项简报，输出 ItinerarySpec JSON + 双语逐日表

> 数据抓取日期 2026-10-07。价格为站点标价（每人、两人一房、不含国际机票；JNJ 为日元参考价），只作对标。中文名为整理时译名。**内部资料，请勿外传。**

## 目录

```
kb/                      生成行程用知识包（JSON）：families / tours / city_graph / attractions / hotels / stats / seasons
skill/                   SKILL.md（Claude）· prompt_chatgpt.md · examples/（示例简报、模型看到的知识上下文样例）
scripts/                 scrape_sgj.py · scrape_jnj.py · consolidate.py · build_families.py · build_kb.py
                         retrieve.py · validate_itinerary.py · generate_itinerary.py · tourspec.schema.json
data/selfguidejapan/     110 条线路目录 / 标准行程 / 景点列表 + raw/
data/japan-navi-journey/ 11 条行程目录 / 标准行程 / 景点列表 + raw/
data/merged/             22 个行程家族归并 · 596 个景点按区域→城市 tag
```

## 快速开始

```bash
# 1 简报 → 候选家族与参考线路（无需模型）
python3 -I scripts/retrieve.py --days 10 --entry "Tokyo (HND)" --exit "Osaka (KIX)" --themes "world heritage,onsen" --cities "Takayama,Kyoto"

# 2 校验一份行程 JSON（schema 见 scripts/tourspec.schema.json）
python3 -I scripts/validate_itinerary.py spec.json --tour-type group_coach --month 11

# 3 全自动生成（需 pip install anthropic 与凭证；--dry-run 只组装提示词）
python3 scripts/generate_itinerary.py --brief skill/examples/brief_example.json --out out/ --dry-run
```

在 Claude Cowork 里使用：把 `skill/` 作为 skill 目录，按 `skill/SKILL.md` 的六步执行（选家族底稿 → 增删节点 → 填景点酒店 → 输出 JSON 与逐日表 → 跑校验器 → 交付）。ChatGPT 用 `skill/prompt_chatgpt.md`，附件上传 `kb/*.json`。

## 校验器检查什么

夜数合计、相邻城市是否在真实线路中出现过、景点是否属于当天城市（按真实线路出现城市，跨区域才报错，同区域提示为一日游）、每日景点密度、1 晚停留占比、季节封闭（滑雪、立山、睡魔祭、世博闭幕等）、进出机场与首末站、价格带对标。121 条真实线路回归：仅 6 条报错且均为站点数据自身不一致。

## 重新生成知识库

```bash
# 下载页面（需网络），然后：
python3 -I scripts/scrape_sgj.py <fetch_sgj> <raw_sgj>
python3 -I scripts/scrape_jnj.py <fetch_jnj> <raw_jnj>
python3 -I scripts/consolidate.py <raw_sgj> <out_sgj> selfguidejapan.com
python3 -I scripts/consolidate.py <raw_jnj> <out_jnj> japan-navi-journey.com
python3 -I scripts/build_families.py <out_merged> <out_sgj> <out_jnj>
python3 -I scripts/build_kb.py <out_merged> <out_sgj> <out_jnj> kb
```
家族定义在 `scripts/families_def.py`，中英对照在 `scripts/names.py` / `scripts/geo.py`。

## 已知局限与下一步

- 知识库按自助游与私人定制产品校准，跟团大巴可更密：建议把自家历史行程按同一 schema 导入后重算 `kb/stats.json`。
- 交通边只有「出现过」没有用时；景点无坐标与开放时间；季节表为人工 12 条。
- 来源：WEBUY Planner 工作流 AI 化项目（planner-ai-workflow）的 A5 行程生成模块。
