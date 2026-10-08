# -*- coding: utf-8 -*-
"""解析已下载的四站页面 → 统一线路 JSON（每站一个 raw/<site>_tours.json）。
用法: python3 -I parse_sources.py <fetch_dir> <out_data_dir>
  fetch_dir 下：cb/<entity_id>.json（Chan Brothers trip-detail API）· eu/<slug>.html · dyn/<slug>.html（Next.js RSC）
  KTE（koreatraveleasy.com）多日团页面格式各异，结构化结果直接写在 kte_multiday.py。
"""
import sys, os, re, json, glob, html as htmlmod
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geo_kr as geo
import names_kr as names
import kte_multiday

SGD_USD = 0.78  # 2026-10 参考汇率，仅用于跨站价格对标

def strip_html(s):
    s = re.sub(r"<br\s*/?>|</p>|</li>", "\n", s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s).replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", s).strip()

def md_plain(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s or "")
    return s.replace("**", "").replace("_", " ").strip()

def rsc(s):
    out = []
    for m in re.finditer(r"self\.__next_f\.push\((\[.*?\])\)</script>", s, flags=re.S):
        try:
            a = json.loads(m.group(1))
            if len(a) > 1 and isinstance(a[1], str): out.append(a[1])
        except Exception:
            pass
    return "".join(out)

def rsc_refs(s):
    """顺序解析 RSC 流：普通行「<id>:<json>\n」；文本块「<id>:T<hex 字节长度>,<内容>」（无换行，紧接下一条）。
    返回 {"$id": 文本}，逐日描述常以 "$32" 形式引用。"""
    b = s.encode("utf-8"); refs = {}; pos = 0; n = len(b)
    rx = re.compile(rb"([0-9a-f]{1,5}):")
    while pos < n:
        m = rx.match(b, pos)
        if not m:
            nl = b.find(b"\n", pos)
            if nl < 0: break
            pos = nl + 1; continue
        rid = m.group(1).decode(); p = m.end()
        if b[p:p + 1] == b"T":
            c = b.find(b",", p)
            ln = int(b[p + 1:c], 16)
            refs["$" + rid] = b[c + 1:c + 1 + ln].decode("utf-8", "ignore"); pos = c + 1 + ln
        else:
            nl = b.find(b"\n", p)
            pos = n if nl < 0 else nl + 1
    return refs

def deref(v, refs):
    if isinstance(v, str) and re.fullmatch(r"\$[0-9a-f]{1,4}", v): return refs.get(v, "")
    if isinstance(v, dict): return {k: deref(x, refs) for k, x in v.items()}
    if isinstance(v, list): return [deref(x, refs) for x in v]
    return v

_CITY_RX = None
def cities_in(text):
    """按出现顺序返回文本里的城市 key（只认城市表里的名字和常见别名）。"""
    global _CITY_RX
    if _CITY_RX is None:
        alts = {}
        for ck, (en, cn, reg) in geo.CITIES.items():
            alts[en.split(" (")[0].lower()] = ck
        alts.update({"jeju island": "jeju", "jenoju": "jeonju", "gangwon-do": "gangwon_region", "gangwondo": "gangwon_region", "ski resort": "gangwon_region",
                     "jinhae": "changwon", "everland": "yongin", "gyeonggido": "seoul", "gyeonggi-do": "seoul", "gyeonggi": "seoul", "seoraksan": "sokcho", "mount seorak": "sokcho"})
        _CITY_RX = (re.compile(r"\b(" + "|".join(sorted(map(re.escape, alts), key=len, reverse=True)) + r")\b", re.I), alts)
    rx, alts = _CITY_RX
    return [alts[m.group(1).lower()] for m in rx.finditer(text or "")]

def city_from_segment(seg):
    seg = re.sub(r"\(.*?\)|\(.*$", "", seg or "").strip(" -–—.,")
    k = geo.key_of(seg)
    if geo.is_city(k): return geo.CITIES[k][0], k
    # 片段里含城市名（如 "SKI RESORT"、"Gyeonggi-do"）
    low = seg.lower()
    if "ski" in low or "resort" in low: return "Pyeongchang", "pyeongchang"
    if "gyeonggi" in low: return "Seoul", "seoul"
    for ck, (en, cn, reg) in geo.CITIES.items():
        if re.search(r"\b" + re.escape(en.split(" (")[0].lower()) + r"\b", low): return en, ck
    return (seg.title() if seg else None), (k or None)

def split_title(name):
    name = re.sub(r"\(.*", "", htmlmod.unescape(name or "")).replace("&nbsp;", " ")
    return [p.strip() for p in re.split(r"\s+[-–—/]\s+|\s*–\s*|\s*—\s*", name) if p.strip()]

def meals_code(b, l, d):
    return "".join(c for c, f in (("B", b), ("L", l), ("D", d)) if f) or None

def spots(text, day_key):
    """词典抽景点；泛化条目的城市按当天城市。返回 (en 列表, 景点明细列表)。"""
    out, det = [], []
    for en, cn, ck, cat in names.match_all(text):
        if en in names.GENERIC: ck = day_key or ck
        out.append(en); det.append({"name_en": en, "name_cn": cn, "city_key": ck, "category": cat})
    return out, det

RESORT_CITY = [(r"vivaldi", "hongcheon"), (r"welli", "hoengseong"), (r"yongpyong|alpensia|phoenix|intercontinental alpensia|holiday inn.*alpensia|pyeongchang", "pyeongchang"),
               (r"elysian", "chuncheon"), (r"high ?1|high ?one|kangwon land", "jeongseon"), (r"sokcho|seorak", "sokcho"), (r"gangneung|seamarq|skybay", "gangneung"),
               (r"chuncheon|legoland", "chuncheon"), (r"hongcheon", "hongcheon")]
def fix_region_stays(dd):
    """「Gangwon-do / Ski Resort」这类区域名：按酒店名落到具体城市，落不到就记平昌（滑雪团最常见）。"""
    for d in dd:
        for f in ("key", "stay_key"):
            if d.get(f) == "gangwon_region" or (d.get(f) and not geo.is_city(d[f])):
                k = None
                for rx, ck in RESORT_CITY:
                    if re.search(rx, (d.get("hotel") or "") + " " + (d.get("desc") or "")[:400], re.I): k = ck; break
                k = k or ("pyeongchang" if d.get(f) == "gangwon_region" else d.get(f))
                if geo.is_city(k):
                    d[f] = k
                    if f == "key": d["city"] = geo.CITIES[k][0]
                    else: d["stay"] = geo.CITIES[k][0]

RESORT_CITY += [(r"bloom vista|yangpyeong", "yangpyeong"), (r"goyang|ilsan|sono calm", "goyang"), (r"marina ?bay seoul|gimpo", "gimpo"), (r"choochoo|gapyeong", "gapyeong")]
def _one_hotel_city(h):
    for rx, ck in RESORT_CITY:
        if re.search(rx, h, re.I): return ck
    ks = [k for k in cities_in(h) if geo.is_city(k)]
    return ks[-1] if ks else None

def hotel_city(h, current=None):
    """多选酒店（A or B or C）：任一选项在当前城市就保留；否则用第一个能识别城市的选项。"""
    if not h: return None
    opts = [o for o in re.split(r"\s+or\s+(?!similar)|\s*/\s*", h) if o.strip()]
    cs = [c for c in (_one_hotel_city(o) for o in opts) if c]
    if current in cs: return current
    return cs[0] if cs else None

def fix_stays_by_hotel(dd):
    """酒店名里带城市（Hotel Inter-Burgo Daegu、Elysian Gangchon…）且与推算的过夜城市不同 → 以酒店为准。"""
    for d in dd:
        if not d.get("stay") or not d.get("hotel"): continue
        hk = hotel_city(d["hotel"], d.get("stay_key"))
        if hk and hk != d.get("stay_key"):
            if d.get("key") == d.get("stay_key"):   # 当天终点也跟着改，原终点记为出发地
                d["from"] = d.get("from") or d.get("city")
                d["key"], d["city"] = hk, geo.CITIES[hk][0]
            d["stay_key"], d["stay"] = hk, geo.CITIES[hk][0]

def build_route(days_detail):
    fix_region_stays(days_detail)
    fix_stays_by_hotel(days_detail)
    route = []
    for d in days_detail:
        if not d.get("stay"): continue
        k = d.get("stay_key")
        if route and route[-1]["key"] == k: route[-1]["nights"] += 1
        else: route.append({"city": d["stay"], "key": k, "nights": 1})
    return route

def hotels_from_days(days_detail):
    out = []
    for d in days_detail:
        h = d.get("hotel")
        if not h: continue
        if out and out[-1]["name"] == h and out[-1]["city_key"] == d.get("stay_key"): out[-1]["nights"] += 1
        else: out.append({"name": h, "city": d.get("stay"), "city_key": d.get("stay_key"), "nights": 1})
    return out

# ---------------- Chan Brothers ----------------
def parse_cb(fp):
    d = json.load(open(fp, encoding="utf-8"))
    its = d.get("field_n_t_itinerary") or []
    if not its: return None
    style = (d.get("field_n_t_travel_style") or {}).get("name", "")
    tour_type = {"Package Tours": "group_coach", "Free & Easy+": "self_guided", "Private Tours": "private_custom"}.get(style, "group_coach")
    dd = []
    for i, day in enumerate(its, 1):
        route = [r.get("field_p_ir_location_city") for r in (day.get("field_p_i_route") or []) if r.get("field_p_ir_location_city")]
        modes = [((r.get("field_p_ir_mode") or {}).get("name")) for r in (day.get("field_p_i_route") or [])]
        modes = [m for m in modes if m]
        acc = day.get("field_p_i_accommodation") or []
        desc = md_plain(day.get("field_p_i_description") or "")
        hl = [h.strip() for h in (day.get("field_p_i_highlight") or []) if h and h.strip()]
        last_city, last_key = city_from_segment(route[-1]) if route else (None, None)
        first_city, first_key = city_from_segment(route[0]) if route else (None, None)
        meals = {m.get("field_p_mc_meal") for m in (day.get("field_p_i_meals_with_description") or [])}
        meal_desc = [f"{m.get('field_p_mc_meal')}: {m.get('field_p_short_description')}" for m in (day.get("field_p_i_meals_with_description") or []) if m.get("field_p_short_description")]
        a, det = spots(" ; ".join(hl) + " ; " + desc, last_key)
        title = " – ".join(route) if route else None
        dd.append({"day": i, "city": last_city, "key": last_key, "from": first_city if first_key != last_key else None,
                   "transport": " / ".join(dict.fromkeys(modes)) or None, "attractions": a, "attractions_detail": det, "highlights_raw": hl,
                   "meals": meals_code("Breakfast" in meals, "Lunch" in meals, "Dinner" in meals), "meals_desc": meal_desc,
                   "stay": last_city if acc else None, "stay_key": last_key if acc else None, "hotel": acc[0] if acc else None, "title": title,
                   "desc": desc[:1500]})
    price = d.get("field_n_t_sale_price")
    title = (d.get("field_n_t_itinerary_name") or d.get("title") or "").strip()
    code = d.get("field_n_t_tour_code") or f"CB-{d.get('entity_id')}"
    days = int(d.get("field_n_t_travel_duration") or len(its))
    if days < len(its): days = len(its)
    t = {"code": code, "site": "CB", "source": "chanbrothers.com", "url": "https://www.chanbrothers.com" + d.get("path_alias", ""), "tour_type": tour_type,
         "style": style, "title_en": title.title() if title.isupper() else title, "title_cn": (d.get("field_n_t_chinese_title") or "").strip() or None,
         "days": days, "nights": sum(1 for x in dd if x["stay"]), "season": d.get("field_n_t_season"),
         "price": {"min": float(price) if price else None, "max": float(d["field_n_t_price"]) if d.get("field_n_t_price") else None, "currency": "SGD",
                   "note": "站点「From」促销价 / 原价，每人、两人一房、含新加坡往返机票（税燃另计）"},
         "airlines": d.get("field_n_t_airline") or [], "cities_listed": d.get("field_n_t_city") or [],
         "days_detail": dd, "inclusions": [x.strip("* ").strip() for x in ((d.get("field_n_t_inclusions") or {}).get("text") or "").split("\n") if x.strip("* ").strip()],
         "exclusions": [x.strip("* ").strip() for x in ((d.get("field_n_t_exclusions") or {}).get("text") or "").split("\n") if x.strip("* ").strip()],
         "highlights": [d.get("field_n_t_description_text") or "", d.get("field_n_t_write_up") or ""],
         "meals_featured": d.get("field_n_t_custom_meals") or [],
         "remarks": ((d.get("field_n_t_itinerary_remarks") or {}).get("text") or "")[:1200]}
    t["route"] = build_route(dd); t["hotels"] = hotels_from_days(dd)
    return t

# ---------------- EU Holidays / Dynasty（同一 Tourix 后台） ----------------
def hotels_block(txt):
    """EU 亮点块里的「2N Jeju Best Western Hotel」。"""
    out = []
    for m in re.finditer(r"(\d)N\s*\n?\s*([^\n]+)", txt):
        name = m.group(2).strip()
        if len(name) > 3 and not name.lower().startswith(("glamping",)) or "glamping" in name.lower():
            out.append({"nights": int(m.group(1)), "name": name})
    return out

def assign_stays(dd, nights, hotel_list=None):
    """无逐日酒店时：按总夜数从后往前排（首日红眼航班不住）——第 k+1..k+N 天住当天终点城市。"""
    D = len(dd); k = max(0, (D - 1) - nights)
    for i, d in enumerate(dd):
        if k <= i < k + nights and d.get("key") and d["key"] != "singapore":
            d["stay"], d["stay_key"] = d["city"], d["key"]
    if hotel_list:
        # 按夜数顺序把酒店名铺到住宿日
        seq = []
        for h in hotel_list: seq += [h["name"]] * h["nights"]
        stays = [d for d in dd if d.get("stay")]
        for d, h in zip(stays, seq): d["hotel"] = h

def parse_tourix_days(days, lang_key="EN", refs=None):
    days = deref(days, refs or {})
    dd = []; prev = (None, None)
    for i, x in enumerate(days, 1):
        name = (x.get("name") or {}).get(lang_key) or ""
        title = re.sub(r"\(.*", "", strip_html(name))
        keys = [k for k in cities_in(title) if k != "singapore"]
        if not keys and x.get("itineraryCities"): keys = [k for k in cities_in(x["itineraryCities"]) if k]
        if keys:
            key = keys[-1]; city = geo.CITIES[key][0] if key in geo.CITIES else "Gangwon-do"
            frm = (geo.CITIES[keys[0]][0] if keys[0] in geo.CITIES else "Gangwon-do") if len(keys) > 1 and keys[0] != key else None
        else:
            city, key = prev; frm = None
        prev = (city, key)
        desc = strip_html((x.get("description") or {}).get(lang_key) or "")
        desc_cn = strip_html((x.get("description") or {}).get("CN") or "")
        hotel = None
        m = re.search(r"Accommodation\s*:\s*([^\n]+)", desc)
        if m: hotel = m.group(1).strip(" .")
        desc_noacc = re.sub(r"Accommodation\s*:[^\n]+", "", desc)
        a, det = spots(desc_noacc, key)
        def has(f): return bool((x.get(f) or {}).get("EN") or (x.get(f) or {}).get("CN"))
        dd.append({"day": i, "city": city, "key": key, "from": frm, "transport": "Flight" if re.search(r"\bflights?\b|\bfly\b|\bflies\b", desc, re.I) and i not in (1, len(days)) else
                   ("KTX" if re.search(r"\bKTX\b|high-speed (?:train|rail)", desc, re.I) else None),
                   "attractions": a, "attractions_detail": det, "highlights_raw": [],
                   "meals": meals_code(has("breakfast"), has("lunch"), has("dinner")),
                   "meals_desc": [f"{k.title()}: {strip_html((x.get(k) or {}).get('EN'))}" for k in ("breakfast", "lunch", "dinner") if (x.get(k) or {}).get("EN") and "&" not in (x.get(k) or {}).get("EN", "")],
                   "stay": None, "stay_key": None, "hotel": hotel, "title": strip_html(name), "title_cn": strip_html((x.get("name") or {}).get("CN") or "") or None,
                   "desc": desc[:1500], "desc_cn": desc_cn[:800] or None})
    return dd

def _en(v):
    if isinstance(v, dict): return v.get("EN") or ""
    return v if isinstance(v, str) and not v.startswith("$") else ""

def parse_eu(fp):
    raw = open(fp, encoding="utf-8").read(); s = rsc(raw)
    j = s.find('"tour":{"id"')
    if j < 0: return None
    t, _ = json.JSONDecoder().raw_decode(s, j + 7)
    its = (t.get("itinerary") or [{}])[0].get("details", {}).get("itineraries") or []
    if not its: return None
    refs = rsc_refs(s)
    dd = parse_tourix_days(its, refs=refs)
    hl_html = ""
    if t.get("highlights", "").startswith("$"):
        ref = t["highlights"][1:]
        m = re.search(r"(?:^|[\n\]}])" + re.escape(ref) + r":T([0-9a-f]+),", s)
        if m: hl_html = s[m.end(): m.end() + int(m.group(1), 16) * 2]
    else:
        hl_html = t.get("highlights") or ""
    hl_txt = strip_html(hl_html)
    acc_part = hl_txt[hl_txt.find("ACCOM"):] if "ACCOM" in hl_txt else ""
    acc_part = acc_part.split("* Note")[0].split("Service Fee")[0]
    hlist = hotels_block(acc_part)
    assign_stays(dd, int(t.get("nights") or 0), hlist)
    deps = []
    for x in t.get("departureDates") or []:
        deps.append({"code": x.get("code"), "date": x.get("date"), "status": x.get("status"), "airline": x.get("airline"),
                     "twin": x.get("adultPricing", {}).get("twin"), "single": x.get("adultPricing", {}).get("single"),
                     "child_with_bed": x.get("childPricing", {}).get("withBed"), "child_no_bed": x.get("childPricing", {}).get("noBed"),
                     "tax": x.get("adultPricing", {}).get("taxFees"), "flights": [f"{f.get('route')} {f.get('flight','').strip()} {f.get('depart')}-{f.get('arrive')}" for f in x.get("flightItinerary") or []]})
    def num(v):
        try: return float(re.sub(r"[^\d.]", "", v))
        except Exception: return None
    twins = [num(x["twin"]) for x in deps if x.get("twin")]
    pmin = min(twins) if twins else num(t.get("price") or "")
    hl_items = [ln.strip("• ").strip() for ln in hl_txt.split("\n") if ln.strip().startswith("•")]
    slug = os.path.basename(fp)[:-5]
    out = {"code": t.get("id"), "site": "EU", "source": "euholidays.com.sg", "url": f"https://www.euholidays.com.sg/tours/{slug}", "tour_type": "group_coach",
           "style": "Group Holidays", "title_en": htmlmod.unescape(t.get("title") or ""), "title_cn": None, "days": int(t.get("duration") or len(dd)),
           "nights": int(t.get("nights") or 0), "season": re.search(r"\(([^)]*)\)", t.get("title") or "").group(1) if "(" in (t.get("title") or "") else None,
           "price": {"min": pmin, "max": max(twins) if twins else pmin, "currency": "SGD", "note": "按出发日期成人双人房价，含新加坡往返机票（税燃另计）"},
           "departures": deps, "days_detail": dd, "inclusions": [], "exclusions": [], "highlights": hl_items,
           "service_fee": (re.search(r"KRW[\d,]+ per person", hl_txt) or [None])[0], "remarks": strip_html(_en(t.get("importantNote")))[:1200]}
    # 中文标题：第一天之外的 CN 标题拼不出整团名，留空
    out["route"] = build_route(dd); out["hotels"] = hotels_from_days(dd)
    return out

def parse_dyn(fp):
    raw = open(fp, encoding="utf-8").read(); s = rsc(raw)
    i = s.find('"tourData":')
    if i < 0: return None
    t, _ = json.JSONDecoder().raw_decode(s, i + len('"tourData":'))
    j = s.find('[{"seq":1')
    if j < 0: return None
    its, _ = json.JSONDecoder().raw_decode(s, j)
    dd = parse_tourix_days(its, refs=rsc_refs(s))
    # Dynasty 逐日描述里写了 Accommodation；有酒店的天 = 住宿
    has_hotel = any(d.get("hotel") for d in dd)
    if has_hotel:
        for d in dd:
            if d.get("hotel"): d["stay"], d["stay_key"] = d["city"], d["key"]
        # 同一酒店连住时页面只在第一天写，补齐到 nights
        n = int(t.get("nights") or 0); cur = None
        stays = sum(1 for d in dd if d.get("stay"))
        if stays < n:
            for d in dd[:-1]:
                if d.get("hotel"): cur = d["hotel"]
                elif cur and d.get("key") and not d.get("stay"):
                    d["stay"], d["stay_key"], d["hotel"] = d["city"], d["key"], cur
    else:
        assign_stays(dd, int(t.get("nights") or 0))
    name = t.get("name") or {}
    out = {"code": t.get("productCode"), "site": "DYN", "source": "dynastytravel.com.sg", "url": "https://www.dynastytravel.com.sg/" + (t.get("uri") or ""),
           "tour_type": "group_coach", "style": "Premium small group", "title_en": htmlmod.unescape(name.get("EN") or ""), "title_cn": name.get("CN") or None,
           "days": int(t.get("duration") or len(dd)), "nights": int(t.get("nights") or 0), "season": None,
           "price": {"min": float(t.get("price") or 0) or None, "max": None, "currency": "SGD", "note": "站点「From」价，每人、两人一房、含新加坡往返机票"},
           "themes": t.get("tags") or [], "days_detail": dd, "inclusions": [], "exclusions": [],
           "highlights": [strip_html((t.get("shortDescription") or {}).get("EN") or "")], "remarks": strip_html((t.get("importantNote") or {}).get("EN") or "")[:1200]}
    out["route"] = build_route(dd); out["hotels"] = hotels_from_days(dd)
    return out

def parse_kte():
    out = []
    for t in kte_multiday.TOURS:
        dd = []
        for i, x in enumerate(t["days"], 1):
            city, key = city_from_segment(x["city"])
            frm = city_from_segment(x["from"])[0] if x.get("from") else None
            a, det = spots(" ; ".join(x.get("spots") or []), key)
            stay = city_from_segment(x["stay"]) if x.get("stay") else (None, None)
            dd.append({"day": i, "city": city, "key": key, "from": frm, "transport": x.get("transport"), "attractions": a, "attractions_detail": det,
                       "highlights_raw": x.get("spots") or [], "meals": x.get("meals"), "meals_desc": [], "stay": stay[0], "stay_key": stay[1],
                       "hotel": x.get("hotel"), "title": x.get("title"), "desc": " ; ".join(x.get("spots") or [])})
        r = dict(t); r.pop("days")
        r.update({"site": "KTE", "source": "koreatraveleasy.com", "days_detail": dd, "days": len(dd), "nights": sum(1 for d in dd if d["stay"])})
        r["route"] = build_route(dd); r["hotels"] = hotels_from_days(dd)
        out.append(r)
    return out

def main():
    fetch, out = sys.argv[1], sys.argv[2]
    res = {"chanbrothers": [], "euholidays": [], "dynastytravel": [], "koreatraveleasy": parse_kte()}
    for fp in sorted(glob.glob(os.path.join(fetch, "cb", "*.json"))):
        t = parse_cb(fp)
        if t: res["chanbrothers"].append(t)
    for fp in sorted(glob.glob(os.path.join(fetch, "eu", "*.html"))):
        t = parse_eu(fp)
        if t: res["euholidays"].append(t)
    for fp in sorted(glob.glob(os.path.join(fetch, "dyn", "*.html"))):
        t = parse_dyn(fp)
        if t: res["dynastytravel"].append(t)
    for site, tours in res.items():
        os.makedirs(os.path.join(out, site, "raw"), exist_ok=True)
        json.dump(tours, open(os.path.join(out, site, "raw", f"{site}_tours.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(site, len(tours))

if __name__ == "__main__":
    main()
