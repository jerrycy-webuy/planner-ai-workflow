# -*- coding: utf-8 -*-
"""回归：把 kb/tours.json 的真实线路转成 ItinerarySpec 跑校验器，看误报。用法: python3 -I regress_kr.py [kb_dir] [-v]"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from validate_itinerary import validate_spec

def to_spec(t):
    dd = t["days_detail"]
    return {"code": t["code"], "title_en": t["title_en"], "title_cn": t.get("title_cn") or "", "days": len(dd), "nights": t["nights"],
            "entry_airport": "", "exit_airport": "", "tour_type": t["tour_type"],
            "route": [{"city": r["city"], "nights": r["nights"]} for r in t["route"]],
            "days_detail": [{"day": d["day"], "city": d["city"] or "", "from": d.get("from"), "transport": d.get("transport"), "title_cn": d.get("title") or "",
                             "attractions": d["attractions"], "meals": d.get("meals"), "stay": d.get("stay")} for d in dd]}

def main():
    kb = next((a for a in sys.argv[1:] if not a.startswith("-")), os.path.join(HERE, "..", "kb")); verbose = "-v" in sys.argv
    tours = [t for t in json.load(open(os.path.join(kb, "tours.json"), encoding="utf-8")) if t["route"]]
    codes = collections.Counter(); bad = []
    for t in tours:
        spec = to_spec(t)
        errs, warns = validate_spec(spec, kb, t["tour_type"])
        for i in errs + warns: codes[i["code"]] += 1
        if errs: bad.append((t["code"], errs))
        if verbose:
            for i in errs + warns: print(t["code"], i["level"], i["code"], i.get("day"), i["msg"])
    print(f"{len(tours)} 条有住宿线路：{len(tours) - len(bad)} 条无 error；问题分布 {dict(codes.most_common())}")
    for c, errs in bad:
        for e in errs: print(f"  {c} [{e['code']}] D{e.get('day')} {e['msg']}")

if __name__ == "__main__":
    main()
