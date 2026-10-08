# -*- coding: utf-8 -*-
"""行程校验器：对生成的 ItinerarySpec JSON 做确定性检查，输出问题清单（error / warn）与修复建议。
CLI: python3 -I validate_itinerary.py <spec.json> [--kb <kb_dir>] [--tour-type group_coach|self_guided|private_custom] [--month 4] [--json]
库:  from validate_itinerary import validate_spec; errors, warns = validate_spec(spec, kb_dir, tour_type, month)
退出码: 0 无 error；1 有 error。
"""
import sys, os, re, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geo_kr as geo

def norm(s):
    s = (s or "").lower(); s = re.sub(r"\(.*?\)", "", s); s = s.replace("-", " ").replace("’", "'").replace("'", "")
    s = re.sub(r"\b(the)\b", " ", s); s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def ckey(name):
    if not name: return None
    return geo.key_of(re.sub(r"\s*(station|airport|port|terminal)\s*$", "", name.strip(), flags=re.I))

# 同城/一日游等效：景点所在地 → 可视为当天城市（大巴单程 ≤ 约 1.5h 的放射范围）
NEARBY = {
    "seoul": {"incheon", "gimpo", "ganghwa", "paju", "suwon", "yongin", "gapyeong", "namiisland", "pocheon", "yangpyeong", "goyang", "icheon", "gwangmyeong", "yeoju", "anseong", "chuncheon"},
    "incheon": {"seoul", "gimpo", "ganghwa", "paju", "goyang", "suwon"}, "gimpo": {"seoul", "incheon", "ganghwa", "paju", "goyang"},
    "suwon": {"seoul", "yongin", "icheon", "anseong"}, "yongin": {"seoul", "suwon", "icheon"}, "gapyeong": {"namiisland", "chuncheon", "seoul", "pocheon", "yangpyeong", "hongcheon"},
    "chuncheon": {"gapyeong", "namiisland", "hongcheon", "hwacheon", "seoul"}, "hongcheon": {"chuncheon", "gapyeong", "pyeongchang", "hoengseong", "wonju"},
    "hoengseong": {"pyeongchang", "wonju", "hongcheon"}, "pyeongchang": {"gangneung", "hoengseong", "jeongseon", "hongcheon", "wonju", "yangyang", "yeongwol"},
    "gangneung": {"pyeongchang", "sokcho", "donghae", "yangyang", "samcheok", "jeongseon"}, "sokcho": {"yangyang", "gangneung", "inje", "pyeongchang"},
    "donghae": {"gangneung", "samcheok"}, "jeju": {"seogwipo", "udo"}, "seogwipo": {"jeju", "udo"},
    "busan": {"gyeongju", "ulsan", "gimhae", "changwon", "yangsan", "geoje", "miryang"}, "gyeongju": {"busan", "pohang", "ulsan", "daegu"},
    "daegu": {"gyeongju", "andong", "cheongdo", "mungyeong"}, "pohang": {"gyeongju"}, "andong": {"yeongju", "mungyeong", "daegu"},
    "jeonju": {"gunsan", "wanju", "jeongeup", "damyang", "namwon", "buyeo", "gongju", "jangseong", "gwangju"}, "gwangju": {"damyang", "jangseong", "boseong", "suncheon", "jeongeup", "mokpo"},
    "suncheon": {"yeosu", "boseong", "gwangyang", "gurye"}, "yeosu": {"suncheon", "gwangyang", "boseong"}, "mokpo": {"sinan", "haenam", "wando", "gwangju"},
    "daejeon": {"gongju", "buyeo", "boeun", "cheongju"}, "buyeo": {"gongju", "daejeon", "boryeong", "jeonju"}, "danyang": {"jecheon", "yeongwol", "chungju"},
    "namhae": {"hadong", "sacheon", "jinju"}, "hadong": {"namhae", "gurye", "jinju", "gwangyang"}, "seosan": {"taean", "yesan", "dangjin"},
}
AIRPORT_CITY = {"incheon": ["incheon", "seoul", "gimpo", "ganghwa"], "icn": ["incheon", "seoul", "gimpo", "ganghwa"], "seoul": ["seoul", "incheon", "gimpo"],
                "gimpo": ["seoul", "gimpo", "incheon"], "gmp": ["seoul", "gimpo", "incheon"], "busan": ["busan", "gyeongju", "ulsan", "changwon", "gimhae"],
                "gimhae": ["busan", "gyeongju", "ulsan", "changwon", "gimhae"], "pus": ["busan", "gyeongju", "ulsan", "changwon", "gimhae"],
                "jeju": ["jeju", "seogwipo"], "cju": ["jeju", "seogwipo"], "daegu": ["daegu", "gyeongju"], "tae": ["daegu", "gyeongju"],
                "cheongju": ["cheongju", "daejeon"], "cjj": ["cheongju", "daejeon"], "yangyang": ["sokcho", "gangneung", "yangyang"], "muan": ["mokpo", "gwangju"]}
ISLAND = {"jeju", "seogwipo", "udo", "ulleungdo"}
MAX_SPOTS = {"group_coach": 10, "join_in_group": 8, "self_guided": 7, "private_custom": 8}   # 韩国跟团每日景点 p50=4、p90=6、max=12（含购物站）

def city_matches(attr_city_key, day_key):
    if not attr_city_key or not day_key or attr_city_key == day_key: return True
    return attr_city_key in NEARBY.get(day_key, set()) or day_key in NEARBY.get(attr_city_key, set())

_KB_CACHE = {}
def load_kb(kb):
    if kb in _KB_CACHE: return _KB_CACHE[kb]
    d = {name: json.load(open(os.path.join(kb, f"{name}.json"), encoding="utf-8")) for name in ("city_graph", "attractions", "families", "stats", "seasons")}
    d["nodes"] = {n["key"]: n for n in d["city_graph"]["nodes"]}
    d["edges"] = {(e["from"], e["to"]): e for e in d["city_graph"]["edges"]}
    d["attr_idx"] = {}
    for x in d["attractions"]: d["attr_idx"].setdefault(norm(x["name_en"]), x)
    d["cn_idx"] = {x["name_cn"]: x for x in d["attractions"] if x.get("name_cn")}
    d["fam_idx"] = {f["id"]: f for f in d["families"]}
    d["spot_cities"] = {}
    try:
        for t in json.load(open(os.path.join(kb, "tours.json"), encoding="utf-8")):
            for day in t.get("days_detail", []):
                ck = day.get("key") or ckey(day.get("city"))
                for a in day.get("attractions", []):
                    if ck: d["spot_cities"].setdefault(norm(a), set()).add(ck)
    except FileNotFoundError:
        pass
    d["region_of"] = {n["key"]: n.get("region") for n in d["city_graph"]["nodes"]}
    d["n_tours"] = sum(1 for _ in open(os.path.join(kb, "tours.json"), encoding="utf-8") if '"code"' in _)
    _KB_CACHE[kb] = d
    return d

def find_spot(name, kbd):
    """精确 → 中文名 → 包含关系（≥6 字符）模糊匹配。"""
    n = norm(name)
    x = kbd["attr_idx"].get(n) or kbd["cn_idx"].get(name)
    if x: return x
    if len(n) >= 6:
        cands = [a for k, a in kbd["attr_idx"].items() if len(k) >= 6 and (k in n or n in k)]
        if cands: return sorted(cands, key=lambda a: -a.get("tour_count", 0))[0]
    return None

def region_of(key, kbd):
    r = kbd["region_of"].get(key)
    if r: return r
    _, reg, _ = geo.city_info(key or "")
    return reg

def spot_city_status(name, day_key, kbd, from_key=None):
    """返回 'ok' / 'daytrip' / 'wrong' / 'unknown'。
    词典景点以词典城市为准（真实线路常把出发前的景点记在到达城市那天）；泛化体验（韩服、购物站…）不限城市；
    移动日允许景点在出发城市。"""
    x = find_spot(name, kbd)
    if not x:
        n = norm(name); seen = kbd["spot_cities"].get(n)
        if not seen: return "unknown"
        if day_key in seen or any(city_matches(c, day_key) for c in seen): return "ok"
        return "daytrip" if any(region_of(c, kbd) == region_of(day_key, kbd) for c in seen) else "wrong"
    if x.get("generic"): return "ok"
    ck = x.get("city_key")
    for k in filter(None, (day_key, from_key)):
        if city_matches(ck, k): return "ok"
    if any(region_of(ck, kbd) == region_of(k, kbd) for k in filter(None, (day_key, from_key))): return "daytrip"
    return "wrong"

def airport_ok(ap, city_key):
    ap_k = geo.norm(re.split(r"[(/]", ap or "")[0]).replace("international", "")
    for k, cities in AIRPORT_CITY.items():
        if ap_k.startswith(k):
            return city_key in cities or any(city_key in NEARBY.get(c, set()) for c in cities)
    return True

def validate_spec(spec, kb, tour_type=None, month=None, max_spots=None):
    """返回 (errors, warnings)，每项 {level, code, day, msg, fix}。"""
    kbd = load_kb(kb)
    nodes, edges, graph, stats, seasons, families = kbd["nodes"], kbd["edges"], kbd["city_graph"], kbd["stats"], kbd["seasons"], kbd["fam_idx"]
    tour_type = tour_type or spec.get("tour_type") or "group_coach"
    month = month or spec.get("travel_month")
    max_spots = max_spots or MAX_SPOTS.get(tour_type, 6)
    issues = []
    def err(code, msg, fix=None, day=None): issues.append({"level": "error", "code": code, "day": day, "msg": msg, "fix": fix})
    def warn(code, msg, fix=None, day=None): issues.append({"level": "warn", "code": code, "day": day, "msg": msg, "fix": fix})

    days, nights = spec.get("days"), spec.get("nights")
    route = spec.get("route") or []; dd = spec.get("days_detail") or []
    # 1 结构
    if days and nights is not None and nights not in (days - 1, days - 2): err("E_NIGHTS", f"nights={nights} 应等于 days-1={days-1}（红眼航班可为 days-2）")
    if days and len(dd) != days: err("E_DAYCOUNT", f"days_detail 有 {len(dd)} 天，days={days}")
    rn = sum(r.get("nights") or 0 for r in route)
    # 红眼航班：Day 1 显式 stay=null（机上过夜）时，酒店夜数 = days-2
    redeye = bool(dd) and "stay" in dd[0] and not dd[0].get("stay") and len(dd) > 2
    exp_n = (days - 2) if (days and redeye) else (days - 1 if days else None)
    if days and rn != exp_n: err("E_ROUTE_NIGHTS", f"route 夜数合计 {rn} ≠ {exp_n}（days={days}{'，首晚红眼航班' if redeye else ''}）", "调整各城夜数或天数")
    if [d.get("day") for d in dd] != list(range(1, len(dd) + 1)): err("E_DAYSEQ", "days_detail 的 day 编号不连续或不从 1 开始")
    # 2 城市已知 & 路线边
    rkeys = [ckey(r.get("city")) for r in route]
    for r, k in zip(route, rkeys):
        if k not in nodes: warn("W_CITY_UNKNOWN", f"城市「{r.get('city')}」不在城市图里（{kbd['n_tours']} 条线路从未过夜）", "核实拼写；若是新目的地请确认交通与酒店供给")
    for (ra, ka), (rb, kb_) in zip(zip(route, rkeys), zip(route[1:], rkeys[1:])):
        if ka == kb_: err("E_ROUTE_DUP", f"route 连续两段同城 {ra.get('city')}", "合并为一段并累加夜数"); continue
        e, e_rev = edges.get((ka, kb_)), edges.get((kb_, ka))
        if not e and not e_rev:
            outs = [x["to"] for x in graph["edges"] if x["from"] == ka][:6]; ins = [x["from"] for x in graph["edges"] if x["to"] == kb_][:6]
            warn("W_LEG_UNSEEN", f"{ra.get('city')} → {rb.get('city')} 在 {kbd['n_tours']} 条线路中没有出现过", f"可行的下一站示例：{outs}；可行的上一站示例：{ins}；若确有直达交通请在 transport 写明并标「需核实」")
        elif not e and e_rev:
            warn("W_LEG_REVERSE", f"{ra.get('city')} → {rb.get('city')} 只在反方向出现过（{e_rev['tour_count']} 条）", "方向通常可逆，但请核对班次")
    # 3 节奏
    if route:
        one_n = sum(1 for r in route if (r.get("nights") or 0) == 1) / len(route)
        if one_n > stats["one_night_stay_share"]["p90"]: warn("W_PACE_ONE_NIGHT", f"1 晚停留占比 {one_n:.0%}，高于市场 P90 {stats['one_night_stay_share']['p90']:.0%}", "合并相邻 1 晚停留，减少换酒店")
        for r, k in zip(route, rkeys):
            n = nodes.get(k)
            if n and n.get("nights_max") and (r.get("nights") or 0) > n["nights_max"] + 1:
                warn("W_PACE_LONG_STAY", f"{r.get('city')} 住 {r['nights']} 晚，市场最多 {n['nights_max']} 晚", "拆出一日游或缩短")
        ncity = len({k for k in rkeys if k}); band = stats["cities_by_days"].get(str(days))
        if band and ncity > band["max"]: warn("W_PACE_TOO_MANY_CITIES", f"{days} 天安排 {ncity} 个过夜城市，市场最多 {band['max']}（中位 {band['p50']}）", "减少城市或增加天数")
    # 4 逐日
    if any(d.get("stay") for d in dd):   # 逐日写了 stay 就按逐日对齐（兼容红眼航班、首晚住机场）
        stay_seq = [ckey(d.get("stay")) if d.get("stay") else None for d in dd]
    else:
        stay_seq = []
        for r in route: stay_seq += [ckey(r.get("city"))] * (r.get("nights") or 0)
    for d in dd:
        dn = d.get("day"); ck = ckey(d.get("city"))
        moving = bool(d.get("from")) and ckey(d.get("from")) != ck
        if dn and dn <= len(stay_seq) and ck and stay_seq[dn - 1] and ck != stay_seq[dn - 1] and not city_matches(ck, stay_seq[dn - 1]):
            if region_of(ck, kbd) != region_of(stay_seq[dn - 1], kbd) and moving:
                warn("W_DAY_CITY_TRANSFER", f"Day {dn} 移动日：在 {d.get('city')} 游览后长途转往 {stay_seq[dn-1]} 过夜", "确认车程（司机日驾驶 ≤10h）并在 transport 写明", dn)
            elif region_of(ck, kbd) != region_of(stay_seq[dn - 1], kbd):
                err("E_DAY_CITY", f"Day {dn} 城市 {d.get('city')} 与 route 推算的过夜城市 {stay_seq[dn-1]} 不在同一区域", "对齐 route 与 days_detail", dn)
            else:
                warn("W_DAY_CITY", f"Day {dn} 活动城市 {d.get('city')} 与过夜城市 {stay_seq[dn-1]} 不同（同区域，按一日游处理）", "在 transport 写明往返", dn)
        spots = d.get("attractions") or []
        if len(spots) > max_spots: err("E_DENSITY", f"Day {dn} 排了 {len(spots)} 个景点，上限 {max_spots}（{tour_type}）", "拆到相邻天或改为可选", dn)
        is_transfer = bool(d.get("from")) and ckey(d.get("from")) != ck
        if is_transfer and len(spots) > max(4, max_spots - 3): warn("W_DENSITY_TRANSFER", f"Day {dn} 是移动日仍排 {len(spots)} 个景点", "移动日景点 ≤3", dn)
        if dn not in (1, len(dd)) and not spots and not is_transfer and tour_type != "self_guided": warn("W_EMPTY_DAY", f"Day {dn} 没有景点也不是移动日", "补景点或标明自由活动", dn)
        for s in spots:
            st = spot_city_status(s, ck, kbd, ckey(d.get("from")) if moving else None)
            if st == "unknown":
                warn("W_SPOT_UNKNOWN", f"Day {dn} 景点「{s}」不在景点池（{len(kbd['attractions'])} 个）里", "允许，但需人工核实名称与所在城市；或换成同城核心景点", dn)
            elif st == "daytrip":
                warn("W_SPOT_DAYTRIP", f"Day {dn} 景点「{s}」不在当天城市 {d.get('city')}，但在同一区域（可能是一日游）", "确认当天有往返交通并写进 transport", dn)
            elif st == "wrong" and moving:
                warn("W_SPOT_ENROUTE", f"Day {dn} 景点「{s}」不在出发城市也不在 {d.get('city')}（移动日途经？）", "确认是顺路停靠并核算车程", dn)
            elif st == "wrong":
                x = find_spot(s, kbd); where = [x["city_key"]] if x and x.get("city_key") else sorted(kbd["spot_cities"].get(norm(s), set())) or ["?"]
                err("E_SPOT_CITY", f"Day {dn} 景点「{s}」属于 {where}，当天城市是 {d.get('city')}（跨区域）", f"移到 {where[0]} 所在的那天", dn)
        if month:
            for s in spots:
                for sz in seasons:
                    if not re.search(sz["match"], s, re.I): continue
                    if not sz["months"]: err("E_SEASON_CLOSED", f"Day {dn}「{s}」：{sz['best']}", "", dn)
                    elif month not in sz["months"]: warn("W_SEASON", f"Day {dn}「{s}」最佳 {sz['best']}，出行月 {month} 不在范围", sz.get("note") or "", dn)
    # 5 机场
    if route and spec.get("entry_airport") and not airport_ok(spec["entry_airport"], rkeys[0]):
        warn("W_AIRPORT_ENTRY", f"进点 {spec['entry_airport']} 与首站 {route[0].get('city')} 距离较远", "首站改为机场所在城市，或在 Day 1 写明长途交通")
    if route and spec.get("exit_airport") and not airport_ok(spec["exit_airport"], rkeys[-1]):
        warn("W_AIRPORT_EXIT", f"出点 {spec['exit_airport']} 与末站 {route[-1].get('city')} 距离较远", "末站改为机场所在城市，或最后一天写明长途交通")
    # 5b 韩国特有：济州/郁陵岛必须飞或坐船；购物站数量
    legs = []
    for (ra, ka), (rb, kb_) in zip(zip(route, rkeys), zip(route[1:], rkeys[1:])):
        if ka in geo.CITIES and kb_ in geo.CITIES and (ka in ISLAND) != (kb_ in ISLAND):
            legday = next((d for d in dd if ckey(d.get("stay")) == kb_ or (ckey(d.get("city")) == kb_ and d.get("from"))), None)
            legs.append((ra.get("city"), rb.get("city"), legday))
    for d in dd:
        fk, ck2 = ckey(d.get("from")), ckey(d.get("city"))
        if fk in geo.CITIES and ck2 in geo.CITIES and (fk in ISLAND) != (ck2 in ISLAND) and not any(l[2] is d for l in legs): legs.append((d.get("from"), d.get("city"), d))
    for a_, b_, legday in legs:
        tr = ((legday or {}).get("transport") or "") + " " + ((legday or {}).get("title_cn") or "") + " " + ((legday or {}).get("title_en") or "")
        if not re.search(r"flight|fly|air|ferry|ship|boat|✈|航班|飞|船|cju|gmp|pus", tr, re.I):
            err("E_ISLAND_LEG", f"{a_} → {b_} 跨海（济州/郁陵岛）但 transport 未写航班或船", "transport 写明 Flight（如 GMP-CJU / CJU-PUS）或 Ferry", (legday or {}).get("day"))
    shop = [s for d in dd for s in (d.get("attractions") or []) if (find_spot(s, kbd) or {}).get("category") == "shopstop"]
    if tour_type == "group_coach" and len(shop) > 4:
        warn("W_SHOPSTOP", f"全程购物站 {len(shop)} 个（{'、'.join(shop[:6])}）", "市场跟团常见 3 个（人参/护肝宝/化妆品）；超过 4 个易遭投诉，需与地接确认并在行程写明")
    # 6 价格带（对标，非硬约束）
    fam = families.get(spec.get("family") or ""); pb = spec.get("price_band_usd")
    if fam and pb and fam.get("price_usd_min") and pb.get("min"):
        lo, hi = fam["price_usd_min"] * 0.7, (fam["price_usd_max"] or fam["price_usd_min"]) * 1.3
        if not (lo <= pb["min"] <= hi * 1.2): warn("W_PRICE_BAND", f"价格带 {pb} 偏离家族 {fam['id']} 市场带 USD {fam['price_usd_min']}–{fam['price_usd_max']}", "作为竞品对标参考，非硬约束")
    errors = [i for i in issues if i["level"] == "error"]; warns = [i for i in issues if i["level"] == "warn"]
    return errors, warns

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec"); ap.add_argument("--kb", default=os.path.join(HERE, "..", "kb")); ap.add_argument("--tour-type", default=None)
    ap.add_argument("--month", type=int, default=None); ap.add_argument("--json", action="store_true"); ap.add_argument("--max-spots", type=int, default=None)
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf-8"))
    errors, warns = validate_spec(spec, a.kb, a.tour_type, a.month, a.max_spots)
    route = spec.get("route") or []; dd = spec.get("days_detail") or []
    tour_type = a.tour_type or spec.get("tour_type") or "group_coach"
    if a.json:
        print(json.dumps({"ok": not errors, "errors": errors, "warnings": warns, "summary": {"days": spec.get("days"), "cities": len({ckey(r.get('city')) for r in route}), "spots": sum(len(d.get('attractions') or []) for d in dd)}}, ensure_ascii=False, indent=1))
    else:
        print(f"校验 {spec.get('code')} · {spec.get('title_cn') or spec.get('title_en')} · {spec.get('days')}D · {len(route)} 段 · tour_type={tour_type}")
        print(f"  error {len(errors)} / warn {len(warns)}")
        for i in errors + warns:
            print(f"  [{i['level'].upper()} {i['code']}]" + (f" D{i['day']}" if i.get('day') else "") + f" {i['msg']}" + (f" → {i['fix']}" if i.get('fix') else ""))
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
