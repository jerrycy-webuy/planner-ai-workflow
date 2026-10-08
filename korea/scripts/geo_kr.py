# -*- coding: utf-8 -*-
"""韩国城市 → 中文 / 区域（道）。key 为小写去空格的英文名。"""
import re

REGIONS = {
    "capital": ("Seoul Capital Area", "首都圈（首尔/仁川/京畿）"),
    "gangwon": ("Gangwon", "江原道"),
    "chungcheong": ("Chungcheong", "忠清道"),
    "jeolla": ("Jeolla", "全罗道"),
    "gyeongbuk": ("Gyeongsangbuk-do / Daegu", "庆尚北道·大邱"),
    "gyeongnam": ("Gyeongsangnam-do / Busan / Ulsan", "庆尚南道·釜山·蔚山"),
    "jeju": ("Jeju", "济州"),
}

# key: (英文名, 中文名, 区域)
CITIES = {
    "seoul": ("Seoul", "首尔", "capital"), "incheon": ("Incheon", "仁川", "capital"), "gimpo": ("Gimpo", "金浦", "capital"),
    "ganghwa": ("Ganghwa", "江华岛", "capital"), "paju": ("Paju", "坡州", "capital"), "suwon": ("Suwon", "水原", "capital"),
    "yongin": ("Yongin", "龙仁", "capital"), "gapyeong": ("Gapyeong", "加平", "capital"), "pocheon": ("Pocheon", "抱川", "capital"),
    "yangpyeong": ("Yangpyeong", "杨平", "capital"), "goyang": ("Goyang (Ilsan)", "高阳（一山）", "capital"), "icheon": ("Icheon", "利川", "capital"),
    "gwangmyeong": ("Gwangmyeong", "光明", "capital"), "yeoju": ("Yeoju", "骊州", "capital"), "anseong": ("Anseong", "安城", "capital"),
    "chuncheon": ("Chuncheon", "春川", "gangwon"), "namiisland": ("Nami Island", "南怡岛", "gangwon"), "pyeongchang": ("Pyeongchang", "平昌", "gangwon"),
    "gangneung": ("Gangneung", "江陵", "gangwon"), "sokcho": ("Sokcho", "束草", "gangwon"), "yangyang": ("Yangyang", "襄阳", "gangwon"),
    "hongcheon": ("Hongcheon", "洪川", "gangwon"), "wonju": ("Wonju", "原州", "gangwon"), "jeongseon": ("Jeongseon", "旌善", "gangwon"),
    "hwacheon": ("Hwacheon", "华川", "gangwon"), "yeongwol": ("Yeongwol", "宁越", "gangwon"), "samcheok": ("Samcheok", "三陟", "gangwon"),
    "donghae": ("Donghae", "东海", "gangwon"), "hoengseong": ("Hoengseong", "横城", "gangwon"), "inje": ("Inje", "麟蹄", "gangwon"), "cheorwon": ("Cheorwon", "铁原", "gangwon"),
    "daejeon": ("Daejeon", "大田", "chungcheong"), "buyeo": ("Buyeo", "扶余", "chungcheong"), "gongju": ("Gongju", "公州", "chungcheong"),
    "danyang": ("Danyang", "丹阳", "chungcheong"), "jecheon": ("Jecheon", "堤川", "chungcheong"), "cheongju": ("Cheongju", "清州", "chungcheong"),
    "taean": ("Taean", "泰安", "chungcheong"), "boryeong": ("Boryeong", "保宁", "chungcheong"), "yesan": ("Yesan", "礼山", "chungcheong"),
    "seosan": ("Seosan", "瑞山", "chungcheong"), "boeun": ("Boeun", "报恩", "chungcheong"), "jincheon": ("Jincheon", "镇川", "chungcheong"),
    "chungju": ("Chungju", "忠州", "chungcheong"), "asan": ("Asan", "牙山", "chungcheong"),
    "jeonju": ("Jeonju", "全州", "jeolla"), "gwangju": ("Gwangju", "光州", "jeolla"), "yeosu": ("Yeosu", "丽水", "jeolla"),
    "suncheon": ("Suncheon", "顺天", "jeolla"), "mokpo": ("Mokpo", "木浦", "jeolla"), "damyang": ("Damyang", "潭阳", "jeolla"),
    "boseong": ("Boseong", "宝城", "jeolla"), "gunsan": ("Gunsan", "群山", "jeolla"), "jeongeup": ("Jeongeup", "井邑", "jeolla"),
    "wando": ("Wando", "莞岛", "jeolla"), "haenam": ("Haenam", "海南", "jeolla"), "sinan": ("Sinan (Jeungdo)", "新安（曾岛）", "jeolla"),
    "gurye": ("Gurye", "求礼", "jeolla"), "gwangyang": ("Gwangyang", "光阳", "jeolla"), "jangseong": ("Jangseong", "长城", "jeolla"),
    "wanju": ("Wanju", "完州", "jeolla"), "namwon": ("Namwon", "南原", "jeolla"),
    "daegu": ("Daegu", "大邱", "gyeongbuk"), "gyeongju": ("Gyeongju", "庆州", "gyeongbuk"), "andong": ("Andong", "安东", "gyeongbuk"),
    "pohang": ("Pohang", "浦项", "gyeongbuk"), "mungyeong": ("Mungyeong", "闻庆", "gyeongbuk"), "ulleungdo": ("Ulleungdo", "郁陵岛", "gyeongbuk"),
    "cheongdo": ("Cheongdo", "清道", "gyeongbuk"), "yeongju": ("Yeongju", "荣州", "gyeongbuk"),
    "busan": ("Busan", "釜山", "gyeongnam"), "ulsan": ("Ulsan", "蔚山", "gyeongnam"), "geoje": ("Geoje", "巨济", "gyeongnam"),
    "tongyeong": ("Tongyeong", "统营", "gyeongnam"), "changwon": ("Changwon (Jinhae)", "昌原（镇海）", "gyeongnam"), "gimhae": ("Gimhae", "金海", "gyeongnam"),
    "namhae": ("Namhae", "南海", "gyeongnam"), "jinju": ("Jinju", "晋州", "gyeongnam"), "hadong": ("Hadong", "河东", "gyeongnam"),
    "yangsan": ("Yangsan", "梁山", "gyeongnam"), "miryang": ("Miryang", "密阳", "gyeongnam"), "sacheon": ("Sacheon", "泗川", "gyeongnam"),
    "jeju": ("Jeju", "济州", "jeju"), "seogwipo": ("Seogwipo", "西归浦", "jeju"), "udo": ("Udo Island", "牛岛", "jeju"),
}

ALIAS = {
    "jejuisland": "jeju", "jejucity": "jeju", "jejudo": "jeju", "seoulcity": "seoul", "myeongdong": "seoul", "gimpoairport": "gimpo",
    "incheonairport": "incheon", "icn": "incheon", "gmp": "gimpo", "cju": "jeju", "pus": "busan", "gimhaeairport": "busan",
    "jinhae": "changwon", "ilsan": "goyang", "goyangilsan": "goyang", "nami": "namiisland", "namiislandgapyeong": "namiisland",
    "everland": "yongin", "alpensia": "pyeongchang", "yongpyong": "pyeongchang", "yongpyongresort": "pyeongchang", "phoenixpark": "pyeongchang",
    "vivaldipark": "hongcheon", "sonovivaldipark": "hongcheon", "wellihillipark": "hoengseong", "highone": "jeongseon", "highoneresort": "jeongseon",
    "elysiangangchon": "chuncheon", "seorak": "sokcho", "seoraksan": "sokcho", "jeungdo": "sinan", "jeungdoisland": "sinan",
    "gyeonggi": "seoul", "gyeonggido": "seoul", "skiresort": "gangwon_region", "gangwondo": "gangwon_region", "ganghwado": "ganghwa", "ganghwaisland": "ganghwa",
    "songdo": "incheon", "wolmido": "incheon", "haeundae": "busan", "jejuairport": "jeju", "udoisland": "udo", "seogwipocity": "seogwipo",
    "dmz": "paju", "imjingak": "paju", "gyeongjucity": "gyeongju", "suncheonbay": "suncheon", "boseonggreentea": "boseong",
}

def norm(s):
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[^a-z0-9]", "", s)
    return s

def key_of(name):
    k = norm(name)
    k = re.sub(r"(station|airport|city|island|terminal)$", "", k) if k not in CITIES and k not in ALIAS else k
    k = ALIAS.get(k, k)
    return k

def city_info(key):
    """返回 (中文, 区域英文, 区域中文)。"""
    c = CITIES.get(key)
    if not c:
        return (None, None, None)
    r = REGIONS[c[2]]
    return (c[1], r[0], r[1])

def region_key(key):
    c = CITIES.get(key)
    return c[2] if c else None

def is_city(key):
    return key in CITIES
