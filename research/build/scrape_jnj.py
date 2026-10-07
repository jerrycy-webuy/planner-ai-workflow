# -*- coding: utf-8 -*-
"""从已下载的 japan-navi-journey.com 页面抽取行程与目的地景点。
用法: python3 -I scrape_jnj.py <fetch_dir> <out_dir>
  fetch_dir/itinerary/<slug>.html, fetch_dir/itinerary_index.html, fetch_dir/column/<id>.html
输出: out_dir/jnj_itineraries.json, out_dir/destinations.json
"""
import sys, os, re, json, glob, html
FETCH, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

def strip_tags(s):
    s = re.sub(r"<br\s*/?>", "\n", s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"[ \t]+", " ", s).strip()

def clean(h):
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", "", h, flags=re.S)
    h = re.sub(r"<noscript>.*?</noscript>", "", h, flags=re.S)
    return h

# ---------- 地名/景点启发式抽取 ----------
PLACE_SUFFIX = r"(?:Shrine|Temple|Castle|Falls|Waterfall|Lake|Gorge|Onsen|Park|Museum|Market|Island|Pass|Bridge|Garden|Gardens|Port|Beach|Village|Valley|Ropeway|Plateau|Peninsula|Cape|Tower|Hot Spring|Aquarium|Zoo|Winery|Brewery|Distillery|Coast|Cliffs|Trail|Street|Ruins|Hall|Center|Centre|Farm|Observatory|Mountain|Cirque|Pond|River|Bay|Highlands|Shopping Street|Old Town|Festival|Station|Cave|Caves|Forest|Marsh|Monument|Workshop|Kiln|Pavilion|Resort)"
PLACE_RE = re.compile(r"\b((?:Mt\.?|Mount|Lake|Cape)\s+[A-Z][\w’'ōūōāīéŌŪ-]+|(?:\d+(?:st|nd|rd|th)\s+)?[A-Z][\w’'ōūāīéŌŪ-]+(?:\s+(?:no|of|the|de)\s+[A-Z][\w’'ōūāīéŌŪ-]+)?(?:\s+[A-Z][\w’'ōūāīéŌŪ-]+){0,3}\s+" + PLACE_SUFFIX + r")\b")
GENERIC = re.compile(r"^(The |A |An )?(Hot Spring|Onsen|Castle|Temple|Shrine|Park|Museum|Market|Island|Lake|Mount|Mountain|Festival|Station|Garden|Village|Valley|Port|Beach|Tower|Resort|Winery|Brewery|Farm|Trail|Street)s?$", re.I)
def find_places(text):
    out = []
    for m in PLACE_RE.finditer(text or ""):
        name = m.group(1).strip()
        name = re.sub(r"^(Visit|Explore|Enjoy|Stroll|Walk|See|Take|Head|Begin|Spend|Stop|Continue|Then|At|In|Morning|Afternoon|Evening|Late|Early|Day|Night|Next|Your|Our|The|A|An)\s+", "", name)
        if GENERIC.match(name) or len(name) < 5: continue
        if name not in out: out.append(name)
    return out

# ---------- index: region tag + days ----------
idx = clean(open(os.path.join(FETCH, "itinerary_index.html"), encoding="utf-8", errors="replace").read())
cards = {}
for m in re.finditer(r'<a href="https://japan-navi-journey\.com/itinerary/([^/"]+)/"[^>]*class="p-panel-a[^"]*">(.*?)</a>', idx, re.S):
    slug, body = m.group(1), m.group(2)
    tags = [strip_tags(x) for x in re.findall(r'class="c-tag"[^>]*>(.*?)</p>', body, re.S)]
    days = re.search(r'p-panel-a__day">\s*ex\s*(\d+)\s*day', body, re.I)
    title = re.search(r'p-panel-a__ttl[^"]*">(.*?)</p>', body, re.S)
    cards[slug] = {"tags": tags, "days": int(days.group(1)) if days else None, "title": strip_tags(title.group(1)) if title else None}
print("index cards:", len(cards))

REGION_OF = {"Aomori": "Tohoku", "Miyagi": "Tohoku", "Iwate": "Tohoku", "Yamagata": "Tohoku", "Akita": "Tohoku", "Fukushima": "Tohoku",
             "Nagano": "Chubu", "Niigata": "Chubu", "Aichi": "Chubu", "Gifu": "Chubu", "Toyama": "Hokuriku", "Ishikawa": "Hokuriku",
             "Tochigi": "Kanto", "Tokyo": "Kanto", "Kanagawa": "Kanto", "Osaka": "Kansai", "Kyoto": "Kansai", "Nara": "Kansai", "Hyogo": "Kansai",
             "Fukuoka": "Kyushu", "Oita": "Kyushu", "Kumamoto": "Kyushu", "Nagasaki": "Kyushu", "Hokkaido": "Hokkaido"}

ROUTE_OVERRIDE = {
    "aichi-nagoya-chita": (["Nagoya", "Nagoya", "Chita Peninsula", None], [("Nagoya", 2), ("Chita Peninsula", 1)]),
    "aomori-unveiled": (["Hakkoda / Oirase", "Goshogawara", "Shimokita Peninsula", "Hachinohe", "Hachinohe", "Hachinohe", None], [("Hakkoda / Oirase", 1), ("Goshogawara", 1), ("Shimokita Peninsula", 1), ("Hachinohe", 3)]),
    "discover-fukuoka": (["Itoshima", "Kurume", "Ukiha", "Munakata", "Fukuoka", None], [("Itoshima", 1), ("Kurume", 1), ("Ukiha", 1), ("Munakata", 1), ("Fukuoka", 1)]),
    "eastern-nagano-escape": (["Karuizawa", "Saku", "Komoro", "Tomi", None], [("Karuizawa", 1), ("Saku", 1), ("Komoro", 1), ("Tomi", 1)]),
    "nagano-premium-retreat": (["Matsumoto", "Suwa", "Ina", "Hirugami Onsen", "Hirugami Onsen", "Kiso", None], [("Matsumoto", 1), ("Suwa", 1), ("Ina", 1), ("Hirugami Onsen", 2), ("Kiso", 1)]),
    "nikko": (["Nikko", "Oku-Nikko", "Tochigi City", None], [("Nikko", 1), ("Oku-Nikko", 1), ("Tochigi City", 1)]),
    "osaka-5days": (["Osaka (Sakai)", "Osaka (Sakai)", "Osaka (Sakai)", "Osaka (Sakai)", None], [("Osaka (Sakai)", 4)]),
    "premium-tohoku-gourmet-tour": (["Shimokita Peninsula", "Oma", "Aomori City", "Sendai", None], [("Shimokita Peninsula", 1), ("Oma", 1), ("Aomori City", 1), ("Sendai", 1)]),
    "sado-island": (["Sado Island", "Sado Island", "Sado Island", None], [("Sado Island", 3)]),
    "slow-travel-in-tsugaru": (["Hirosaki (Mt. Iwaki)", "Hirosaki (Mt. Iwaki)", None], [("Hirosaki (Mt. Iwaki)", 2)]),
    "tokyo-tohoku-snow-monsters-onsen": (["Kakunodate", "Nyuto Onsen", "Aomori City", "Aizu-Wakamatsu", "Aizu-Wakamatsu", "Sendai", "Sendai", "Sendai", "Tokyo", None], [("Kakunodate", 1), ("Nyuto Onsen", 1), ("Aomori City", 1), ("Aizu-Wakamatsu", 2), ("Sendai", 3), ("Tokyo", 1)]),
}
itins = []
for fp in sorted(glob.glob(os.path.join(FETCH, "itinerary", "*.html"))):
    slug = os.path.basename(fp)[:-5]
    h = clean(open(fp, encoding="utf-8", errors="replace").read())
    title = re.search(r'<h1 class="itinerary-mv__ttl">(.*?)</h1>', h, re.S)
    intro = re.search(r'<div class="itinerary-mv__txt">(.*?)</div>', h, re.S)
    days_m = re.search(r'itinerary-sect-c__head-days">\s*ex\s*(\d+)\s*Days?', h, re.I)
    subtitle = re.search(r'itinerary-sect-c__head-txt-main">(.*?)</p>', h, re.S)
    day_blocks = re.findall(r'<div class="itinerary-day js-fadeIn-up">(.*?)(?=<div class="itinerary-day js-fadeIn-up">|<section class="itinerary-detail)', h, re.S)
    days = []
    for b in day_blocks:
        num = re.search(r'__head-num">\s*(\d+)', b)
        ttl_lg = re.search(r'itinerary-day__ttl-lg[^"]*">(.*?)</h3>', b, re.S)
        ttl = re.search(r'<h4 class="itinerary-day__ttl[^"]*">(.*?)</h4>', b, re.S)
        txt = re.search(r'<div class="itinerary-day__txt">(.*?)</div>', b, re.S)
        route = strip_tags(ttl_lg.group(1)) if ttl_lg else ""
        HYPHEN_NAMES = ["Shin-Aomori", "Oku-Nikko", "Kii-Katsuura", "Shin-Osaka", "Shin-Hakodate", "Shin-Yokohama", "Oku-Yagen", "Oku-Hida", "Kami-Kochi", "Nachi-Katsuura", "Ise-Shima", "Tokyo-Narita", "Oku-Matsushima", "Jo-mon"]
        protected = route
        for hn in HYPHEN_NAMES: protected = protected.replace(hn, hn.replace("-", "§"))
        parts = [p.strip().replace("§", "-") for p in re.split(r"\s*[-–—－‐]\s*|・|/|→|⇒", protected) if p.strip()]
        paras = [strip_tags(p) for p in re.findall(r"<p>(.*?)</p>", txt.group(1), re.S)] if txt else []
        days.append({
            "day": int(num.group(1)) if num else None, "title": (strip_tags(ttl.group(1)).split("\n")[0] if ttl else None),
            "route_text": route, "from": parts[0] if len(parts) > 1 else None, "to": parts[-1] if parts else None,
            "transport": "private vehicle with driver", "attractions": find_places(" ".join(paras)), "activities": " ".join(paras)[:1500] or None,
            "meals": None, "stay": parts[-1] if parts else None, "notes": None,
        })
    # 最后一天通常是离境，stay=None
    if days: days[-1]["stay"] = None
    if slug in ROUTE_OVERRIDE:
        stays, _ = ROUTE_OVERRIDE[slug]
        prev = None
        for i, d in enumerate(days):
            st = stays[i] if i < len(stays) else None
            d["stay"] = st
            d["to"] = st or (d["to"] if d["to"] and len(d["to"]) < 30 else None)
            d["from"] = prev if (prev and prev != d["to"]) else None
            prev = d["to"] or prev
    inc = [strip_tags(x) for x in re.findall(r'<ul class="c-list-disc">(.*?)</ul>', h, re.S) for x in [x]]
    inc_items = []
    for ul in re.findall(r'<ul class="c-list-disc">(.*?)</ul>', h, re.S):
        inc_items += [strip_tags(li) for li in re.findall(r"<li>(.*?)</li>", ul, re.S)]
    notes = []
    for ul in re.findall(r'<ul class="c-list-asterisk[^"]*">(.*?)</ul>', h, re.S):
        notes += [strip_tags(li) for li in re.findall(r"<li>(.*?)</li>", ul, re.S)]
    prices = {int(k): v for k, v in re.findall(r'data-price-(\d)="([^"]*)"', h)}
    def jpy(v):
        m = re.search(r"([\d,]+)", v or ""); return int(m.group(1).replace(",", "")) if m else None
    price_map = {k: jpy(v) for k, v in prices.items()}
    card = cards.get(slug, {})
    tags = card.get("tags") or []
    pref = tags[0].split("（")[0].split("(")[0].strip() if tags else None
    n_days = int(days_m.group(1)) if days_m else card.get("days")
    # route: 人工校正表优先，否则按住宿地压缩
    if slug in ROUTE_OVERRIDE:
        route = [{"city": c, "nights": n} for c, n in ROUTE_OVERRIDE[slug][1]]
    else:
        route = []
        for d in days[:-1] if len(days) > 1 else days:
            c = d["to"]
            if not c: continue
            if route and route[-1]["city"] == c: route[-1]["nights"] += 1
            else: route.append({"city": c, "nights": 1})
    code = "JNJ-" + slug.upper()
    itins.append({
        "code": code, "exists": True, "url": f"https://japan-navi-journey.com/itinerary/{slug}/",
        "title_en": (lambda h1, ct: (ct if (ct and h1 and ct.startswith(h1)) else (h1 or ct)))(strip_tags(title.group(1)).split("\n")[0].strip() if title else None, card.get("title")),
        "subtitle_en": (strip_tags(subtitle.group(1)) if subtitle else None) or (strip_tags(title.group(1)).split("\n")[1].strip() if title and "\n" in strip_tags(title.group(1)) else None),
        "description_en": " ".join(strip_tags(p) for p in re.findall(r"<p>(.*?)</p>", intro.group(1), re.S)) if intro else None,
        "days": n_days, "nights": (n_days - 1) if n_days else None,
        "price_min": price_map.get(5) or min([v for v in price_map.values() if v] or [None]) if price_map else None,
        "price_max": price_map.get(2) or max([v for v in price_map.values() if v] or [None]) if price_map else None,
        "currency": "JPY" if price_map else None,
        "price_note": ("JPY per person, from; by group size: " + ", ".join(f"{k} pax {v:,}" for k, v in sorted(price_map.items()) if v) + " (sample quotation incl. private vehicle, guide, hotels & meals)") if price_map else "custom quote",
        "price_by_group_size_jpy": price_map,
        "series": "JNJ", "themes": ["Private custom tour"] + ([t for t in tags] if tags else []), "season": None,
        "tour_type": "private custom tour: private vehicle with driver + English-speaking guide",
        "region": REGION_OF.get(pref or "", None), "prefectures": [pref] if pref else [],
        "arrival_airport": days[0]["from"] if days and days[0]["from"] else None, "departure_airport": None,
        "route": route, "hotels": [], "day_by_day": days,
        "inclusions": inc_items, "exclusions": [], "highlights": [d["title"] for d in days if d.get("title")],
        "attractions_all": [{"name_en": a, "city": d["to"]} for d in days for a in d["attractions"]], "source_confidence": "high",
        "sources": [f"https://japan-navi-journey.com/itinerary/{slug}/ (direct fetch 2026-10-07)"], "notes": "; ".join(notes)[:800] or None,
    })
json.dump(itins, open(os.path.join(OUT, "jnj_itineraries.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("itineraries:", len(itins), "| with price:", sum(1 for x in itins if x["currency"]), "| days parsed:", [(x["code"][4:], len(x["day_by_day"]), x["days"]) for x in itins])

# ---------- columns → destinations/attractions ----------
STOP2 = re.compile(r"(plan your|continue your|await|overview|bloom|performances|kids experience|nearby attractions|quick history|level$|beginner|advanced|intermediate|other attractions|^(winter|spring|summer|autumn)$|the winery experience|^history of|^grounds of|^beauty of|^experience |^try |bite into|warm up|^down at|^through the|^inside the|^wander the|lesson|^traditional crafts$|^lush gardens$|^private onsen$|^living village$|shopping spots|local dishes|department store|^(the )?four areas|^walking trail$|^lover|^crafting|^diverse|^attend|^interactive|^cycle the|^samurai residences$|^gold leaf workshops$|^japan’s highest|^along the|^beyond the|^samurai school$)", re.I)
STOP = re.compile(r"^(planning|subscribe|conclusion|final|summary|faq|how to|getting|access|why |what |when |where |tips|introduction|itinerary|day \d|things to do|overview|best time|about |travel |a (relaxing|first)|related|recommended|book|contact|sample|our |the (best|ultimate|complete)|top \d|\d+\.|step|before you|after |in conclusion|wrap|key |practical|essential|model|suggested|highlights|local (food|cuisine)|food and|where to (stay|eat)|how (much|long)|is |are |do |can |should |enjoy|experience the|explore|discover|visit|from |with |for |your )", re.I)
dests = {}
for fp in sorted(glob.glob(os.path.join(FETCH, "column", "*.html"))):
    cid = os.path.basename(fp)[:-5]
    raw = open(fp, encoding="utf-8", errors="replace").read()
    h = clean(raw)
    title = re.search(r"<title>(.*?)</title>", h, re.S); title = strip_tags(title.group(1)).replace("| Japan Navi Journey", "").strip() if title else cid
    tags = [strip_tags(x) for x in re.findall(r'class="c-tag[^"]*"[^>]*>(.*?)<', h)]
    pref = tags[0] if tags else None
    body_m = re.search(r'<div class="p-column-single(.*?)<footer', h, re.S)
    body = body_m.group(1) if body_m else h
    url = f"https://japan-navi-journey.com/column/{cid}/"
    # headings with following paragraph
    items = []
    for m in re.finditer(r"<h([23])[^>]*>(.*?)</h\1>(.*?)(?=<h[23]|$)", body, re.S):
        name = strip_tags(m.group(2)).strip()
        if not name or len(name) > 70 or STOP.search(name) or name.lower().startswith("subscribe"): continue
        if re.search(r"[?？!]", name): continue
        words = name.split()
        if len(words) > 9: continue
        para = re.findall(r"<p[^>]*>(.*?)</p>", m.group(3), re.S)
        desc = strip_tags(para[0])[:300] if para else None
        places = find_places(name)
        if places:
            nm = places[0]
        else:
            core = re.sub(r"^(Morning|Afternoon|Evening|Late Morning|Night|Day \d+)\s*:\s*", "", name)
            core = re.sub(r"\s*\(.*?\)\s*$", "", core).strip()
            if len(core.split()) <= 4 and not re.search(r"\b(at|in|with|and|the|your|of|to|for|a|an|through|along|into|from)\b", core, re.I) and core[:1].isupper():
                nm = core
            elif len(core.split()) <= 5 and re.search(r"[A-Z][a-z]+", core) and core.istitle():
                nm = core
            else:
                continue
        if STOP.search(nm) or STOP2.search(nm) or GENERIC.match(nm): continue
        nm = re.sub(r"^(Heritage Site|World Heritage Site)\s+", "", nm)
        items.append({"name_en": nm, "name_ja": None, "category": None, "description_en": desc, "note": f"from column: {title} (heading: {name[:60]})", "source": url})
    key = pref or title
    d = dests.setdefault(key, {"destination": pref or title, "slug": None, "region": REGION_OF.get((pref or "").split("（")[0].strip()), "prefecture": pref, "url": None, "blog_urls": [], "summary_en": None, "attractions": [], "sources": []})
    d["blog_urls"].append(url); d["sources"].append(url)
    seen = {a["name_en"].lower() for a in d["attractions"]}
    for it in items:
        if it["name_en"].lower() not in seen:
            d["attractions"].append(it); seen.add(it["name_en"].lower())
json.dump(list(dests.values()), open(os.path.join(OUT, "destinations.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("destinations (by prefecture tag):", len(dests), "| attractions:", sum(len(d['attractions']) for d in dests.values()))
for d in dests.values(): print(f"  - {d['destination']}: {len(d['attractions'])} | {[a['name_en'] for a in d['attractions'][:8]]}")
