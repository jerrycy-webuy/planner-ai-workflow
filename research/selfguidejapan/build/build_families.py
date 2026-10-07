# -*- coding: utf-8 -*-
"""行程归并：把线路按路线骨架聚成「标准行程家族」，并把景点按区域/城市打 tag 作为可选景点池。
用法: python3 -I build_families.py <out_dir>   （读取 out_dir/package_tours.json 与 attractions.csv）
"""
import sys, os, json, csv, re
from collections import OrderedDict, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import geo
OUT = sys.argv[1]
tours = {t["code"]: t for t in json.load(open(os.path.join(OUT, "package_tours.json"), encoding="utf-8"))}
attrs = list(csv.DictReader(open(os.path.join(OUT, "attractions.csv"), encoding="utf-8-sig")))

# ---------------- 家族定义（人工归并，依据：核心城市骨架 + 主题） ----------------
FAMILIES = [
 dict(id="F01", name="黄金路线 7 天（东京 > 京都 > 大阪）", name_en="Golden Route Classic 7D",
      skeleton=[("Tokyo",2),("Kyoto",2),("Osaka",2)], days="6–7D", standard="BF001",
      members=["BF001","KA001","KR003"],
      note="首访日本的最短闭环；KA001 为关西进出的 6 天版（大阪 2N > 奈良 1N > 京都 2N），KR003 为大阪基地 4 天樱花短线（仅 2027-04-08～04-17 出发）。"),
 dict(id="F02", name="东京 > 金泽 > 京都（北陆文化线）", name_en="Tokyo–Kanazawa–Kyoto",
      skeleton=[("Tokyo",2),("Kanazawa",2),("Kyoto",2)], days="7–12D", standard="BF002",
      members=["BF002","GR006","GR106","KA002","NT009"],
      note="北陆新干线 + 敦贺转特急；GR006/GR106 为 12 天版（加大阪进出、京都 3N）；KA002 为关西出发 7 天、加白川乡包车到高山；NT009 为美食铁道版（富士/伊势/金泽，标题待核）。"),
 dict(id="F03", name="东京 > 高山·白川乡 > 京都（飞驒世界遗产线）", name_en="Golden Route Plus: Takayama & Shirakawa-go",
      skeleton=[("Tokyo",2),("Takayama",2),("Kyoto",3),("Nara",2),("Tokyo",2)], days="7–14D", standard="GR002",
      members=["BF003","GR002","GR102","GR003","GR103","SL103","TP003","FG002","FG003","GR009","HS002"],
      note="站点最主力的 12 天骨架：Tokyo 2N > Takayama 2N（包车白川乡）> Kyoto 3N > Nara 2N > Tokyo 2N。BF003 是 7 天缩减版；GR003 把奈良换成金泽 2N；TP003 把奈良换成大阪环球影城；FG002/FG003 为家庭 13 天（加箱根/广岛）；GR009 14 天加箱根 1N + 广岛；HS002 为温泉版（金泽 2N > 白川乡住 1N > 高山 > 下吕）。"),
 dict(id="F04", name="东京 > 京都 > 姬路 > 广岛·宫岛（西日本名城线）", name_en="West Japan: Castles, Hiroshima & Miyajima",
      skeleton=[("Tokyo",2),("Kyoto",3),("Himeji",1),("Hiroshima",2),("Osaka",2)], days="7–16D", standard="GR005",
      members=["BF004","BF005","KA003","GR004","GR104","GR005","GR105","SL004","SL005","GR010","FG001","TP002","TP102","LX003","HS001","KM004"],
      note="7 天版（BF004 Tokyo > Hiroshima 2N > Himeji > Osaka；BF005 延伸到福冈）；15 天版加金泽/冈山/直岛（GR004、GR005 及其豪华版、SOLO 版）；GR010 16 天 Tokyo > Takayama > Kyoto > Okayama > Fukuoka > Hiroshima > Tokyo；KA003 关西进出 8 天加城崎温泉；LX003 奢华 10 天（包车 + 高速船宫岛）；KM004 把姬路/城崎与高野山组合。"),
 dict(id="F05", name="伊势志摩·贤岛（Hidden Gems 线）", name_en="Ise-Shima / Kashikojima",
      skeleton=[("Tokyo",2),("Nagoya",1),("Kashikojima",2),("Osaka",2),("Nara",1),("Kyoto",3)], days="9–16D", standard="GR001",
      members=["GR001","GR101","SL001","GR007","GR107","SL007","GR008","GR108","TP001","TP101","LX001","FG005","NT008","KM001","KM002"],
      note="站点特色产品：伊势神宫（内外宫、宇治桥日出）+ 夫妇岩 + 御木本真珠岛 + 英虞湾游船 + 海女小屋午餐 + 观光特急 Shimakaze。GR007 加箱根与广岛（13 天）；GR008 为美食主题 16 天（松阪牛/怀石）；TP001/TP101 加大阪环球影城 2 天与高山；LX001 奢华版（帝国饭店、Green Car）；FG005 家庭忍者版（赤目四十八瀑忍者训练）；KM001/KM002 与高野山组合 15 天。"),
 dict(id="F06", name="高野山 · 熊野古道 · 纪伊半岛（灵场徒步线）", name_en="Koyasan & Kumano Kodo",
      skeleton=[("Tokyo",2),("Kyoto",2),("Koyasan",1),("Kawayu Onsen",1),("Kii-Katsuura",1),("Osaka",2)], days="8–12D", standard="NT006",
      members=["KM003","SL003","NT006","NT007","NT002","NT-?SACRED","NT008"],
      note="高野山宿坊（福智院）+ 奥之院 + 熊野本宫/那智大社/那智瀑布 + 瀞峡游船 + 川汤/汤峰温泉。KM003/SL003 为 12 天高野山 2N + 京都 3N + 高山 2N（白川乡包车）；NT006 夏季北山川筏流版；NT007 高野山 > 熊野 > 白滨 11 天；NT008 熊野 → 伊势 8 天（徒步段发心门王子 → 本宫 7.5km）。"),
 dict(id="F07", name="濑户内 · 四国（艺术岛与港町线）", name_en="Setouchi & Shikoku",
      skeleton=[("Tokyo",2),("Onomichi",1),("Tomonoura",1),("Hiroshima",2),("Dogo Onsen",2),("Osaka",2)], days="11–15D", standard="SE003",
      members=["SE001","SE002","SE003","SE004","SE005"],
      note="直岛/丰岛艺术岛、仓敷美观地区、尾道、鞆之浦、岛波海道、松山道后温泉；SE002 15 天深入四国；SE005 加出云大社；SE001 加姬路城与温泉旅馆。"),
 dict(id="F08", name="九州温泉线（福冈进出）", name_en="Kyushu Onsen Circuit",
      skeleton=[("Fukuoka",2),("Kagoshima",1),("Ibusuki",1),("Kumamoto",1),("Takachiho",1),("Beppu",2)], days="9–13D", standard="KY003",
      members=["KY001","KY002","KY003","KY004","KY005"],
      note="KY003 南九州版（仙岩园、指宿砂浴、玉手箱观光列车、阿苏、高千穗峡、别府地狱）；KY001 西九州版（长崎、熊本、高千穗、别府）；KY002 陶瓷小镇 + 嬉野 + 豪斯登堡 + 长崎 3N；KY004/KY005 尊享版 12–13 天（云仙、柳川、日田，旅馆含晚餐）。"),
 dict(id="F09", name="北海道夏季自然线（5–10 月）", name_en="Hokkaido Summer",
      skeleton=[("Sapporo",2),("Sounkyo",1),("Lake Akan",1),("Shiretoko",2)], days="7D", standard="HD001",
      members=["HD001","HD002"],
      note="HD001 道东（层云峡、屈斜路湖、知床、阿寒湖，3 天包车）；HD002 道南（札幌/小樽 > 登别地狱谷·洞爷湖包车 > 函馆 2N）。"),
 dict(id="F10", name="北海道滑雪线（12–3 月）", name_en="Hokkaido Ski",
      skeleton=[("Sapporo",3),("Rusutsu",4)], days="8–12D", standard="HK005",
      members=["HK001","HK002","HK003","HK004","HK005","HK006","HK007","HK008"],
      note="留寿都 / 富良野 / 佐幌 / 旭川周边雪场两两组合，前后接札幌或温泉（定山溪、登别）；HK006 为 12 天 + 北海道精华；HK001 跨本州白马栂池。"),
 dict(id="F11", name="本州滑雪线（白马 / 志贺高原 / 藏王）", name_en="Honshu Ski",
      skeleton=[("Yudanaka Onsen",1),("Hakuba",6)], days="11–14D", standard="SK005",
      members=["SK002","SK004","SK005","SK006","SK102"],
      note="雪猴（地狱谷野猿公苑）+ 汤田中温泉 1N + 雪场 6N；两周版加藏王树冰。"),
 dict(id="F12", name="日本阿尔卑斯 · 立山黑部（6–10 月 / 4–5 月雪墙）", name_en="Japan Alps & Tateyama-Kurobe",
      skeleton=[("Tokyo",2),("Matsumoto",2),("Takayama",2),("Kanazawa",2),("Kyoto",2)], days="11–12D", standard="NT005",
      members=["NT004","NT104","NT005","NT105"],
      note="立山黑部阿尔卑斯路线（4–5 月雪之大谷版 NT104/NT105）、松本城、上高地、新穗高、美原高原；NT004 从富士山出发 12 天。"),
 dict(id="F13", name="温泉主题线", name_en="Onsen Journeys",
      skeleton=[("Tokyo",2),("Hakone",2),("Kyoto",3),("Kinosaki Onsen",1)], days="11–14D", standard="HS003",
      members=["HS001","HS002","HS003","KA003","KM004"],
      note="箱根 2N 含晚餐 > 京都 > 城崎温泉七汤；HS001 14 天（东京/姬路/广岛）；HS002 金泽 > 白川乡 > 高山 > 下吕。与 F03/F04 交叉。"),
 dict(id="F14", name="主题乐园线", name_en="Theme Parks",
      skeleton=[("Maihama (Tokyo Bay)",3),("Nagoya",2),("Universal City (Osaka)",3)], days="9–15D", standard="TP004",
      members=["TP004","FG004","TP001","TP101","TP002","TP102","TP003"],
      note="TP004/FG004 纯乐园 9 天（东京迪士尼两园 > 名古屋乐高/吉卜力 > 大阪环球影城）；TP001–TP003 为黄金路线 + 环球影城 2 天。"),
 dict(id="F15", name="奢华线（帝国饭店 / Green Car / 包车）", name_en="Luxury",
      skeleton=[("Tokyo",2),("Kashikojima",2),("Kyoto",3),("Kanazawa",2),("Tokyo",2)], days="10–12D", standard="LX001",
      members=["LX001","LX002","LX003"],
      note="LX002 琵琶湖·彦根城·近江八幡·大原（4 天包车，椿山庄/Prince 京都宝池/InterContinental 大阪）；LX003 广岛 + 京都（Suiran 岚山）。"),
]
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
L = ["# 行程归并：标准行程家族（Self-Guided Japan 88 条线路 → 15 个家族）", "",
     "归并依据：**住宿城市骨架**（城市顺序 + 过夜数）相同或仅差 1–2 个节点的线路视为同一家族；家族内选一条数据最完整的作为「标准行程」，其余列为变体并注明差异。价格为每人、两人一房、不含国际机票（SOLO 为单人价）。",
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
        if not t:
            L.append(f"| {m} | （未在目录中） |  |  |  |  |  |"); continue
        tag = "**标准**" if m == f["standard"] else ("豪华版" if t.get("deluxe") else "变体")
        extra = []
        others = sorted(tour_fams[m] - {f["id"]})
        if others: extra.append("也属 " + "/".join(others))
        if t.get("season"): extra.append(f"季节 {t['season']}")
        L.append(f"| {m} | {t['title_en'] or ''} | {t.get('title_cn') or ''} | {t['days'] or '?'}D | {route_of(t) or '—'} | {price(t)} | {tag}{'；' + '；'.join(extra) if extra else ''} |")
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
        A += [f"### {city} {ccn}".strip(), "", "| 景点 | 中文 | 类别 | 线路数 | 等级 | 家族 tag | 出现线路 |", "|---|---|---|---|---|---|---|"]
        for a in items:
            lvl = "核心" if a["_count"] >= 3 else ("常见" if a["_count"] == 2 else "可选")
            fams = " ".join(f"`{x}`" for x in a["_fams"]) or "—"
            A.append(f"| {a['name_en']} | {a['name_cn']} | {a.get('category_cn') or a['category'] or '—'} | {a['_count']} | {lvl} | {fams} | {a['tours'] or '（目的地指南）'} |")
        A.append("")
A += ["## 城市汇总", "", "| 区域 | 城市 | 核心 | 常见 | 可选 |", "|---|---|---|---|---|"]
for reg, city, ccn, c1, c2, c3 in summary: A.append(f"| {reg} | {city} {ccn} | {c1} | {c2} | {c3} |")
A += ["", "家族代号对照：" + "；".join(f"`{k}` {v}" for k, v in FAM_NAME.items())]
with open(os.path.join(OUT, "attractions_by_city.md"), "w", encoding="utf-8") as fo: fo.write("\n".join(A))
rows = []
for a in attrs:
    rows.append(OrderedDict([(k, a.get(k, "")) for k in ("name_en","name_cn","name_ja","city","city_cn","region","region_cn","category","category_cn","tour_count")] +
                            [("level", "core" if a["_count"] >= 3 else ("common" if a["_count"] == 2 else "optional")), ("families", " ".join(a["_fams"])), ("tours", a["tours"]), ("description", a["description"])]))
with open(os.path.join(OUT, "attractions_by_city.csv"), "w", newline="", encoding="utf-8-sig") as fo:
    w = csv.DictWriter(fo, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"families={len(FAMILIES)}, assigned={len(primary)}, unassigned={unassigned}, attractions={len(attrs)}")
