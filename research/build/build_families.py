# -*- coding: utf-8 -*-
"""行程归并：把线路按路线骨架聚成「标准行程家族」，并把景点按区域/城市打 tag 作为可选景点池。
用法: python3 -I build_families.py <out_dir>   （读取 out_dir/package_tours.json 与 attractions.csv）
"""
import sys, os, json, csv, re
from collections import OrderedDict, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geo
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SRC = sys.argv[2:] or [OUT]
tours = {}
attrs_raw = []
for d in SRC:
    for t in json.load(open(os.path.join(d, "package_tours.json"), encoding="utf-8")):
        tours[t["code"]] = t
    attrs_raw += list(csv.DictReader(open(os.path.join(d, "attractions.csv"), encoding="utf-8-sig")))
# 跨站去重（按归一化英文名）
def _akey(s):
    s = (s or "").lower(); s = re.sub(r"\(.*?\)", "", s); s = s.replace("-", " ").replace("’", "'").replace("'", "")
    s = re.sub(r"\b(the|temple|shrine|jinja|jingu|taisha|dera|ji)\b", " ", s); s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()
_m = OrderedDict()
for a in attrs_raw:
    k = _akey(a["name_en"]) or a["name_en"]
    if k in _m:
        o = _m[k]
        o["tours"] = " ".join(sorted(set((o["tours"] + " " + a["tours"]).split())))
        o["tour_count"] = str(len(o["tours"].split()))
        o["site"] = " ".join(sorted(set((o.get("site", "") + " " + a.get("site", "")).split())))
        for f in ("name_cn", "name_ja", "city", "city_cn", "region", "region_cn", "category", "category_cn", "description"):
            if not o.get(f) and a.get(f): o[f] = a[f]
    else:
        _m[k] = dict(a)
attrs = list(_m.values())

# ---------------- 家族定义（人工归并，依据：核心城市骨架 + 主题） ----------------
from families_def import FAMILIES as _ALL_FAMILIES
FAMILIES = [f for f in _ALL_FAMILIES if f["standard"] in tours]
# 显式标注交叉（一线路可属多个家族）
primary = {}
for f in FAMILIES:
    for m in f["members"]:
        primary.setdefault(m, f["id"])
unassigned = [c for c in tours if c not in primary]

def cn(city):
    c, _, _ = geo.city_info(city); return c
def route_of(t):
    return " > ".join(f"{r['city']}{'('+str(r['nights'])+'N)' if r['nights'] else ''}" for r in t.get("route") or [])
def price(t):
    p = t["price"]; cur = p.get("currency") or ""
    if p.get("min") is None and p.get("max") is None: return "—"
    f = lambda x: f"{int(x):,}" if isinstance(x, (int, float)) else str(x)
    return f"{cur} {f(p['min'])}–{f(p['max'])}" if p.get("min") is not None and p.get("max") is not None else f"{cur} {f(p.get('min') or p.get('max'))}"

# ---------------- 景点池：按家族城市归属 ----------------
fam_cities = {f["id"]: {geo.norm(c) for c, _ in f["skeleton"]} for f in FAMILIES}
# 线路 → 家族集合
tour_fams = defaultdict(set)
for f in FAMILIES:
    for m in f["members"]: tour_fams[m].add(f["id"])
for a in attrs:
    codes = a["tours"].split()
    fams = set()
    for c in codes: fams |= tour_fams.get(c, set())
    a["_fams"] = sorted(fams)
    a["_count"] = int(a["tour_count"] or 0)

# ---------------- 输出 1：merged_itineraries.md ----------------
L = [f"# 行程归并：标准行程家族（{len(tours)} 条线路 → {len(FAMILIES)} 个家族）", "",
     "归并依据：**住宿城市骨架**（城市顺序 + 过夜数）相同或仅差 1–2 个节点的线路视为同一家族；家族内选一条数据最完整的作为「标准行程」，其余列为变体并注明差异。价格为每人、两人一房、不含国际机票（SOLO 为单人价；JNJ = Japan Navi Journey 私人定制团，按询价）。成员后括号标来源站：SGJ = selfguidejapan.com，JNJ = japan-navi-journey.com。",
     "", "## 家族总览", "", "| 家族 | 标准骨架 | 天数带 | 标准线路 | 成员数 | 成员代码 |", "|---|---|---|---|---|---|"]
for f in FAMILIES:
    sk = " > ".join(f"{c} {cn(c) or ''}({n}N)".replace(" (", "(") for c, n in f["skeleton"])
    L.append(f"| {f['id']} {f['name']} | {sk} | {f['days']} | {f['standard']} | {len(f['members'])} | {' '.join(f['members'])} |")
L.append("")
if unassigned: L += [f"未归入家族的代码：{', '.join(unassigned)}", ""]

for f in FAMILIES:
    L += [f"## {f['id']} {f['name']}", f"_{f['name_en']}_", ""]
    sk = " > ".join(f"{c.upper()} {cn(c) or ''} ({n}N)" for c, n in f["skeleton"])
    L += [f"- **标准骨架**：{sk}", f"- **天数带**：{f['days']}", f"- **归并说明**：{f['note']}", ""]
    # 价格带
    ps = [tours[m]["price"] for m in f["members"] if m in tours and tours[m]["price"].get("min") is not None and (tours[m]["price"].get("currency") in (None, "USD"))]
    if ps:
        lo = min(p["min"] for p in ps); hi = max((p["max"] or p["min"]) for p in ps)
        L += [f"- **家族价格带（USD/人）**：{int(lo):,} – {int(hi):,}", ""]
    L += ["| 代码 | 线路 | 中文名 | 天数 | 住宿骨架 | 价格/人 | 与标准行程的差异 / 备注 |", "|---|---|---|---|---|---|---|"]
    for m in f["members"]:
        t = tours.get(m)
        if not t: continue
        tag = "**标准**" if m == f["standard"] else ("豪华版" if t.get("deluxe") else "变体")
        extra = []
        others = sorted(tour_fams[m] - {f["id"]})
        if others: extra.append("也属 " + "/".join(others))
        if t.get("season"): extra.append(f"季节 {t['season']}")
        site = "JNJ" if t.get("site", "").startswith("japan-navi") else "SGJ"
        L.append(f"| {m} | {t['title_en'] or ''} | {t.get('title_cn') or ''} | {t['days'] or '?'}D | {route_of(t) or '—'} | {price(t)} | {tag}（{site}）{'；' + '；'.join(extra) if extra else ''} |")
    L.append("")
    # 家族景点池（核心 = 出现 ≥2 条线路）
    pool = [a for a in attrs if f["id"] in a["_fams"]]
    pool.sort(key=lambda a: (-a["_count"], a["city"], a["name_en"]))
    if pool:
        L += ["**家族景点池**（出现于本家族线路的景点，按出现线路数排序；★ = 出现 ≥2 条线路的核心景点，其余为可选）", ""]
        bycity = OrderedDict()
        for a in pool: bycity.setdefault(a["city"] or "—", []).append(a)
        for city, items in bycity.items():
            s = "、".join(f"{'★' if a['_count'] >= 2 else ''}{a['name_cn'] or a['name_en']}" for a in items)
            L.append(f"- **{city} {cn(city) or ''}**：{s}")
        L.append("")
with open(os.path.join(OUT, "merged_itineraries.md"), "w", encoding="utf-8") as fo: fo.write("\n".join(L))
json.dump([{**{k: v for k, v in f.items()}, "skeleton": [{"city": c, "city_cn": cn(c), "nights": n} for c, n in f["skeleton"]]} for f in FAMILIES],
          open(os.path.join(OUT, "merged_itineraries.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------- 输出 2：attractions_by_city.md（可选景点池，按区域→城市，带 tag） ----------------
FAM_NAME = {f["id"]: f["name"].split("（")[0] for f in FAMILIES}
A = ["# 可选景点池：按区域 → 城市 tag", "",
     "每个景点标注：类别 tag、出现线路数（越多越是该站核心卖点）、所属行程家族 tag。**核心** = 出现 ≥3 条线路；**常见** = 2 条；**可选** = 1 条或仅出现在目的地指南。",
     "Planner 做产品时可按城市直接挑选：先放核心，再按主题补可选。", ""]
order = ["Hokkaido", "Tohoku", "Kanto", "Chubu", "Hokuriku", "Kansai", "Chugoku", "Setouchi", "Shikoku", "Kyushu", "Okinawa"]
byreg = defaultdict(lambda: defaultdict(list))
for a in attrs: byreg[a["region"] or "其他/未归类"][a["city"] or "（未标城市）"].append(a)
summary = []
for reg in sorted(byreg, key=lambda x: (order.index(x) if x in order else 99, x)):
    cities = byreg[reg]
    A += [f"## {reg} {geo.REGION_CN.get(reg, '')}".strip(), ""]
    for city in sorted(cities, key=lambda c: -sum(x["_count"] for x in cities[c])):
        items = sorted(cities[city], key=lambda a: (-a["_count"], a["name_en"]))
        ccn = items[0]["city_cn"]
        core = [a for a in items if a["_count"] >= 3]; common = [a for a in items if a["_count"] == 2]; opt = [a for a in items if a["_count"] <= 1]
        summary.append((reg, city, ccn, len(core), len(common), len(opt)))
        A += [f"### {city} {ccn}".strip(), "", "| 景点 | 中文 | 类别 | 线路数 | 等级 | 家族 tag | 出现线路 | 来源站 |", "|---|---|---|---|---|---|---|---|"]
        for a in items:
            lvl = "核心" if a["_count"] >= 3 else ("常见" if a["_count"] == 2 else "可选")
            fams = " ".join(f"`{x}`" for x in a["_fams"]) or "—"
            site = a.get("site", "").replace("selfguidejapan.com", "SGJ").replace("japan-navi-journey.com", "JNJ")
            A.append(f"| {a['name_en']} | {a['name_cn']} | {a.get('category_cn') or a['category'] or '—'} | {a['_count']} | {lvl} | {fams} | {a['tours'] or '（目的地指南）'} | {site} |")
        A.append("")
A += ["## 城市汇总", "", "| 区域 | 城市 | 核心 | 常见 | 可选 |", "|---|---|---|---|---|"]
for reg, city, ccn, c1, c2, c3 in summary: A.append(f"| {reg} | {city} {ccn} | {c1} | {c2} | {c3} |")
A += ["", "家族代号对照：" + "；".join(f"`{k}` {v}" for k, v in FAM_NAME.items())]
with open(os.path.join(OUT, "attractions_by_city.md"), "w", encoding="utf-8") as fo: fo.write("\n".join(A))
rows = []
for a in attrs:
    rows.append(OrderedDict([(k, a.get(k, "")) for k in ("name_en","name_cn","name_ja","city","city_cn","region","region_cn","category","category_cn","tour_count")] +
                            [("level", "core" if a["_count"] >= 3 else ("common" if a["_count"] == 2 else "optional")), ("families", " ".join(a["_fams"])), ("tours", a["tours"]), ("site", a.get("site", "")), ("description", a["description"])]))
with open(os.path.join(OUT, "attractions_by_city.csv"), "w", newline="", encoding="utf-8-sig") as fo:
    w = csv.DictWriter(fo, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"families={len(FAMILIES)}, assigned={len(primary)}, unassigned={unassigned}, attractions={len(attrs)}")
