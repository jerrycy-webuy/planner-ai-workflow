# -*- coding: utf-8 -*-
"""把 consolidate/build_families 的输出转成生成行程用的机器可读知识包。
用法: python3 -I build_kb.py <out_merged> <out_sgj> <out_jnj> <kb_dir>
输出: families.json tours.json city_graph.json attractions.json hotels.json stats.json seasons.json
"""
import sys, os, re, json, csv, collections, statistics
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geo
from families_def import FAMILIES
OUT_M, OUT_S, OUT_J, KB = sys.argv[1:5]
os.makedirs(KB, exist_ok=True)

tours = {}
for d in (OUT_S, OUT_J):
    for t in json.load(open(os.path.join(d, "package_tours.json"), encoding="utf-8")):
        tours[t["code"]] = t
attrs = list(csv.DictReader(open(os.path.join(OUT_M, "attractions_by_city.csv"), encoding="utf-8-sig")))

# ---------- 城市归一 ----------
STATION_FIX = {"turuga": "tsuruga", "hakata": "fukuoka", "shinosaka": "osaka", "shinaomori": "aomori", "shinhakodate": "hakodate", "shinhakodatehokuto": "hakodate",
               "tokyobaymaihama": "maihama", "osakauniversalcity": "osaka", "universalcity": "osaka", "toya": "laketoya", "shinyokohama": "yokohama",
               "kiikatsuura": "kiikatsuura", "yudanaka": "yudanakaonsen", "hakubawadano": "hakuba", "hakubatsugaike": "hakuba", "hakubamisorano": "hakuba",
               "osakasakai": "osaka", "hirosakimtiwaki": "hirosaki", "hakkodaoirase": "hakkoda", "oma": "oma", "mutsu": "mutsu",
               "tokyoorueno": "tokyo", "tokyoshinjuku": "tokyo", "kagoshimachuo": "kagoshima", "meitetsunagoya": "nagoya", "osakanambaorosakashinsaibashi": "osaka",
               "osakauehommachi": "osaka", "hirshima": "hiroshima", "kanzawa": "kanazawa", "inuyamayuen": "inuyama", "tosu": "tosu", "minoota": "minoota"}
HUBS = ("tokyo", "osaka", "kyoto", "nagoya", "fukuoka", "sapporo", "hiroshima", "kanazawa", "sendai", "kobe", "yokohama")
def hubify(k):
    for h in HUBS:
        if k and k != h and k.startswith(h) and not k.startswith("kyotango"): return h
    return k
def ckey(name):
    if not name: return None
    k = geo.norm(re.sub(r"\s*(station|staion|airport|st\.)\s*$", "", name.strip(), flags=re.I))
    k = hubify(k)
    k = re.sub(r"^shin(?=[a-z])", "", k) if k.startswith("shin") and k not in ("shinjuku", "shinagawa", "shimokita", "shinhotaka", "shingu") else k
    k = STATION_FIX.get(k, k)
    return k
def cinfo(key):
    cn, reg, regcn = geo.city_info(key)
    return cn, reg

# ---------- tours.json（紧凑版） ----------
compact = []
for code, t in tours.items():
    route = [{"city": r["city"], "key": ckey(r["city"]), "nights": r["nights"]} for r in t["route"]]
    days = []
    for d in t["days_detail"]:
        days.append({"day": d["day"], "city": d.get("to"), "key": ckey(d.get("to")), "from": d.get("from"), "transport": d.get("transport"),
                     "attractions": d.get("attractions") or [], "meals": d.get("meals"), "stay": d.get("stay"), "title": d.get("title")})
    compact.append({"code": code, "site": "JNJ" if code.startswith("JNJ") else "SGJ", "title_en": t["title_en"], "title_cn": t.get("title_cn"),
                    "days": t["days"], "nights": t["nights"], "price": t["price"], "themes": t.get("themes") or [], "season": t.get("season"),
                    "airports": t.get("airports"), "route": route, "days_detail": days, "hotels": t.get("hotels") or [],
                    "inclusions": t.get("inclusions") or [], "highlights": t.get("highlights") or [], "url": t.get("url")})
json.dump(compact, open(os.path.join(KB, "tours.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- families.json ----------
fam_out = []
for f in FAMILIES:
    members = [m for m in f["members"] if m in tours]
    prices = [tours[m]["price"] for m in members if tours[m]["price"].get("min") is not None and tours[m]["price"].get("currency") == "USD"]
    days_list = [tours[m]["days"] for m in members if tours[m]["days"]]
    fam_out.append({"id": f["id"], "name_cn": f["name"], "name_en": f["name_en"], "standard": f["standard"],
                    "skeleton": [{"city": c, "key": ckey(c), "nights": n} for c, n in f["skeleton"]], "days_band": f["days"],
                    "days_min": min(days_list) if days_list else None, "days_max": max(days_list) if days_list else None,
                    "price_usd_min": min(p["min"] for p in prices) if prices else None, "price_usd_max": max((p["max"] or p["min"]) for p in prices) if prices else None,
                    "members": members, "note_cn": f["note"],
                    "themes": sorted({th for m in members for th in (tours[m].get("themes") or [])}),
                    "cities": sorted({ckey(r["city"]) for m in members for r in tours[m]["route"] if ckey(r["city"])})})
json.dump(fam_out, open(os.path.join(KB, "families.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- city_graph.json ----------
nodes = {}
def add_node(key, name=None):
    if not key: return
    if key not in nodes:
        cn, reg = cinfo(key)
        nodes[key] = {"key": key, "name_en": name or key, "name_cn": cn, "region": reg, "stays": 0, "tours": set(), "nights": []}
edges = {}
def add_edge(a, b, mode, code, via=None):
    if not a or not b or a == b: return
    e = edges.setdefault((a, b), {"from": a, "to": b, "modes": collections.Counter(), "tours": set(), "via": collections.Counter()})
    e["modes"][mode] += 1; e["tours"].add(code)
    if via: e["via"][via] += 1
MODE = {"🚅": "shinkansen", "🚃": "train", "🚌": "bus", "🚕": "taxi", "🚖": "taxi", "⛴": "ferry", "🚢": "ferry", "✈": "flight", "🚠": "ropeway", "🚡": "ropeway", "🚗": "car"}
for t in compact:
    for r in t["route"]:
        add_node(r["key"], r["city"]); nodes[r["key"]]["stays"] += 1; nodes[r["key"]]["tours"].add(t["code"])
        if r["nights"]: nodes[r["key"]]["nights"].append(r["nights"])
    # 住宿序列边
    seq = [r["key"] for r in t["route"] if r["key"]]
    for a, b in zip(seq, seq[1:]):
        add_edge(a, b, "stay-sequence", t["code"])
    # 交通段边（含中转）
    for d in t["days_detail"]:
        tr = d.get("transport") or ""
        for seg in tr.split("; "):
            seg = seg.strip()
            if not seg: continue
            mode = MODE.get(seg[0], None)
            if mode is None:
                if re.search(r"shinkansen", seg, re.I): mode = "shinkansen"
                elif re.search(r"taxi|private vehicle|charter", seg, re.I): mode = "taxi"
                elif re.search(r"bus", seg, re.I): mode = "bus"
                elif re.search(r"ferry|boat", seg, re.I): mode = "ferry"
                elif re.search(r"train|express", seg, re.I): mode = "train"
                else: mode = "other"
            parts = [p.strip() for p in re.split(r"→|->|⇒", seg.lstrip("".join(MODE.keys()))) if p.strip()]
            keys = [ckey(p) for p in parts]
            keys = [k for k in keys if k]
            for a, b in zip(keys, keys[1:]):
                add_node(a, a.title()); add_node(b, b.title())
                add_edge(a, b, mode, t["code"])
for k, n in nodes.items():
    n["tours"] = sorted(n["tours"]); n["tour_count"] = len(n["tours"])
    n["nights_typical"] = statistics.median(n["nights"]) if n["nights"] else None
    n["nights_min"] = min(n["nights"]) if n["nights"] else None; n["nights_max"] = max(n["nights"]) if n["nights"] else None
    del n["nights"]
edge_list = []
for (a, b), e in edges.items():
    edge_list.append({"from": a, "to": b, "from_cn": nodes[a]["name_cn"], "to_cn": nodes[b]["name_cn"], "modes": dict(e["modes"]),
                      "tour_count": len(e["tours"]), "tours": sorted(e["tours"])[:12], "via": dict(e["via"])})
edge_list.sort(key=lambda e: -e["tour_count"])
json.dump({"nodes": sorted(nodes.values(), key=lambda n: -n["stays"]), "edges": edge_list}, open(os.path.join(KB, "city_graph.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- attractions.json ----------
attr_out = []
for a in attrs:
    attr_out.append({"name_en": a["name_en"], "name_cn": a["name_cn"], "city": a["city"], "city_key": ckey(a["city"]), "city_cn": a["city_cn"], "region": a["region"],
                     "category": a["category"], "category_cn": a.get("category_cn", ""), "level": a["level"], "tour_count": int(a["tour_count"] or 0),
                     "families": a["families"].split(), "tours": a["tours"].split(), "site": a.get("site", ""), "description": a.get("description", "")})
json.dump(attr_out, open(os.path.join(KB, "attractions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- hotels.json ----------
hotels = collections.defaultdict(lambda: collections.defaultdict(set))
for t in compact:
    for h in t["hotels"]:
        m = re.match(r"^(.*?)\s*\((.*?),\s*(\d+)N(?:,\s*(.*?))?\)\s*$", h)
        if not m: continue
        name, loc, n, tier = m.group(1).strip(), m.group(2).strip(), int(m.group(3)), (m.group(4) or "standard").strip()
        tier = {"none": "standard", "std": "standard", "dx": "deluxe"}.get(tier, tier)
        hotels[ckey(loc) or loc][tier].add((name, loc))
hotel_out = []
for ck, tiers in hotels.items():
    cn, reg = cinfo(ck)
    hotel_out.append({"city_key": ck, "city_cn": cn, "tiers": {tier: sorted({n for n, _ in names}) for tier, names in tiers.items()}})
json.dump(hotel_out, open(os.path.join(KB, "hotels.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- stats.json（节奏先验） ----------
per_day_attr = [len(d["attractions"]) for t in compact if t["site"] == "SGJ" for d in t["days_detail"]]
per_day_attr_nonzero = [x for x in per_day_attr if x > 0]
cities_vs_days = collections.defaultdict(list)
for t in compact:
    if t["days"]: cities_vs_days[t["days"]].append(len({r["key"] for r in t["route"]}))
one_night_ratio = []
for t in compact:
    if t["route"]:
        one_night_ratio.append(sum(1 for r in t["route"] if r["nights"] == 1) / len(t["route"]))
transfer_days = 0; total_days = 0
for t in compact:
    for d in t["days_detail"]:
        total_days += 1
        if d.get("from") and d.get("from") != d.get("city"): transfer_days += 1
stats = {
    "attractions_per_day": {"p50": statistics.median(per_day_attr_nonzero), "p90": sorted(per_day_attr_nonzero)[int(len(per_day_attr_nonzero) * 0.9)], "max": max(per_day_attr_nonzero), "share_of_days_with_listed_spots": round(len(per_day_attr_nonzero) / len(per_day_attr), 2)},
    "cities_by_days": {str(k): {"p50": statistics.median(v), "min": min(v), "max": max(v), "n": len(v)} for k, v in sorted(cities_vs_days.items())},
    "one_night_stay_share": {"p50": round(statistics.median(one_night_ratio), 2), "p90": round(sorted(one_night_ratio)[int(len(one_night_ratio) * 0.9)], 2)},
    "transfer_day_share": round(transfer_days / total_days, 2),
    "typical_first_city": collections.Counter(t["route"][0]["key"] for t in compact if t["route"]).most_common(6),
    "notes_cn": "按 121 条在售线路统计（SGJ 自助游为主）。跟团大巴线路密度可高于此，建议 WEBUY 自家历史行程导入后重算。",
}
json.dump(stats, open(os.path.join(KB, "stats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- seasons.json（硬日期约束，人工表） ----------
seasons = [
 {"match": r"snow monkey|jigokudani", "name_cn": "雪猴（地狱谷野猿公苑）", "best": "12–3 月", "months": [12, 1, 2, 3], "note": "全年可去，雪景仅冬季"},
 {"match": r"tateyama|kurobe|alpine route|yuki-no-otani|snow corridor", "name_cn": "立山黑部阿尔卑斯路线", "best": "4 月中–11 月（雪之大谷 4 月中–6 月）", "months": [4, 5, 6, 7, 8, 9, 10, 11], "note": "冬季封闭"},
 {"match": r"nebuta", "name_cn": "青森睡魔祭", "best": "8 月 2–7 日", "months": [8], "note": "固定日期"},
 {"match": r"cherry blossom|sakura|hanami|senbonzakura|yoshino", "name_cn": "樱花", "best": "3 月下旬–4 月中（吉野 4 月上中旬）", "months": [3, 4], "note": "年际浮动"},
 {"match": r"light-up|lightup", "name_cn": "白川乡点灯", "best": "1–2 月指定日", "months": [1, 2], "note": "需预约"},
 {"match": r"ski|hakuba|rusutsu|furano ski|sahoro|appi|shiga kogen|zao", "name_cn": "滑雪场", "best": "12–3 月", "months": [12, 1, 2, 3], "note": "藏王树冰 1 月下–2 月"},
 {"match": r"lavender|farm tomita", "name_cn": "富良野薰衣草", "best": "7 月", "months": [7], "note": ""},
 {"match": r"autumn|koyo|momiji|foliage", "name_cn": "红叶", "best": "10 月中（北海道）–12 月上（京都）", "months": [10, 11, 12], "note": ""},
 {"match": r"shiretoko", "name_cn": "知床", "best": "5–10 月", "months": [5, 6, 7, 8, 9, 10], "note": "冬季流冰另算"},
 {"match": r"takayama festival", "name_cn": "高山祭", "best": "4 月 14–15 / 10 月 9–10", "months": [4, 10], "note": "固定日期"},
 {"match": r"kumano kodo|nakasendo|kamikochi", "name_cn": "徒步线", "best": "4–11 月", "months": [4, 5, 6, 7, 8, 9, 10, 11], "note": "上高地 11 月中封山"},
 {"match": r"expo 2025|yumeshima", "name_cn": "大阪世博", "best": "已于 2025-10-13 闭幕", "months": [], "note": "不可排入 2026 行程"},
]
json.dump(seasons, open(os.path.join(KB, "seasons.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"tours={len(compact)} families={len(fam_out)} nodes={len(nodes)} edges={len(edge_list)} attractions={len(attr_out)} hotel_cities={len(hotel_out)}")
print("stats:", json.dumps(stats, ensure_ascii=False)[:900])
print("unmapped nodes:", [n['key'] for n in nodes.values() if not n['name_cn']][:30])
print("top edges:", [(e['from'], e['to'], e['tour_count'], list(e['modes'])) for e in edge_list[:12]])
