# -*- coding: utf-8 -*-
"""行程生成驱动：简报 → 检索家族/参考线路 → Claude 结构化输出 ItinerarySpec → 校验 → 修复循环 → 输出 JSON + house grammar 逐日表。
用法:
  python3 generate_itinerary.py --brief brief.json --out out_dir [--model claude-opus-5-5] [--rounds 3] [--dry-run]
brief.json 示例见 ../itinerary_skill/examples/brief_example.json
需要: pip install anthropic ；凭证走 ANTHROPIC_API_KEY 或 `ant auth login`。--dry-run 只组装提示词并打印大小，不调用模型。
"""
import sys, os, re, json, argparse, subprocess, copy, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geo
from validate_itinerary import validate_spec, ckey
KB_DEFAULT = os.path.join(HERE, "..", "japan_kb")
SCHEMA_PATH = os.path.join(HERE, "tourspec.schema.json")

def retrieve(brief, kb, top=3):
    args = [sys.executable, "-I", os.path.join(HERE, "retrieve.py"), "--days", str(brief["days"]), "--entry", brief.get("entry_airport", ""), "--exit", brief.get("exit_airport", ""),
            "--themes", ",".join(brief.get("themes", [])), "--cities", ",".join(brief.get("must_cities", [])), "--season", brief.get("season", "") or "", "--kb", kb, "--top", str(top), "--json"]
    return json.loads(subprocess.run(args, capture_output=True, text=True, check=True).stdout)

def kb_context(brief, cands, kb):
    """只放候选城市相关的知识，控制长度。"""
    graph = json.load(open(os.path.join(kb, "city_graph.json"), encoding="utf-8"))
    attractions = json.load(open(os.path.join(kb, "attractions.json"), encoding="utf-8"))
    hotels = json.load(open(os.path.join(kb, "hotels.json"), encoding="utf-8"))
    stats = json.load(open(os.path.join(kb, "stats.json"), encoding="utf-8"))
    seasons = json.load(open(os.path.join(kb, "seasons.json"), encoding="utf-8"))
    cities = set()
    for c in cands:
        for r in c["references"]:
            for d in r["days_detail"]: cities.add(ckey(d.get("city")))
        for part in c["skeleton"].split(" > "): cities.add(ckey(re.sub(r"\(\d+\)", "", part)))
    for x in brief.get("must_cities", []): cities.add(ckey(x))
    cities.discard(None)
    # 相邻可达
    edges = [e for e in graph["edges"] if e["from"] in cities or e["to"] in cities]
    edge_lines = sorted({f"{e['from']}→{e['to']}（{e['tour_count']} 条线路，{'/'.join(e['modes'].keys())}）" for e in edges})
    node_lines = [f"{n['key']} {n['name_cn'] or ''}：典型 {n['nights_typical']} 晚（{n['nights_min']}–{n['nights_max']}），{n['tour_count']} 条线路过夜" for n in graph["nodes"] if n["key"] in cities]
    spot_lines = []
    for a in sorted(attractions, key=lambda a: (-a["tour_count"], a["name_en"])):
        if a["city_key"] in cities or any(a["city_key"] and a["city_key"] in NEAR for NEAR in []):
            spot_lines.append(f"[{a['city']}] {a['name_en']}｜{a['name_cn']}｜{a['category_cn'] or a['category'] or '-'}｜{a['level']}｜{a['tour_count']} 条线路")
    hotel_lines = [f"{h['city_key']} {h['city_cn'] or ''}：" + "；".join(f"{tier}: {', '.join(names[:4])}" for tier, names in h["tiers"].items()) for h in hotels if h["city_key"] in cities]
    season_lines = [f"{z['name_cn']}：{z['best']}（{z['note']}）" for z in seasons]
    ctx = []
    ctx.append("# 候选家族与参考线路（真实在售产品，骨架可直接复用）\n" + json.dumps([{k: v for k, v in c.items() if k != "references"} for c in cands], ensure_ascii=False, indent=1))
    for c in cands:
        for r in c["references"]:
            ctx.append(f"## 参考线路 {r['code']}｜{r['title_en']}｜{r['days']}D｜USD {r['price_usd'].get('min')}–{r['price_usd'].get('max')}\n路线：{r['route']}\n酒店：{'；'.join(r['hotels'][:6])}\n逐日：\n" +
                       "\n".join(f"D{d['day']} {d['city']}{'（从 ' + d['from'] + '）' if d.get('from') else ''}｜{d.get('transport') or ''}｜{'、'.join(d['attractions'])}｜餐 {d.get('meals') or '-'}" for d in r["days_detail"]))
    ctx.append("# 城市节奏先验\n" + "\n".join(node_lines))
    ctx.append("# 可用交通边（只在这些城市对之间移动；没出现的组合要在 transport 标「需核实」）\n" + "\n".join(edge_lines[:220]))
    ctx.append("# 景点池（[城市] 英文名｜中文｜类别｜等级｜出现线路数；优先用 core/common，optional 作自费或升级项）\n" + "\n".join(spot_lines[:400]))
    ctx.append("# 酒店参考（标准 standard / 豪华 deluxe，“or similar”）\n" + "\n".join(hotel_lines))
    ctx.append("# 季节硬约束\n" + "\n".join(season_lines))
    ctx.append("# 市场节奏统计\n" + json.dumps(stats, ensure_ascii=False))
    return "\n\n".join(ctx)

SYSTEM = """你是 WEBUY 的日本线产品 Planner 助手。任务：根据立项简报，参照知识库里的真实在售线路骨架，产出一条合理、可售、可报价的行程（ItinerarySpec JSON）。

硬规则：
1. 先选一个最接近的家族骨架作为底稿（写入 family / based_on），只做增删节点的改动；不要凭空编路线。
2. 城市之间的移动只用「可用交通边」里出现过的组合；确需新组合时在 transport 写明交通方式并加「需核实」。
3. 每天的景点只能来自当天城市或其一日游范围；优先选等级 core/common；optional 等级的放进 optional（自费/升级）。不在景点池里的景点允许出现，但要在 assumptions_cn 里列出待核实。
4. 节奏：route 夜数合计 = days-1；每天景点建议 4–6 个（市场中位 4、P90 6），硬上限：跟团大巴 8、自助游 8、私人定制 7；移动日 ≤4；1 晚停留占比不超过 40%；主要枢纽（东京/京都/大阪/福冈/札幌）至少 2 晚。
5. 进出机场与首末站一致；最后一天为离境日，stay 为 null。
6. 遵守季节硬约束（滑雪、立山、睡魔祭、樱花、世博已闭幕等）。
7. 酒店用参考表里的名称加 "or similar"，按 BU 定位选档（WEBUY_SG 标准 / ALTITUDE 豪华）。
8. 输出严格符合给定 JSON schema；title_cn 用中文营销名；每天 title_cn 用「城市中文 ｜ 主题」风格；assumptions_cn 写清你做的假设。
"""

def render_md(spec):
    L = [f"## 【{spec.get('code')}】{spec.get('title_en')}", f"**{spec.get('title_cn')}** · {spec.get('days')}天{spec.get('nights')}晚 · 家族 {spec.get('family')} · 参照 {', '.join(spec.get('based_on') or [])}", ""]
    def lab(c):
        cn, _, _ = geo.city_info(c or ""); return f"{(c or '').upper()} {cn}" if cn else (c or "")
    L.append("- **路线**：" + " > ".join(f"{lab(r['city'])} ({r['nights']}N)" for r in spec.get("route", [])))
    L.append(f"- **进出点**：{spec.get('entry_airport')} ✈ 进 · {spec.get('exit_airport')} ✈ 出")
    if spec.get("highlights_cn"): L.append("- **亮点**：" + " ".join("✦ " + h for h in spec["highlights_cn"]))
    if spec.get("inclusions") or spec.get("exclusions"): L.append(f"- **含**：{'、'.join(spec.get('inclusions') or [])} · **不含**：{'、'.join(spec.get('exclusions') or [])}")
    L += ["", "| Day | 路线 | 交通 | 景点 / 活动 | 可选 | 餐 | 住宿 |", "|---|---|---|---|---|---|---|"]
    for d in spec.get("days_detail", []):
        route = f"{lab(d.get('from'))} > {lab(d['city'])}" if d.get("from") and d.get("from") != d.get("city") else lab(d.get("city"))
        L.append(f"| {d['day']} | {route}　{d.get('title_cn') or ''} | {d.get('transport') or ''} | {'、'.join(d.get('attractions') or [])} | {'、'.join(d.get('optional') or [])} | {d.get('meals') or ''} | {lab(d.get('stay')) if d.get('stay') else ''} |")
    if spec.get("assumptions_cn"): L += ["", "**假设 / 待核实**：", *[f"- {a}" for a in spec["assumptions_cn"]]]
    return "\n".join(L)

def api_schema():
    """结构化输出用的 schema：去掉数值约束（校验器负责），保留类型/枚举/required。"""
    sch = json.load(open(SCHEMA_PATH, encoding="utf-8"))
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in o.items() if k not in ("minimum", "maximum", "minItems", "$schema", "title")}
        if isinstance(o, list): return [strip(x) for x in o]
        return o
    return strip(sch)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", required=True); ap.add_argument("--out", required=True); ap.add_argument("--kb", default=KB_DEFAULT)
    ap.add_argument("--model", default="claude-opus-5-5"); ap.add_argument("--rounds", type=int, default=3); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--top", type=int, default=2)
    a = ap.parse_args()
    brief = json.load(open(a.brief, encoding="utf-8"))
    os.makedirs(a.out, exist_ok=True)
    cands = retrieve(brief, a.kb, a.top)
    context = kb_context(brief, cands, a.kb)
    user_msg = "## 立项简报\n" + json.dumps(brief, ensure_ascii=False, indent=1) + "\n\n请输出 ItinerarySpec JSON。"
    open(os.path.join(a.out, "prompt_context.md"), "w", encoding="utf-8").write(context)
    print(f"候选家族：{[c['family'] for c in cands]}；知识上下文 {len(context):,} 字符（约 {len(context)//3:,} tokens）")
    if a.dry_run:
        print("dry-run：未调用模型。上下文已写入 prompt_context.md"); return
    import anthropic
    client = anthropic.Anthropic()
    system = [{"type": "text", "text": SYSTEM}, {"type": "text", "text": "# 知识库\n" + context, "cache_control": {"type": "ephemeral"}}]
    messages = [{"role": "user", "content": user_msg}]
    schema = api_schema()
    spec = None
    for rnd in range(1, a.rounds + 1):
        with client.beta.messages.stream(
            model=a.model, max_tokens=32000, system=system, messages=messages,
            output_config={"format": {"type": "json_schema", "schema": schema}, "effort": "high"},
            betas=["server-side-fallback-2026-07-01"], fallbacks="default",
        ) as stream:
            response = stream.get_final_message()
        if response.stop_reason == "refusal":
            print("模型拒绝了请求（stop_reason=refusal）", getattr(response, "stop_details", None)); sys.exit(2)
        text = next(b.text for b in response.content if b.type == "text")
        spec = json.loads(text)
        errors, warns = validate_spec(spec, a.kb, brief.get("tour_type"), brief.get("travel_month"))
        json.dump(spec, open(os.path.join(a.out, f"spec_round{rnd}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"round {rnd}: error {len(errors)} / warn {len(warns)} · usage in={response.usage.input_tokens} cached={getattr(response.usage, 'cache_read_input_tokens', 0)} out={response.usage.output_tokens}")
        if not errors: break
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": "校验器发现以下问题，请修复后重新输出完整 ItinerarySpec JSON（保持其余内容不变）：\n" + json.dumps({"errors": errors, "warnings": warns}, ensure_ascii=False, indent=1)})
    json.dump(spec, open(os.path.join(a.out, "spec.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(a.out, "itinerary.md"), "w", encoding="utf-8").write(render_md(spec))
    errors, warns = validate_spec(spec, a.kb, brief.get("tour_type"), brief.get("travel_month"))
    open(os.path.join(a.out, "validation.json"), "w", encoding="utf-8").write(json.dumps({"errors": errors, "warnings": warns}, ensure_ascii=False, indent=1))
    print(f"完成：{a.out}/spec.json, itinerary.md；剩余 error {len(errors)} / warn {len(warns)}")

if __name__ == "__main__":
    main()
