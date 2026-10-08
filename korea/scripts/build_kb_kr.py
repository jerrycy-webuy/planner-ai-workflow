# -*- coding: utf-8 -*-
"""统一线路 JSON → 各站目录/标准行程/景点表 + 家族归并 + 生成行程用知识包（kb/）。
用法: python3 -I build_kb_kr.py <data_dir> <kb_dir>
"""
import sys, os, re, json, csv, statistics, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geo_kr as geo
import names_kr as names
from families_def_kr import FAMILIES
from seasons_kr import SEASONS

SITES = [("chanbrothers", "Chan Brothers（新加坡）", "chanbrothers.com"), ("euholidays", "EU Holidays（新加坡）", "euholidays.com.sg"),
         ("dynastytravel", "Dynasty Travel（新加坡）", "dynastytravel.com.sg"), ("koreatraveleasy", "KoreaTravelEasy（首尔地接）", "koreatraveleasy.com")]
FX_USD = {"SGD": 0.78, "USD": 1.0}
TYPE_CN = {"group_coach": "跟团", "self_guided": "自由行", "private_custom": "私人包车", "join_in_group": "地接拼团"}
DATE = "2026-10-08"

def usd(t):
    p = t["price"]; fx = FX_USD.get(p.get("currency"), 1)
    lo = round(p["min"] * fx) if p.get("min") else None
    hi = round((p.get("max") or p["min"]) * fx) if p.get("min") else None
    return lo, hi

def themes_of(t):
    cats = collections.Counter(a["category"] for d in t["days_detail"] for a in d["attractions_detail"])
    en = {a["name_en"] for d in t["days_detail"] for a in d["attractions_detail"]}
    title = (t["title_en"] + " " + (t.get("season") or "")).lower()
    th = set()
    if cats["palace"] + cats["heritage"] + cats["temple"] >= 2: th.add("Heritage & Culture")
    if cats["nature"] + cats["park"] + cats["beach"] + cats["island"] >= 3: th.add("Nature & Scenery")
    if cats["ski"] or re.search(r"\bski", title): th.add("Winter & Ski")
    if "Cherry Blossom Viewing" in en or "Jinhae Gunhangje Cherry Blossom Festival" in en or "blossom" in title: th.add("Cherry Blossom")
    if "Autumn Foliage" in en or "autumn" in title or "maple" in title or "foliage" in title: th.add("Autumn Foliage")
    if cats["themepark"]: th.add("Theme Parks & Family")
    if cats["farm"] + cats["experience"] >= 3: th.add("Hands-on Experiences")
    if cats["outlet"] + cats["shopstop"] + cats["district"] >= 4: th.add("Shopping & City")
    if cats["dmz"]: th.add("DMZ")
    if cats["cafe"] or "instagram" in title: th.add("Instagrammable & Cafés")
    if "yummy" in title or "taste" in title or "food" in title: th.add("Food")
    if "family" in title: th.add("Theme Parks & Family")
    if cats["festival"] and "Cherry Blossom" not in th and "Autumn Foliage" not in th: th.add("Seasonal Festivals")
    if t["tour_type"] == "self_guided": th.add("Free & Easy")
    return sorted(th | set(t.get("themes") or []))

def shopping_stops(t):
    return sorted({a["name_cn"] for d in t["days_detail"] for a in d["attractions_detail"] if a["category"] == "shopstop"})

def route_str(t, cn=False):
    out = []
    for r in t["route"]:
        name = geo.CITIES.get(r["key"], (r["city"], r["city"]))[1] if cn else r["city"]
        out.append(f"{name} ({r['nights']}N)")
    return " > ".join(out) or "—"

def clean_hotel(h):
    h = re.sub(r"\s+", " ", h or "").strip(" .")
    return h

# ---------------- 各站输出 ----------------
def write_site(data_dir, site, label, domain, tours):
    d = os.path.join(data_dir, site)
    # 目录
    rows = []
    for t in tours:
        lo, hi = usd(t)
        rows.append({"code": t["code"], "type": TYPE_CN.get(t["tour_type"], t["tour_type"]), "title_en": t["title_en"], "title_cn": t.get("title_cn") or "",
                     "days": t["days"], "nights": t["nights"], "route": route_str(t), "route_cn": route_str(t, True),
                     "price": f"{t['price'].get('currency')} {int(t['price']['min']) if t['price'].get('min') else '—'}", "price_usd_min": lo or "",
                     "season": t.get("season") or "", "themes": "; ".join(t["themes"]), "shopping_stops": "、".join(t["shopping_stops"]), "url": t["url"]})
    with open(os.path.join(d, "tours_catalog.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    L = [f"# {label} · 韩国线目录（{len(tours)} 条）", "", f"> 来源 https://www.{domain} · 抓取 {DATE} · 价格为站点标价，USD 按 1 SGD = 0.78 USD 折算只作对标", "",
         "| 代码 | 类型 | 线路 | 天数 | 住宿骨架 | 标价 | 季节 | 主题 |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['code']} | {r['type']} | {r['title_en']}{' / ' + r['title_cn'] if r['title_cn'] else ''} | {r['days']}D{r['nights']}N | {r['route_cn']} | {r['price']} | {r['season']} | {r['themes']} |")
    open(os.path.join(d, "tours_catalog.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    # 标准行程（逐日）
    L = [f"# {label} · 韩国线标准行程（Package Tour 格式）", "", f"> house grammar：`CITY_EN 中文 (2N)`；逐日：城市 · 交通 · 景点（词典标准名 / 中文）· 含餐 · 住宿。抓取 {DATE}。", ""]
    for t in tours:
        lo, hi = usd(t)
        L += [f"## {t['code']} · {t['title_en']}" + (f" / {t['title_cn']}" if t.get("title_cn") else ""), "",
              f"- 类型：{TYPE_CN.get(t['tour_type'], t['tour_type'])} · {t['days']} 天 {t['nights']} 晚 · 标价 {t['price'].get('currency')} {t['price'].get('min') or '—'}（≈ USD {lo or '—'}）· {t['price'].get('note','')}",
              f"- 住宿骨架：{' > '.join(f'{r['city'].upper()} {geo.CITIES.get(r['key'], ('', r['city']))[1]} ({r['nights']}N)' for r in t['route']) or '—'}",
              f"- 季节：{t.get('season') or '全年'} · 主题：{', '.join(t['themes']) or '—'}" + (f" · 购物站：{'、'.join(t['shopping_stops'])}" if t["shopping_stops"] else ""),
              f"- 链接：{t['url']}", "", "| 天 | 城市 | 交通 | 景点 | 含餐 | 住宿 |", "|---|---|---|---|---|---|"]
        for x in t["days_detail"]:
            sp = "、".join(f"{a['name_cn']}" for a in x["attractions_detail"]) or "—"
            L.append(f"| D{x['day']} | {x.get('title') or x.get('city') or ''} | {x.get('transport') or ''} | {sp} | {x.get('meals') or ''} | {(x.get('hotel') or '') if x.get('stay') else ''} |")
        if t.get("departures"):
            L += ["", "出发日期：" + "；".join(f"{p['date']} {p['code']} 双人房 {p['twin']} 单人 {p['single']}（{p['status']}）" for p in t["departures"])]
        L.append("")
    open(os.path.join(d, "package_tours.md"), "w", encoding="utf-8").write("\n".join(L))
    # 景点
    att = collections.OrderedDict()
    for t in tours:
        for x in t["days_detail"]:
            for a in x["attractions_detail"]:
                k = a["name_en"]
                if k not in att: att[k] = dict(a, tours=[])
                if t["code"] not in att[k]["tours"]: att[k]["tours"].append(t["code"])
    rows = sorted(att.values(), key=lambda a: (-len(a["tours"]), a["name_en"]))
    with open(os.path.join(d, "attractions.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow(["name_en", "name_cn", "city", "city_cn", "region_cn", "category", "tour_count", "tours"])
        for a in rows:
            cn, reg, regcn = geo.city_info(a["city_key"])
            w.writerow([a["name_en"], a["name_cn"], geo.CITIES.get(a["city_key"], ("",))[0], cn, regcn, names.CAT_CN.get(a["category"]), len(a["tours"]), " ".join(a["tours"])])
    L = [f"# {label} · 韩国线景点（{len(rows)} 个）", "", "| 景点 | 中文 | 城市 | 类别 | 出现线路 |", "|---|---|---|---|---|"]
    for a in rows:
        L.append(f"| {a['name_en']} | {a['name_cn']} | {geo.city_info(a['city_key'])[0] or ''} | {names.CAT_CN.get(a['category'])} | {len(a['tours'])}：{' '.join(a['tours'][:8])} |")
    open(os.path.join(d, "attractions.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

# ---------------- 合并 + 知识包 ----------------
def main():
    data_dir, kb_dir = sys.argv[1], sys.argv[2]
    os.makedirs(kb_dir, exist_ok=True); os.makedirs(os.path.join(data_dir, "merged"), exist_ok=True)
    all_tours = []
    for site, label, domain in SITES:
        tours = json.load(open(os.path.join(data_dir, site, "raw", f"{site}_tours.json"), encoding="utf-8"))
        for t in tours:
            t["themes"] = themes_of(t); t["shopping_stops"] = shopping_stops(t)
        write_site(data_dir, site, label, domain, tours)
        all_tours += tours
    by_code = {t["code"]: t for t in all_tours}
    fam_of = collections.defaultdict(list)
    for f in FAMILIES:
        for m in f["members"]:
            assert m in by_code, m
            fam_of[m].append(f["id"])

    # tours.json（紧凑版）
    tours_kb = []
    for t in all_tours:
        lo, hi = usd(t)
        tours_kb.append({"code": t["code"], "site": t["site"], "tour_type": t["tour_type"], "title_en": t["title_en"], "title_cn": t.get("title_cn"),
                         "days": t["days"], "nights": t["nights"], "price": {"min": lo, "max": hi, "currency": "USD", "note": f"{t['price'].get('currency')} {t['price'].get('min')}；{t['price'].get('note','')}"},
                         "themes": t["themes"], "season": t.get("season"), "families": fam_of.get(t["code"], []),
                         "route": [{"city": r["city"], "key": r["key"], "nights": r["nights"]} for r in t["route"]],
                         "days_detail": [{"day": x["day"], "city": x["city"], "key": x["key"], "from": x.get("from"), "transport": x.get("transport"),
                                          "attractions": x["attractions"], "meals": x.get("meals"), "stay": x.get("stay"), "title": x.get("title")} for x in t["days_detail"]],
                         "hotels": [f"{clean_hotel(h['name'])} ({h['city']}, {h['nights']}N)" for h in t["hotels"]],
                         "shopping_stops": t["shopping_stops"], "inclusions": t.get("inclusions") or [], "url": t["url"]})
    json.dump(tours_kb, open(os.path.join(kb_dir, "tours.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # families.json
    fams = []
    for f in FAMILIES:
        mem = [by_code[m] for m in f["members"]]
        prices = [p for t in mem for p in usd(t) if p]
        days = [t["days"] for t in mem]
        th = collections.Counter(x for t in mem for x in t["themes"])
        cities = sorted({r["key"] for t in mem for r in t["route"]} | {x["key"] for t in mem for x in t["days_detail"] if x.get("key")})
        fams.append({"id": f["id"], "name_cn": f["name_cn"], "name_en": f["name_en"], "standard": f["standard"],
                     "skeleton": [{"city": c, "key": geo.key_of(c), "nights": n} for c, n in f["skeleton"]],
                     "days_band": f"{min(days)}–{max(days)}D" if min(days) != max(days) else f"{min(days)}D", "days_min": min(days), "days_max": max(days),
                     "price_usd_min": min(prices) if prices else None, "price_usd_max": max(prices) if prices else None,
                     "members": f["members"], "tour_types": sorted({TYPE_CN[t["tour_type"]] for t in mem}), "sites": sorted({t["site"] for t in mem}),
                     "note_cn": f["note_cn"], "themes": [k for k, c in th.most_common() if c * 2 >= len(mem)][:8], "cities": [c for c in cities if c]})
    json.dump(fams, open(os.path.join(kb_dir, "families.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # attractions.json（合并池 + 等级）
    pool = collections.OrderedDict()
    for t in all_tours:
        for x in t["days_detail"]:
            for a in x["attractions_detail"]:
                k = a["name_en"]
                if k not in pool: pool[k] = dict(a, tours=[], sites=set(), families=set(), cities_seen=set())
                p = pool[k]
                if t["code"] not in p["tours"]: p["tours"].append(t["code"])
                p["sites"].add(t["source"]); p["families"].update(fam_of.get(t["code"], []))
                if x.get("key"): p["cities_seen"].add(x["key"])
    # 词典里有但线路没出现的条目，作为「可选」入池（来自地接/攻略常识，便于 Planner 补点）
    for _, en, cn, ck, cat in names.G:
        if en not in pool:
            pool[en] = {"name_en": en, "name_cn": cn, "city_key": ck, "category": cat, "tours": [], "sites": set(), "families": set(), "cities_seen": set()}
    attractions = []
    for a in pool.values():
        n = len(a["tours"])
        cn, reg, regcn = geo.city_info(a["city_key"])
        attractions.append({"name_en": a["name_en"], "name_cn": a["name_cn"], "city": geo.CITIES.get(a["city_key"], (a["city_key"],))[0], "city_key": a["city_key"],
                            "city_cn": cn, "region": reg, "region_cn": regcn, "category": a["category"], "category_cn": names.CAT_CN.get(a["category"]),
                            "level": "core" if n >= 4 else "common" if n >= 2 else "optional", "tour_count": n, "families": sorted(a["families"]),
                            "tours": a["tours"], "sites": sorted(a["sites"]) or ["词典（未见在售线路）"], "generic": a["name_en"] in names.GENERIC,
                            "cities_seen": sorted(a["cities_seen"])})
    attractions.sort(key=lambda a: (a["region"] or "", a["city_key"] or "", -a["tour_count"], a["name_en"]))
    json.dump(attractions, open(os.path.join(kb_dir, "attractions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # city_graph.json
    nodes = collections.OrderedDict(); edges = {}
    for t in all_tours:
        for r in t["route"]:
            k = r["key"]
            if k not in nodes: nodes[k] = {"key": k, "name_en": geo.CITIES.get(k, (r["city"],))[0], "name_cn": geo.city_info(k)[0], "region": geo.city_info(k)[1], "region_cn": geo.city_info(k)[2],
                                           "stays": 0, "tours": [], "nights": []}
            nodes[k]["stays"] += 1; nodes[k]["nights"].append(r["nights"])
            if t["code"] not in nodes[k]["tours"]: nodes[k]["tours"].append(t["code"])
        seq = [r["key"] for r in t["route"]]
        modes = {}
        for x in t["days_detail"]:
            if x.get("from") and x.get("transport"): modes[x["key"]] = x["transport"]
        for a, b in zip(seq, seq[1:]):
            e = edges.setdefault((a, b), {"from": a, "to": b, "tour_count": 0, "modes": collections.Counter(), "examples": []})
            e["tour_count"] += 1
            m = modes.get(b) or ("Flight" if "jeju" in (a, b) or "ulleungdo" in (a, b) else "Coach")
            e["modes"][m] += 1
            if len(e["examples"]) < 5: e["examples"].append(t["code"])
    for n in nodes.values():
        ns = n.pop("nights"); n["tour_count"] = len(n["tours"]); n["nights_typical"] = int(statistics.median(ns)); n["nights_min"] = min(ns); n["nights_max"] = max(ns)
    # 一日游可达（同日往返）：逐日活动城市 ≠ 过夜城市
    daytrips = collections.Counter()
    for t in all_tours:
        for x in t["days_detail"]:
            if x.get("stay_key") and x["attractions_detail"]:
                for a in x["attractions_detail"]:
                    if not a["city_key"] or a["city_key"] == x["stay_key"] or a["name_en"] in names.GENERIC: continue
                    daytrips[(x["stay_key"], a["city_key"])] += 1
    graph = {"nodes": list(nodes.values()),
             "edges": [dict(e, modes=dict(e["modes"])) for e in sorted(edges.values(), key=lambda e: -e["tour_count"])],
             "daytrip_reach": [{"base": a, "spot_city": b, "count": c} for (a, b), c in daytrips.most_common()],
             "transport_notes_cn": {"seoul-busan": "KTX 约 2h30m；内陆航班 GMP–PUS 约 1h", "seoul-jeju": "GMP–CJU 约 1h10m，班次极密", "busan-jeju": "PUS–CJU 约 1h",
                                    "seoul-gangneung": "KTX 约 1h50m；大巴约 2h30m", "seoul-jeonju": "大巴约 2h45m；KTX 至全州站约 1h40m",
                                    "busan-gyeongju": "大巴约 1h；KTX 新庆州站约 30m", "seoul-pyeongchang": "大巴约 2h30m；KTX 珍富站约 1h40m",
                                    "jeju-gangwon": "无直达陆路，需飞金浦或襄阳", "pohang-ulleungdo": "高速船约 3h（冬季常停航）",
                                    "coach_limit": "韩国旅游大巴司机每日驾驶建议 ≤ 10 小时，跨道长途日景点 ≤ 3 个"}}
    json.dump(graph, open(os.path.join(kb_dir, "city_graph.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # hotels.json
    tier_of = {"CB": {"group_coach": "group_standard", "self_guided": "fit", "private_custom": "fit"}, "EU": {"group_coach": "group_standard"},
               "DYN": {"group_coach": "premium"}, "KTE": {"join_in_group": "join_in"}}
    hot = collections.defaultdict(lambda: collections.defaultdict(set))
    for t in all_tours:
        for h in t["hotels"]:
            if not h.get("city_key") or not h.get("name"): continue
            for part in re.split(r"\s+/\s+|\s+or\s+(?!similar)", clean_hotel(h["name"])):
                part = re.sub(r"\s*(or similar( property)?|or equivalent)\s*$", "", part, flags=re.I).strip(" ,.")
                part = re.sub(r"^(overnight in [^:]+:\s*)", "", part, flags=re.I)
                if len(part) > 3 and not re.search(r"simil|^choice|^\d|accommodation", part, re.I):
                    hot[h["city_key"]][tier_of.get(t["site"], {}).get(t["tour_type"], "other")].add(part)
    def dedupe(v):
        seen = {}
        for x in sorted(v, key=len):
            k = re.sub(r"\b(hotel|the)\b|[^a-z0-9]", "", x.lower())
            k = "".join(sorted(re.findall(r"[a-z]+|\d+", re.sub(r"\b(hotel|the)\b", "", x.lower()))))
            seen.setdefault(k, x)
        return sorted(seen.values())
    hotels = [{"city_key": k, "city_cn": geo.city_info(k)[0], "tiers": {tier: dedupe(v) for tier, v in tiers.items()}} for k, tiers in sorted(hot.items(), key=lambda x: -sum(len(v) for v in x[1].values()))]
    json.dump(hotels, open(os.path.join(kb_dir, "hotels.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # stats.json（节奏先验，分跟团 / 全部）
    def pct(xs, q):
        xs = sorted(xs); return xs[min(len(xs) - 1, int(round(q * (len(xs) - 1))))] if xs else None
    def stats_for(ts):
        per_day = [len(x["attractions"]) for t in ts for x in t["days_detail"][1:-1] if x["attractions"]]
        all_mid = [x for t in ts for x in t["days_detail"][1:-1]]
        cbd = collections.defaultdict(list)
        one = []; transfer = []
        for t in ts:
            if not t["route"]: continue
            cbd[t["days"]].append(len({r["key"] for r in t["route"]}))
            one.append(sum(1 for r in t["route"] if r["nights"] == 1) / len(t["route"]))
            transfer += [1 if x.get("from") else 0 for x in t["days_detail"][1:-1]]
        return {"attractions_per_day": {"p50": pct(per_day, .5), "p90": pct(per_day, .9), "max": max(per_day) if per_day else None,
                                        "share_of_days_with_listed_spots": round(len(per_day) / max(1, len(all_mid)), 2)},
                "cities_by_days": {str(d): {"p50": statistics.median(v), "min": min(v), "max": max(v), "n": len(v)} for d, v in sorted(cbd.items())},
                "one_night_stay_share": {"p50": round(pct(one, .5), 2), "p90": round(pct(one, .9), 2)},
                "transfer_day_share": round(sum(transfer) / max(1, len(transfer)), 2),
                "typical_first_city": collections.Counter(t["route"][0]["key"] for t in ts if t["route"]).most_common(6)}
    group = [t for t in all_tours if t["tour_type"] == "group_coach"]
    st = stats_for(all_tours); st["group_coach"] = stats_for(group)
    st["shopping_stop_share_group"] = round(sum(1 for t in group if t["shopping_stops"]) / max(1, len(group)), 2)
    st["notes_cn"] = (f"按 {len(all_tours)} 条在售线路统计（新加坡出发跟团 {len(group)} 条为主）。首末日为国际航班日不计景点。"
                      "韩国跟团常见首晚住仁川/金浦（红眼航班或夜抵），首尔通常是收尾 2–3 晚（购物 + 免税）。")
    json.dump(st, open(os.path.join(kb_dir, "stats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(SEASONS, open(os.path.join(kb_dir, "seasons.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # merged：家族 md/json + 景点按城市
    json.dump(fams, open(os.path.join(data_dir, "merged", "merged_itineraries.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    L = [f"# 韩国线行程家族（{len(fams)} 个）", "", f"> 四站 {len(all_tours)} 条线路归并 · {DATE}。价格 USD 为每人对标价（新加坡三站含机票，KTE 为首尔出发地接价）。", ""]
    for f in fams:
        L += [f"## {f['id']} {f['name_cn']}", "", f"- 标准骨架：{' > '.join(f'{geo.CITIES.get(s['key'], (s['city'], s['city']))[1]} {s['nights']}N' for s in f['skeleton'])}",
              f"- 天数带 {f['days_band']} · USD {f['price_usd_min']}–{f['price_usd_max']} · 形态：{'、'.join(f['tour_types'])} · 来源：{'、'.join(f['sites'])}",
              f"- 主题：{', '.join(f['themes'])}", f"- 说明：{f['note_cn']}", "", "| 成员 | 天数 | 住宿骨架 | USD 起 |", "|---|---|---|---|"]
        for m in f["members"]:
            t = by_code[m]
            L.append(f"| {m}{' ★标准' if m == f['standard'] else ''} {t['title_en']} | {t['days']}D{t['nights']}N | {route_str(t, True)} | {usd(t)[0] or '—'} |")
        L.append("")
    open(os.path.join(data_dir, "merged", "merged_itineraries.md"), "w", encoding="utf-8").write("\n".join(L))
    L = [f"# 韩国景点池：按区域 → 城市（{len(attractions)} 个）", "", "> tag：核心 = 出现 ≥4 条线路；常见 = 2–3 条；可选 = 1 条或仅词典（未见在售线路，供 Planner 补点）。泛化体验（韩服、购物站等）城市按出现城市记。", ""]
    with open(os.path.join(data_dir, "merged", "attractions_by_city.csv"), "w", encoding="utf-8-sig", newline="") as fcsv:
        w = csv.writer(fcsv); w.writerow(["region_cn", "city", "city_cn", "name_en", "name_cn", "category", "level", "tour_count", "families", "tours"])
        lv = {"core": "核心", "common": "常见", "optional": "可选"}
        cur_r = cur_c = None
        for a in attractions:
            if a["region_cn"] != cur_r: cur_r = a["region_cn"]; L += ["", f"## {cur_r}"]
            if a["city_key"] != cur_c: cur_c = a["city_key"]; L += ["", f"### {a['city']} {a['city_cn']}", "", "| 景点 | 中文 | 类别 | tag | 线路数 | 家族 |", "|---|---|---|---|---|---|"]
            L.append(f"| {a['name_en']} | {a['name_cn']} | {a['category_cn']} | {lv[a['level']]} | {a['tour_count']} | {' '.join(a['families'])} |")
            w.writerow([a["region_cn"], a["city"], a["city_cn"], a["name_en"], a["name_cn"], a["category_cn"], lv[a["level"]], a["tour_count"], " ".join(a["families"]), " ".join(a["tours"])])
    open(os.path.join(data_dir, "merged", "attractions_by_city.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"tours {len(all_tours)} · families {len(fams)} · attractions {len(attractions)} (in tours {sum(1 for a in attractions if a['tour_count'])}) · "
          f"nodes {len(graph['nodes'])} · edges {len(graph['edges'])} · hotel cities {len(hotels)}")

if __name__ == "__main__":
    main()
