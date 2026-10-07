# -*- coding: utf-8 -*-
"""汇总 series/*.json -> 标准 package tour 文件 + 景点列表。
用法: python3 -I consolidate.py <series_dir> <out_dir>
"""
import sys, os, json, csv, re, glob
from collections import OrderedDict, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geo
try:
    import names  # 可选：title_cn / attraction_cn 对照表
except Exception:
    names = None

SERIES_DIR, OUT_DIR = sys.argv[1], sys.argv[2]
SITE = sys.argv[3] if len(sys.argv) > 3 else "selfguidejapan.com"
SITE_LABEL = {"selfguidejapan.com": "Self-Guided Japan（selfguidejapan.com）", "japan-navi-journey.com": "Japan Navi Journey（japan-navi-journey.com）"}.get(SITE, SITE)
os.makedirs(OUT_DIR, exist_ok=True)

SERIES_CN = {
    "BF": "基础精选（7天）", "GR": "黄金路线", "SL": "单人出行 SOLO", "FG": "家庭亲子", "TP": "主题乐园",
    "KY": "九州温泉", "HD": "北海道（夏季）", "HK": "北海道滑雪/冬季", "SE": "濑户内·四国", "KA": "关西出发",
    "HS": "温泉之旅", "KM": "高野山·熊野灵场", "NT": "自然徒步", "LX": "奢华", "WT": "冬季", "CB": "樱花", "SK": "滑雪", "KR": "樱花短线",
    "JNJ": "Japan Navi Journey 私人定制团",
}
TRANSPORT_CN = [
    (r"shinkansen|bullet", "新干线"), (r"limited express|express train|train", "火车"),
    (r"charter|private taxi|taxi", "包车/的士"), (r"\bbus\b|coach", "巴士"), (r"ferry|boat|cruise", "渡轮/游船"),
    (r"flight|plane|fly|✈", "航班"), (r"walk|hike|trek|foot", "步行/徒步"), (r"cable|ropeway|alpine route", "缆车"),
    (r"metro|subway", "地铁"), (r"rental car|drive", "自驾"),
]

def tcn(s):
    if not s: return ""
    out = []
    for pat, cn in TRANSPORT_CN:
        if re.search(pat, str(s), re.I): out.append(cn)
    return "/".join(OrderedDict.fromkeys(out)) if out else str(s)

def series_of(code):
    m = re.match(r"([A-Z]+)", code or "")
    return m.group(1) if m else ""

def is_deluxe(code):
    m = re.match(r"[A-Z]+(\d+)", code or "")
    return bool(m) and int(m.group(1)) >= 100

def fmt_price(t):
    cur = t.get("currency") or ""
    lo, hi = t.get("price_min"), t.get("price_max")
    if lo is None and hi is None: return "—"
    def f(x):
        try: return f"{int(x):,}"
        except Exception: return str(x)
    if lo is not None and hi is not None and lo != hi: return f"{cur} {f(lo)}–{f(hi)}".strip()
    return f"{cur} {f(lo if lo is not None else hi)}".strip()

def city_cn(name):
    if isinstance(name, dict): name = name.get("city") or name.get("name")
    if not isinstance(name, str): return None
    cn, _, _ = geo.city_info(name)
    return cn

def route_str(route, bilingual=True):
    parts = []
    for r in route or []:
        if isinstance(r, str): city, n = r, None
        else: city, n = r.get("city"), r.get("nights")
        if not city: continue
        cn = city_cn(city)
        label = f"{city.upper()} {cn}" if (bilingual and cn) else city
        if n: label += f" ({n}N)"
        parts.append(label)
    return " > ".join(parts)

def _tnorm(s):
    s = re.sub(r"【.*?】", "", s or "").strip().lower()
    s = s.replace("–", "-").replace("—", "-").replace("’", "'").replace("shirakawa-go", "shirakawago")
    return re.sub(r"\s+", " ", s)
_TITLE_IDX = {_tnorm(k): v for k, v in (getattr(names, "TITLE_CN", {}) or {}).items()}
def title_cn_of(t):
    if not names: return ""
    v = getattr(names, "TITLE_CN", {}).get(t.get("code"))
    if v: return v
    k = _tnorm(t.get("title_en"))
    if k in _TITLE_IDX: return _TITLE_IDX[k]
    # 去掉 " - deluxe" 后缀再试
    k2 = re.sub(r"\s*-\s*(hotel )?deluxe.*$", "", k)
    if k2 in _TITLE_IDX: return _TITLE_IDX[k2] + "（豪华版）"
    k3 = re.sub(r"^solo\s*/?\s*", "", k)
    if k3 in _TITLE_IDX: return "单人·" + _TITLE_IDX[k3]
    return ""

_ATTR_IDX = None; _ATTR_IDX2 = None
def attr_cn_of(name_en):
    global _ATTR_IDX, _ATTR_IDX2
    if not names: return ""
    if _ATTR_IDX is None:
        _ATTR_IDX, _ATTR_IDX2 = {}, {}
        for k, v in getattr(names, "ATTR_CN", {}).items():
            _ATTR_IDX.setdefault(akey(k), v)      # 严格：只去冠词/寺社后缀
            _ATTR_IDX2.setdefault(akey2(k), v)    # 宽松：再去 castle/garden/park 等通用词
    if names.ATTR_CN.get(name_en): return names.ATTR_CN[name_en]
    if _ATTR_IDX.get(akey(name_en)): return _ATTR_IDX[akey(name_en)]
    # 裸地名（如 "Matsumoto"）优先按城市表翻译，避免被 "Matsumoto Castle" 的宽松匹配污染
    ccn, _, _ = geo.city_info(name_en)
    if ccn and len(name_en.split()) <= 2: return ccn
    return _ATTR_IDX2.get(akey2(name_en)) or ""

def akey2(s):
    """更松：去掉 temple/shrine/garden/castle/park/museum 等通用词"""
    s = akey(s)
    s = re.sub(r"\b(garden|gardens|castle|park|museum|market|district|street|bridge|falls|waterfall|lake|mount|mt|island|cruise|ropeway|station|area|village|town|onsen|hot spring|hot springs)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def akey(s):
    s = (s or "").lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = s.replace("-", " ").replace("’", "'").replace("'", "")
    s = re.sub(r"\b(the|temple|shrine|jinja|jingu|taisha|dera|ji)\b", " ", s)  # 松匹配
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def merge_rec(a, b):
    """按代码逐字段合并两条记录：exists 取真优先；标量取非空（逐日更长者优先）；列表取并集。"""
    prio = lambda x: 2 if x.get("_file") == "main_session.json" else (1 if str(x.get("_file", "")).startswith("pass2") else 0)
    score = lambda x: (1 if x.get("exists") else 0, len(x.get("day_by_day") or []), prio(x), 1 if (x.get("source_confidence") == "high") else 0)
    hi, lo = (a, b) if score(a) >= score(b) else (b, a)
    out = dict(hi)
    for k, v in lo.items():
        if k not in out or out[k] in (None, "", [], {}):
            out[k] = v
        elif isinstance(out[k], list) and isinstance(v, list) and k in ("themes", "inclusions", "exclusions", "highlights", "attractions_all", "sources"):
            seen = {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in out[k]}
            out[k] = out[k] + [x for x in v if json.dumps(x, sort_keys=True, ensure_ascii=False) not in seen]
    if a.get("exists") or b.get("exists"): out["exists"] = True
    conf_rank = {"high": 3, "medium": 2, "low": 1}
    out["source_confidence"] = max([a.get("source_confidence"), b.get("source_confidence")], key=lambda c: conf_rank.get(c or "", 0))
    notes = [x.get("notes") for x in (hi, lo) if x.get("notes")]
    if len(notes) == 2 and notes[0] != notes[1]: out["notes"] = notes[0] + " ‖ " + notes[1]
    return out

# ---------- load ----------
tours = OrderedDict()
dests = []
for fp in sorted(glob.glob(os.path.join(SERIES_DIR, "*.json"))):
    with open(fp, encoding="utf-8") as f:
        try: data = json.load(f)
        except Exception as e:
            print("BAD JSON", fp, e); continue
    if os.path.basename(fp).startswith("destinations"):
        dests += (data if isinstance(data, list) else data.get("destinations", [])); continue
    if isinstance(data, dict): data = data.get("tours") or data.get("results") or list(data.values())
    for t in data:
        if not isinstance(t, dict): continue
        if not t.get("code"):
            if not t.get("title_en"): continue
            t["code"] = (t.get("series") or "UNK") + "-?" + re.sub(r"[^A-Za-z]", "", t["title_en"])[:6].upper()
        code = t["code"].strip().upper()
        t["code"] = code
        t["_file"] = os.path.basename(fp)
        if code in tours:
            tours[code] = merge_rec(tours[code], t)
        else:
            tours[code] = t

existing = OrderedDict((c, t) for c, t in sorted(tours.items()) if t.get("exists"))
missing = [c for c, t in sorted(tours.items()) if t.get("exists") is False]
unverified = [c for c, t in sorted(tours.items()) if t.get("exists") is None and c]
print(f"loaded {len(tours)} codes, exists={len(existing)}, not-found={len(missing)}")

# ---------- catalog ----------
cat_rows = []
for code, t in existing.items():
    s = series_of(code)
    cat_rows.append(OrderedDict([
        ("code", code), ("series", s), ("series_cn", SERIES_CN.get(s, s) + ("·豪华版" if is_deluxe(code) else "")),
        ("title_en", t.get("title_en") or ""), ("title_cn", title_cn_of(t)),
        ("days", t.get("days") or ""), ("nights", t.get("nights") or ""),
        ("route", route_str(t.get("route"), bilingual=False)), ("route_cn", route_str(t.get("route"))),
        ("price_min", t.get("price_min") if t.get("price_min") is not None else ""),
        ("price_max", t.get("price_max") if t.get("price_max") is not None else ""),
        ("currency", t.get("currency") or ""), ("themes", "; ".join(t.get("themes") or [])),
        ("season", t.get("season") or ""), ("arrival", t.get("arrival_airport") or ""), ("departure", t.get("departure_airport") or ""),
        ("day_by_day_days", len(t.get("day_by_day") or [])), ("confidence", t.get("source_confidence") or ""),
        ("url", t.get("url") or f"https://selfguidejapan.com/tours/{code}"),
    ]))
with open(os.path.join(OUT_DIR, "tours_catalog.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(cat_rows[0].keys()) if cat_rows else ["code"]); w.writeheader(); w.writerows(cat_rows)

# catalog md grouped by series
by_series = defaultdict(list)
for r in cat_rows: by_series[r["series"]].append(r)
md = [f"# {SITE_LABEL} 线路目录", "",
      f"共 {len(cat_rows)} 条线路。" + ("价格为每人、两人一房、不含国际机票（SOLO 系列为单人单房价）。" if SITE == "selfguidejapan.com" else "私人定制团，价格按询价（站点不公开标价）。") + "数据来自搜索索引摘要，未直接读取网页，见 README。", ""]
for s in sorted(by_series, key=lambda x: (x not in SERIES_CN, x)):
    rows = sorted(by_series[s], key=lambda r: r["code"])
    md += [f"## {s} · {SERIES_CN.get(s, s)}（{len(rows)} 条）", "",
           "| 代码 | 线路名 | 中文名 | 天数 | 路线 | 价格/人 | 逐日 | 可信度 |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        price = fmt_price({"currency": r["currency"], "price_min": r["price_min"] or None, "price_max": r["price_max"] or None})
        md.append(f"| [{r['code']}]({r['url']}) | {r['title_en']} | {r['title_cn']} | {r['days'] or '?'}D | {r['route_cn'] or '—'} | {price} | {r['day_by_day_days']}/{r['days'] or '?'} | {r['confidence']} |")
    md.append("")
if missing:
    md += ["## 探测过、判定不存在的代码", "", ", ".join(missing), ""]
if unverified:
    md += ["## 探测过一次、未命中但尚未二次确认的代码（倾向不存在）", "", ", ".join(unverified), ""]
with open(os.path.join(OUT_DIR, "tours_catalog.md"), "w", encoding="utf-8") as f: f.write("\n".join(md))

# ---------- package tours (standard itinerary) ----------
pt_json = []
pm = [f"# {SITE_LABEL} 标准行程（Package Tour 格式）", "",
      "格式沿用 WEBUY 行程 house grammar：`CITY_EN 中文`、`>` 陆路 / `✈` 航班、(2N) 连住、只列有信息的餐食。",
      "所有内容转录自 selfguidejapan.com 各产品页的搜索索引摘要；空白 = 来源未给出，**不是**不包含。", ""]
# 目录
pm += ["## 目录", ""]
for s in sorted(by_series, key=lambda x: (x not in SERIES_CN, x)):
    pm.append(f"- **{s} {SERIES_CN.get(s, s)}**：" + "、".join(f"[{r['code']}](#{r['code'].lower()})" for r in sorted(by_series[s], key=lambda r: r['code'])))
pm.append("")

def h(s):
    if s is None: return ""
    if isinstance(s, dict): s = s.get("name_en") or s.get("name") or s.get("text") or json.dumps(s, ensure_ascii=False)
    if isinstance(s, (list, tuple)): s = "、".join(h(x) for x in s)
    return str(s).replace("|", "／").replace("\n", " ").strip()

for code, t in existing.items():
    s = series_of(code)
    days, nights = t.get("days"), t.get("nights")
    dn = f"{days}天{nights}晚" if days and nights else (f"{days}天" if days else "天数未知")
    pm += [f'<a id="{code.lower()}"></a>', f"## 【{code}】{t.get('title_en') or ''}", ""]
    tc = title_cn_of(t)
    head = f"**{tc}** · " if tc else ""
    pm.append(f"{head}{dn} · {fmt_price(t)} /人" + (f"（{t.get('price_note')}）" if t.get("price_note") else ""))
    pm.append("")
    meta = [f"- **系列**：{s} {SERIES_CN.get(s, s)}" + ("（豪华酒店版）" if is_deluxe(code) else "")]
    if t.get("themes"): meta.append(f"- **主题**：{'、'.join(t['themes'])}")
    if t.get("season"): meta.append(f"- **季节/出发期**：{t['season']}")
    if t.get("arrival_airport") or t.get("departure_airport"):
        meta.append(f"- **进出点**：{t.get('arrival_airport') or '?'} ✈ 进 · {t.get('departure_airport') or '?'} ✈ 出")
    rs = route_str(t.get("route"))
    if rs: meta.append(f"- **路线**：{rs}")
    if t.get("highlights"): meta.append("- **亮点**：" + " ".join("✦ " + h(x) for x in t["highlights"]))
    if t.get("tour_type"): meta.append(f"- **产品形态**：{h(t['tour_type'])}")
    if t.get("hotels"): meta.append("- **酒店/旅馆**：" + "、".join(h(x) for x in t["hotels"]))
    inc = "、".join(t.get("inclusions") or []); exc = "、".join(t.get("exclusions") or [])
    if inc or exc: meta.append(f"- **含**：{inc or '—'} · **不含**：{exc or '—'}")
    meta.append(f"- **来源**：{t.get('url') or ''}（可信度 {t.get('source_confidence') or '?'}）" + (f" · 备注：{h(t.get('notes'))}" if t.get("notes") else ""))
    pm += meta + [""]
    dbd = t.get("day_by_day") or []
    if dbd:
        pm += ["| Day | 路线 | 交通 | 景点 / 活动 | 餐 | 住宿 |", "|---|---|---|---|---|---|"]
        for d in dbd:
            fr, to = d.get("from"), d.get("to")
            def lab(c):
                cn = city_cn(c); return f"{c.upper()} {cn}" if cn else (c or "")
            if fr and to and fr != to: route = f"{lab(fr)} > {lab(to)}"
            elif to: route = lab(to)
            elif fr: route = lab(fr)
            else: route = ""
            title = h(d.get("title"))
            route = f"{route}　{title}" if title and route else (route or title)
            attrs = "、".join(h(a) for a in (d.get("attractions") or []))
            acts = h(d.get("activities"))
            cell = " ✦ ".join(x for x in [attrs, acts] if x)
            if d.get("notes"): cell += f"（{h(d['notes'])}）"
            stay = d.get("stay") or ""
            if isinstance(stay, dict): stay = stay.get("city") or stay.get("hotel") or ""
            stay_cn = city_cn(stay)
            pm.append(f"| {d.get('day','')} | {route} | {tcn(d.get('transport'))} | {cell} | {h(d.get('meals')) or ''} | {stay_cn or h(stay)} |")
        pm.append("")
    else:
        pm += ["_逐日行程未能从索引摘要中取得，需开放域名后补抓。_", ""]
    pt_json.append(OrderedDict([
        ("code", code), ("series", s), ("deluxe", is_deluxe(code)), ("url", t.get("url")),
        ("title_en", t.get("title_en")), ("title_cn", tc or None), ("subtitle_en", t.get("subtitle_en")),
        ("days", days), ("nights", nights), ("price", {"min": t.get("price_min"), "max": t.get("price_max"), "currency": t.get("currency"), "note": t.get("price_note")}),
        ("themes", t.get("themes") or []), ("season", t.get("season")),
        ("airports", {"arrival": t.get("arrival_airport"), "departure": t.get("departure_airport")}),
        ("route", [({"city": r, "city_cn": city_cn(r), "nights": None} if isinstance(r, str) else {"city": r.get("city"), "city_cn": city_cn(r.get("city")), "nights": r.get("nights")}) for r in (t.get("route") or [])]),
        ("days_detail", [OrderedDict([
            ("day", d.get("day")), ("title", d.get("title")), ("from", d.get("from")), ("to", d.get("to")),
            ("transport", d.get("transport")), ("attractions", d.get("attractions") or []), ("activities", d.get("activities")),
            ("meals", d.get("meals")), ("stay", d.get("stay")), ("stay_cn", city_cn(d.get("stay"))), ("notes", d.get("notes"))]) for d in dbd]),
        ("highlights", t.get("highlights") or []), ("inclusions", t.get("inclusions") or []), ("exclusions", t.get("exclusions") or []),
        ("source_confidence", t.get("source_confidence")), ("sources", t.get("sources") or []), ("notes", t.get("notes")),
        ("site", SITE), ("tour_type", t.get("tour_type")), ("region", t.get("region")), ("prefectures", t.get("prefectures") or []), ("hotels", t.get("hotels") or []),
    ]))
with open(os.path.join(OUT_DIR, "package_tours.md"), "w", encoding="utf-8") as f: f.write("\n".join(pm))
with open(os.path.join(OUT_DIR, "package_tours.json"), "w", encoding="utf-8") as f: json.dump(pt_json, f, ensure_ascii=False, indent=1)

# ---------- attractions ----------
attr = OrderedDict()   # key -> record
def add_attr(name_en, city, code=None, category=None, desc=None, name_ja=None, src=None, dest_region=None):
    name_en = (name_en or "").strip()
    if not name_en or len(name_en) < 3: return
    k = akey(name_en)
    if not k: return
    rec = attr.get(k)
    if not rec:
        rec = attr[k] = OrderedDict([("name_en", name_en), ("name_cn", attr_cn_of(name_en)), ("name_ja", name_ja),
                                     ("city", city or ""), ("category", category or ""), ("description", desc or ""),
                                     ("tours", []), ("sources", [])])
    else:
        if len(name_en) > len(rec["name_en"]) and name_en.lower().startswith(rec["name_en"].lower()[:4]): rec["name_en"] = rec["name_en"]  # 保留首次名称
        if not rec["city"] and city: rec["city"] = city
        if not rec["category"] and category: rec["category"] = category
        if not rec["description"] and desc: rec["description"] = desc
        if not rec["name_ja"] and name_ja: rec["name_ja"] = name_ja
        if not rec["name_cn"]: rec["name_cn"] = attr_cn_of(name_en)
    if code and code not in rec["tours"]: rec["tours"].append(code)
    if src and src not in rec["sources"]: rec["sources"].append(src)

for code, t in existing.items():
    for a in t.get("attractions_all") or []:
        if isinstance(a, str): add_attr(a, None, code, src=t.get("url"))
        else: add_attr(a.get("name_en") or a.get("name"), a.get("city"), code, a.get("category"), src=t.get("url"))
    for d in t.get("day_by_day") or []:
        for a in d.get("attractions") or []:
            if isinstance(a, dict): add_attr(a.get("name_en") or a.get("name"), a.get("city") or d.get("to") or d.get("stay") or d.get("from"), code, a.get("category"), src=t.get("url"))
            else: add_attr(a, d.get("to") or d.get("stay") or d.get("from"), code, src=t.get("url"))
for dst in dests:
    for a in dst.get("attractions") or []:
        add_attr(a.get("name_en"), dst.get("destination"), None, a.get("category"), a.get("description_en"), a.get("name_ja"), a.get("source") or dst.get("url"))

CAT_KW = [
    ("ski", r"\bski|snow|powder|piste"), ("theme_park", r"theme park|disney|universal|legoland|ghibli park|fuji-q|huis ten bosch|brick theme"),
    ("onsen", r"onsen|hot spring|sand bath|bath|ryokan|jigoku|hell valley|hells"), ("temple", r"temple|\bji\b|-ji\b|dera\b|-in\b|okunoin|shukubo|buddha|kannon|garan|koyasan"),
    ("shrine", r"shrine|jingu|jinja|taisha|torii|tenmangu|hachimangu"), ("castle", r"castle|samurai|jinya"),
    ("garden", r"garden|-en\b|korakuen|kenroku|ritsurin|sengan"), ("museum", r"museum|art house|benesse|chichu|teamlab|gallery|kabuki"),
    ("market", r"market|yokocho|yatai|food stall|shopping|street food|ramen|beef|wagyu|kaiseki|okonomiyaki|cuisine|dining|lunch|cafe"),
    ("nature", r"falls|waterfall|gorge|lake|mount|mt\.|mt |alpine|valley|crater|park\b|island|bay|beach|cape|forest|bamboo|pond|snow corridor|monkey|zoo|aquarium|flower|lavender"),
    ("transport_experience", r"train|cruise|ferry|ropeway|cable|railway|boat|rafting|cycling|taxi"),
    ("experience", r"experience|training|ceremony|kimono|cooking|class|festival|matsuri|tour\b|walk|trail|kodo|nakasendo|pilgrimage|stay"),
    ("district", r"district|street|town|quarter|old town|village|alley|bridge|crossing|area|slope|canal|harbor|port|chaya|gion|pontocho|dotonbori|shinsekai|ginza|shinjuku|shibuya|harajuku|asakusa|akihabara|odaiba|susukino|nakasu|namba"),
    ("viewpoint", r"view|observ|tower|skytree|sky|deck|dam"),
]
CAT_CN = {"ski": "滑雪", "theme_park": "主题乐园", "onsen": "温泉", "temple": "寺院", "shrine": "神社", "castle": "城堡/武家", "garden": "庭园", "museum": "博物馆/美术馆",
          "market": "市场/美食", "nature": "自然景观", "festival": "祭典", "village": "村落", "beach": "海滩", "winery": "酒庄/酒藏", "craft": "工艺体验", "transport_experience": "观光交通", "experience": "体验/活动", "district": "街区/城镇", "viewpoint": "观景", "food": "美食", "hotel": "酒店", "city": "城市"}
def guess_cat(name, desc=""):
    s = f"{name} {desc}".lower()
    for c, pat in CAT_KW:
        if re.search(pat, s): return c
    return ""

rows = []
for k, r in attr.items():
    if not r["category"]: r["category"] = guess_cat(r["name_en"], r["description"])
    r["category"] = (r["category"] or "").lower().replace(" ", "_")
    cn, reg, regcn = geo.city_info(r["city"])
    rows.append(OrderedDict([
        ("name_en", r["name_en"]), ("name_cn", r["name_cn"] or ""), ("name_ja", r["name_ja"] or ""),
        ("city", r["city"]), ("city_cn", cn or ""), ("region", reg or ""), ("region_cn", regcn or ""),
        ("category", r["category"]), ("category_cn", CAT_CN.get(r["category"], r["category"])), ("tour_count", len(r["tours"])), ("tours", " ".join(sorted(r["tours"]))),
        ("description", r["description"]), ("sources", " ".join(r["sources"][:3])), ("site", SITE),
    ]))
rows.sort(key=lambda r: (r["region"] or "zz", r["city"], -r["tour_count"], r["name_en"]))
with open(os.path.join(OUT_DIR, "attractions.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["name_en"]); w.writeheader(); w.writerows(rows)

am = [f"# {SITE_LABEL} 景点列表", "", f"共 {len(rows)} 个景点/体验，按区域 → 城市分组；「线路」列为出现该景点的线路代码，次数越多说明越是该站的核心卖点。", ""]
by_reg = defaultdict(lambda: defaultdict(list))
for r in rows: by_reg[r["region"] or "其他/未归类"][r["city"] or "（未标城市）"].append(r)
order = ["Hokkaido", "Tohoku", "Kanto", "Chubu", "Hokuriku", "Kansai", "Chugoku", "Setouchi", "Shikoku", "Kyushu", "Okinawa"]
for reg in sorted(by_reg, key=lambda x: (order.index(x) if x in order else 99, x)):
    am += [f"## {reg} {geo.REGION_CN.get(reg, '')}".strip(), ""]
    for city in sorted(by_reg[reg], key=lambda c: -sum(x['tour_count'] for x in by_reg[reg][c])):
        rs = by_reg[reg][city]
        ccn = rs[0]["city_cn"]
        am += [f"### {city} {ccn}".strip(), "", "| 景点 (EN) | 中文 | 类别 | 出现线路数 | 线路 | 说明 |", "|---|---|---|---|---|---|"]
        for r in rs:
            am.append(f"| {r['name_en']} | {r['name_cn']} | {r['category_cn'] or '—'} | {r['tour_count']} | {r['tours']} | {h(r['description'])[:120]} |")
        am.append("")
with open(os.path.join(OUT_DIR, "attractions.md"), "w", encoding="utf-8") as f: f.write("\n".join(am))

# unmapped report
unm_city = sorted({r["city"] for r in rows if r["city"] and not r["city_cn"]})
unm_attr = [r["name_en"] for r in rows if not r["name_cn"]]
print(f"attractions={len(rows)}, unmapped cities={len(unm_city)}: {unm_city[:40]}")
print(f"attractions without CN name={len(unm_attr)}")
with open(os.path.join(OUT_DIR, "_unmapped.json"), "w", encoding="utf-8") as f:
    json.dump({"cities": unm_city, "attractions": unm_attr, "titles": [t.get("title_en") for c, t in existing.items() if not title_cn_of(t)]}, f, ensure_ascii=False, indent=1)
print("done ->", OUT_DIR)
