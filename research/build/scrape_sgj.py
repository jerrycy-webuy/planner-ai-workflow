# -*- coding: utf-8 -*-
"""从已下载的 selfguidejapan.com 页面（Next.js RSC 数据）抽取线路与目的地。
用法: python3 -I scrape_sgj.py <fetch_dir> <out_dir>
  fetch_dir/tours/<CODE>.html, fetch_dir/destinations/<slug>.html
输出: out_dir/sgj_tours.json（与 consolidate.py 的线路 schema 一致）, out_dir/destinations.json, out_dir/sgj_tours_raw.json
"""
import sys, os, re, json, glob, html
FETCH, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

def rsc_text(h):
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)\s*</script>', h, re.S)
    out = []
    for c in chunks:
        try: out.append(json.loads('"' + c + '"'))
        except Exception: out.append(c.encode('utf-8').decode('unicode_escape', errors='ignore'))
    return "".join(out)

def match_object(txt, start):
    """从 txt[start]=='{' 或 '[' 起做括号匹配，返回结束下标（不含）。"""
    open_ch = txt[start]; close_ch = '}' if open_ch == '{' else ']'
    depth = 0; i = start; instr = False; esc = False
    while i < len(txt):
        ch = txt[i]
        if instr:
            if esc: esc = False
            elif ch == '\\': esc = True
            elif ch == '"': instr = False
        else:
            if ch == '"': instr = True
            elif ch in '{[': depth += 1
            elif ch in '}]':
                depth -= 1
                if depth == 0: return i + 1
        i += 1
    return None

def extract_after(txt, marker):
    """marker 形如 '{"tour":'：从 marker 自身的 '{' 开始解析整个父对象。"""
    i = txt.find(marker)
    if i < 0: return None
    j = i
    k = match_object(txt, j)
    if k is None: return None
    try: return json.loads(txt[j:k])
    except Exception as e:
        return None

def clean_undefined(o):
    if isinstance(o, dict): return {k: clean_undefined(v) for k, v in o.items()}
    if isinstance(o, list): return [clean_undefined(x) for x in o]
    if o == "$undefined": return None
    if isinstance(o, str) and o.startswith("$D"): return o[2:]
    return o

TRANSPORT_ICONS = "🚅🚃🚌🚕🚖⛴🚢🚠🚡🚗🚐✈🛳🚆🚇🚟🛥"
CITY_PREFIX = ["Tokyo", "Osaka", "Kyoto", "Nagoya", "Fukuoka", "Sapporo", "Hiroshima", "Kanazawa", "Kobe", "Yokohama", "Sendai", "Nara", "Hakata"]
CITY_FIX = {"karashiki": "Kurashiki", "kashikojima": "Kashikojima", "aichi-inuyama": "Inuyama", "hakuba tsugaike": "Hakuba (Tsugaike)", "hakuba wadano": "Hakuba (Wadano)", "hakuba misorano": "Hakuba (Misorano)",
            "osaka universal city": "Osaka (Universal City)", "osaka universal city ": "Osaka (Universal City)"}
def norm_city(loc):
    loc = (loc or "").strip()
    if not loc: return loc
    k = loc.lower().strip()
    if k in CITY_FIX: return CITY_FIX[k]
    for c in CITY_PREFIX:
        if k.startswith(c.lower() + " "):
            rest = loc[len(c):].strip()
            if rest.lower().startswith("universal"): return "Osaka (Universal City)"
            return c
    return loc[0].upper() + loc[1:]

STRIP_PREFIX = re.compile(r"^(the\s+)?(unesco\s+)?(world heritage site( of)?\s+|visit\s+(the\s+)?|explore\s+(the\s+)?|stroll along\s+(the\s+)?|lunch at\s+|walk\s+(the\s+)?|enjoy\s+(the\s+)?|see\s+(the\s+)?)", re.I)
STRIP_SUFFIX = re.compile(r"\s*(,\s*a world heritage site|\(.*?\)|®|™)\s*$", re.I)
def normalize_attraction(name):
    """拆分复合名称、去修饰，返回名称列表。"""
    n = name.strip()
    n = re.split(r"\s+-\s+|\s*:\s*|\s*–\s*|\s*→\s*", n)[0].strip()   # "Name - description" / "Name :description"
    n = STRIP_PREFIX.sub("", n); n = STRIP_SUFFIX.sub("", n).strip(" .,:;")
    if not n or n.endswith("?") or len(n) < 3: return []
    parts = re.split(r"\s*,\s*|\s+&\s+|\s+and\s+|\s*/\s*", n)
    out = []
    for p in parts:
        p = p.strip(" .")
        if len(p) < 3 or re.match(r"^(area|the town|town|town area)$", p, re.I): continue
        out.append(p)
    return out or [n]
def parse_day(d, meals_map, hotels_by_city, duration):
    desc = d.get("description") or ""
    lines = [l.strip() for l in desc.replace("\r", "").split("\n")]
    attractions, transport, activities, optional, notes = [], [], [], [], []
    for l in lines:
        if not l: continue
        if l.startswith("★") or l.startswith("☆"):
            body = l[1:].strip()
            parts = re.split(r"→|->|⇒", body, maxsplit=1)
            name = parts[0].strip(" :：")
            a_desc = parts[1].strip() if len(parts) > 1 else ""
            for nm in normalize_attraction(name):
                attractions.append({"name_en": nm, "desc": a_desc})
        elif l[0] in TRANSPORT_ICONS:
            transport.append(l)
        elif re.match(r"^(optional|\*optional)", l, re.I):
            optional.append(l)
        elif re.match(r"^<.*>$", l) or l.startswith("*Entrance"):
            continue
        else:
            activities.append(l)
    act_txt = " ".join(activities)
    act_txt = re.sub(r"\s+", " ", act_txt).strip()
    day_no = d.get("day")
    m = meals_map.get(day_no, {})
    meals = "".join(x for x, inc in (("B", m.get("breakfast")), ("L", m.get("lunch")), ("D", m.get("dinner"))) if inc) or None
    stay_city = d.get("destination") if (day_no is not None and duration and day_no < duration) else None
    return {
        "day": day_no, "title": d.get("title"), "from": None, "to": d.get("destination"),
        "transport": "; ".join(transport) if transport else (d.get("transportation") or None),
        "attractions": [a["name_en"] for a in attractions],
        "activities": act_txt[:1200] if act_txt else None,
        "meals": meals, "stay": stay_city, "notes": "; ".join(optional)[:600] if optional else None,
        "_attr_detail": attractions,
    }, attractions

def airports_from(text):
    t = text or ""
    found = []
    for pat, name in [(r"Haneda|Narita", "Tokyo (Haneda/Narita)"), (r"Kansai|KIX|Itami", "Osaka (KIX/ITM)"), (r"Fukuoka Airport", "Fukuoka"),
                      (r"New Chitose", "Sapporo (New Chitose)"), (r"Centrair|Chubu", "Nagoya (Centrair)"), (r"Aomori Airport", "Aomori")]:
        if re.search(pat, t): found.append(name)
    return found[0] if found else None

tours, raw = [], []
for fp in sorted(glob.glob(os.path.join(FETCH, "tours", "*.html"))):
    code = os.path.basename(fp)[:-5]
    h = open(fp, encoding="utf-8", errors="replace").read()
    txt = rsc_text(h)
    parent = extract_after(txt, '{"tour":')
    if not parent or not parent.get("tour"):
        print("NO TOUR OBJECT", code); continue
    t = clean_undefined(parent["tour"]); dests = clean_undefined(parent.get("destinations") or [])
    raw.append({"tour": t, "destinations": dests})
    duration = t.get("duration")
    meals_map = {m.get("day"): {"breakfast": (m.get("breakfast") or {}).get("included"), "lunch": (m.get("lunch") or {}).get("included"), "dinner": (m.get("dinner") or {}).get("included")} for m in (t.get("meals") or [])}
    acc = t.get("accommodations") or {}
    tiers = list(acc.keys())
    tier0 = acc.get(tiers[0]) if tiers else []
    route = [{"city": norm_city(a.get("location")), "nights": a.get("nights"), "hotel": a.get("name")} for a in (tier0 or [])]
    hotels = []
    for tier, lst in acc.items():
        for a in lst or []:
            hotels.append(f"{a.get('name')} ({a.get('location')}, {a.get('nights')}N{'' if tier in ('none','') else ', ' + tier})")
    days, attr_all = [], []
    prev_city = None
    for d in sorted(t.get("itinerary") or [], key=lambda x: x.get("day") or 0):
        pd, attrs = parse_day(d, meals_map, None, duration)
        pd["from"] = prev_city if (prev_city and prev_city != pd["to"]) else None
        prev_city = pd["to"] or prev_city
        for a in attrs: attr_all.append({"name_en": a["name_en"], "city": d.get("destination"), "description": a["desc"][:300]})
        days.append(pd)
    cp = t.get("currencyPricing") or {}
    usd = cp.get("USD") or {}
    alt = {k: {"min": v.get("min"), "max": v.get("max")} for k, v in cp.items() if k != "USD"}
    rec = {
        "code": code, "exists": True, "url": f"https://selfguidejapan.com/tours/{code}",
        "title_en": re.sub(r"\s*&\s*", " & ", (t.get("title") or "").replace("＆", "&")).strip(), "subtitle_en": t.get("subtitle") or None,
        "description_en": t.get("description") or None, "short_description": t.get("shortDescription") or None,
        "days": duration, "nights": (duration - 1) if duration else None,
        "price_min": usd.get("min"), "price_max": usd.get("max"), "currency": "USD" if usd else (next(iter(cp)) if cp else None),
        "price_note": "per person (site catalog price); " + "; ".join(f"{k} {v['min']}–{v['max']}" for k, v in alt.items()) if alt else "per person (site catalog price)",
        "price_pdf": usd.get("pdfUrl"),
        "series": re.match(r"[A-Z]+", code).group(0), "themes": [x.strip() for x in (t.get("experienceTypes") or []) if x and x.strip()],
        "season": None, "region_site": t.get("region"), "max_group_size": t.get("maxGroupSize"),
        "arrival_airport": t.get("startingPoint") or airports_from((t.get("itinerary") or [{}])[0].get("description") if t.get("itinerary") else ""),
        "departure_airport": t.get("endingPoint") or None,
        "route": [{"city": r["city"], "nights": r["nights"]} for r in route],
        "hotels": hotels, "accommodation_tiers": tiers,
        "day_by_day": [{k: v for k, v in d.items() if k != "_attr_detail"} for d in days],
        "inclusions": t.get("included") or [], "exclusions": t.get("notIncluded") or [],
        "highlights": t.get("highlights") or [], "important_information": t.get("importantInformation") or [], "tour_special": t.get("tourSpecial") or [],
        "destinations_ids": t.get("destinations") or [], "catalog_tags": t.get("catalogTags") or [],
        "attractions_all": attr_all,
        "source_confidence": "high", "sources": [f"https://selfguidejapan.com/tours/{code} (page data, direct fetch 2026-10-07)"],
        "notes": None, "rating": t.get("rating"), "updated_at": t.get("updatedAt"),
    }
    tours.append(rec)
json.dump(tours, open(os.path.join(OUT, "sgj_tours.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(raw, open(os.path.join(OUT, "sgj_tours_raw.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(f"tours: {len(tours)}; with day_by_day: {sum(1 for t in tours if t['day_by_day'])}; attractions (raw): {sum(len(t['attractions_all']) for t in tours)}")

# ---------- destinations ----------
dest_meta = {}
for fp in sorted(glob.glob(os.path.join(FETCH, "destinations", "*.html"))):
    slug = os.path.basename(fp)[:-5]
    h = open(fp, encoding="utf-8", errors="replace").read()
    txt = rsc_text(h)
    # 找含 nameJa 的、id==slug 的对象
    obj = None
    for m in re.finditer(r'\{"id":"' + re.escape(slug) + r'","name":"', txt):
        k = match_object(txt, m.start())
        try:
            cand = json.loads(txt[m.start():k])
            if "nameJa" in cand: obj = cand; break
        except Exception: continue
    # 页面文本段落：Why Visit / Best Time / Insider Tips
    h2 = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    def section(title):
        m = re.search(r"<h2[^>]*>\s*" + re.escape(title) + r"[^<]*</h2>(.*?)(?=<h2|</section>)", h2, re.S)
        if not m: return None
        s = re.sub(r"<[^>]+>", " ", m.group(1)); s = html.unescape(re.sub(r"\s+", " ", s)).strip()
        return s[:1500] or None
    obj = clean_undefined(obj or {})
    dest_meta[slug] = {
        "destination": obj.get("name") or slug.replace("-", " ").title(), "slug": slug, "name_ja": obj.get("nameJa"),
        "region": obj.get("region"), "prefecture": None, "latitude": obj.get("latitude"), "longitude": obj.get("longitude"),
        "url": f"https://selfguidejapan.com/destinations/{slug}", "blog_urls": [],
        "summary_en": (obj.get("description") or section("Why Visit " + (obj.get("name") or "")) or section("Why Visit")),
        "best_time": obj.get("bestTimeToVisit") or section("Best Time to Visit"), "insider_tips": section("Insider Tips"),
        "attractions": [{"name_en": x, "name_ja": None, "category": None, "description_en": None, "note": "destination highlight", "source": f"https://selfguidejapan.com/destinations/{slug}"} for x in (obj.get("highlights") or []) if isinstance(x, str)],
        "sources": [f"https://selfguidejapan.com/destinations/{slug}"],
    }
json.dump(list(dest_meta.values()), open(os.path.join(OUT, "destinations.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"destinations: {len(dest_meta)}; with nameJa: {sum(1 for d in dest_meta.values() if d['name_ja'])}; with region: {sum(1 for d in dest_meta.values() if d['region'])}")
