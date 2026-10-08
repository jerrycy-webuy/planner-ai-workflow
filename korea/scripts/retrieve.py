# -*- coding: utf-8 -*-
"""简报 → 候选家族与参考线路（规则打分，不用模型）。
用法: python3 -I retrieve.py --days 12 --entry Incheon --exit Incheon --themes "heritage,family" --cities "Jeju,Busan" [--season winter] [--kb dir] [--top 3] [--json]
"""
import sys, os, re, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geo_kr as geo
THEME_SYN = {"heritage": "heritage & culture", "unesco": "heritage & culture", "palace": "heritage & culture", "temple": "heritage & culture", "culture": "heritage & culture",
             "nature": "nature & scenery", "hiking": "nature & scenery", "island": "nature & scenery", "ski": "winter & ski", "snow": "winter & ski", "winter": "winter & ski",
             "sakura": "cherry blossom", "blossom": "cherry blossom", "spring": "cherry blossom", "maple": "autumn foliage", "autumn": "autumn foliage", "fall": "autumn foliage",
             "family": "theme parks & family", "kids": "theme parks & family", "theme park": "theme parks & family", "everland": "theme parks & family", "lotte world": "theme parks & family",
             "shopping": "shopping & city", "city": "shopping & city", "k-pop": "shopping & city", "dmz": "dmz", "cafe": "instagrammable & cafés", "instagram": "instagrammable & cafés",
             "food": "food", "gourmet": "food", "experience": "hands-on experiences", "diy": "hands-on experiences", "free": "free & easy", "fit": "free & easy", "festival": "seasonal festivals"}
SEASON_THEME = {"winter": "Winter & Ski", "ski": "Winter & Ski", "snow": "Winter & Ski", "spring": "Cherry Blossom", "sakura": "Cherry Blossom", "autumn": "Autumn Foliage", "fall": "Autumn Foliage"}
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, required=True); ap.add_argument("--entry", default=""); ap.add_argument("--exit", default=""); ap.add_argument("--themes", default="")
    ap.add_argument("--cities", default=""); ap.add_argument("--season", default=""); ap.add_argument("--kb", default=os.path.join(HERE, "..", "kb")); ap.add_argument("--top", type=int, default=3); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    fams = json.load(open(os.path.join(a.kb, "families.json"), encoding="utf-8"))
    tours = {t["code"]: t for t in json.load(open(os.path.join(a.kb, "tours.json"), encoding="utf-8"))}
    want_themes = set()
    for raw in [x.strip().lower() for x in a.themes.split(",") if x.strip()]:
        want_themes.add(THEME_SYN.get(raw, raw))
        for k, v in THEME_SYN.items():
            if k in raw: want_themes.add(v)
    want_cities = {geo.norm(x) for x in a.cities.split(",") if x.strip()}
    entry, exit_ = geo.norm(re.split(r"[(/]", a.entry)[0]), geo.norm(re.split(r"[(/]", a.exit)[0])
    season = a.season.lower()
    scored = []
    for f in fams:
        s = 0.0; why = []
        if f["days_min"] and f["days_max"]:
            if f["days_min"] <= a.days <= f["days_max"]: s += 3; why.append(f"天数 {a.days} 在带内 {f['days_min']}–{f['days_max']}")
            else:
                gap = min(abs(a.days - f["days_min"]), abs(a.days - f["days_max"])); s += max(0, 2 - gap * 0.5); why.append(f"天数差 {gap}")
        ft = {t.lower() for t in f["themes"]}
        hit = {w for w in want_themes if any(w in t for t in ft)}
        s += 1.5 * len(hit); why += [f"主题 {h}" for h in hit]
        ch = want_cities & set(f["cities"]); s += 2 * len(ch); why += [f"城市 {c}" for c in ch]
        if f["skeleton"]:
            if entry and f["skeleton"][0]["key"] and (entry in f["skeleton"][0]["key"] or f["skeleton"][0]["key"] in entry): s += 1; why.append("进点吻合")
            if exit_ and f["skeleton"][-1]["key"] and (exit_ in f["skeleton"][-1]["key"] or f["skeleton"][-1]["key"] in exit_): s += 1; why.append("出点吻合")
        if season and SEASON_THEME.get(season) in f["themes"]: s += 2; why.append(f"季节 {season}")
        scored.append((s, f, why))
    scored.sort(key=lambda x: -x[0])
    out = []
    for s, f, why in scored[: a.top]:
        # 家族内最接近天数的成员
        mem = sorted([tours[m] for m in f["members"] if m in tours and tours[m]["days"]], key=lambda t: (abs(t["days"] - a.days), -len(t["days_detail"])))
        refs = []
        for t in mem[:3]:
            refs.append({"code": t["code"], "title_en": t["title_en"], "title_cn": t.get("title_cn"), "days": t["days"], "price_usd": t["price"],
                         "route": " > ".join(f"{r['city']}({r['nights']})" for r in t["route"]),
                         "days_detail": [{"day": d["day"], "city": d["city"], "from": d["from"], "transport": d["transport"], "attractions": d["attractions"], "meals": d["meals"]} for d in t["days_detail"]],
                         "hotels": t["hotels"][:8]})
        out.append({"score": round(s, 1), "family": f["id"], "name_cn": f["name_cn"], "why": why, "days_band": f["days_band"], "price_usd": [f["price_usd_min"], f["price_usd_max"]],
                    "skeleton": " > ".join(f"{x['city']}({x['nights']})" for x in f["skeleton"]), "note_cn": f["note_cn"], "references": refs})
    if a.json: print(json.dumps(out, ensure_ascii=False, indent=1)); return
    for o in out:
        print(f"## {o['family']} {o['name_cn']}  score={o['score']}  天数带 {o['days_band']}  USD {o['price_usd']}")
        print(f"   骨架：{o['skeleton']}"); print(f"   依据：{'；'.join(o['why'])}"); print(f"   说明：{o['note_cn'][:160]}")
        for r in o["references"]:
            print(f"   - 参考 {r['code']} {r['days']}D USD {r['price_usd'].get('min')}–{r['price_usd'].get('max')} | {r['title_en']} | {r['route']}")
if __name__ == "__main__":
    main()
