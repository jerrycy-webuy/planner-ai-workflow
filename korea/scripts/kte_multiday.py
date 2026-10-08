# -*- coding: utf-8 -*-
"""koreatraveleasy.com（KTE）多日团：页面是 WordPress 自由排版，逐日结构按 2026-10-08 抓取的页面人工转写。
价格：站点按房价（US$/room），这里折成每人（两人一房）。KTE 是首尔本地地接（英文团、拼团、首尔出发），不含国际机票。
"""

_W1 = {"city": "Jeonju", "from": "Seoul", "transport": "Coach", "spots": ["Gongsanseong Fortress", "Tomb of King Muryeong", "Gongju National Museum"], "stay": "Jeonju", "meals": "LD", "title": "Seoul > Gongju > Jeonju"}
_W2 = {"city": "Gwangju", "from": "Jeonju", "transport": "Coach", "spots": ["Jeonju Hanok Village", "Baekyangsa Temple (Jangseong)"], "stay": "Gwangju", "meals": "BLD", "title": "Jeonju > Jangseong > Gwangju"}
_W3 = {"city": "Busan", "from": "Gwangju", "transport": "Coach", "spots": ["Boseong Green Tea Plantation (Daehan Dawon)", "Suncheon Bay Wetland (Naganeupseong Folk Village on last Monday)"], "stay": "Busan", "meals": "BLD", "title": "Boseong > Suncheon > Busan"}
_B1 = {"city": "Busan", "spots": ["UN Memorial Cemetery", "Jagalchi Market", "Songdo Sea Cable Car"], "stay": "Busan", "meals": "BL", "title": "Busan city tour"}
_E2 = {"city": "Gyeongju", "from": "Busan", "transport": "Coach", "spots": ["Nurimaru APEC House", "Bulguksa Temple", "Daereungwon Ancient Tomb Complex", "Gyeongju National Museum", "Cheomseongdae Observatory"], "stay": "Gyeongju", "meals": "BLD", "title": "Busan > Gyeongju"}
_E3 = {"city": "Pyeongchang", "from": "Gyeongju", "transport": "Coach", "spots": ["Daegu Korean Traditional Culture Center (8+ pax) / Donggung Palace and Wolji Pond", "Andong Hahoe Folk Village"], "stay": "Pyeongchang", "meals": "BLD", "title": "Daegu or Gyeongju > Andong > Pyeongchang"}
_E4 = {"city": "Seoul", "from": "Pyeongchang", "transport": "Coach", "spots": ["Seoraksan National Park (Jujeongol Valley)"], "stay": None, "meals": "BL", "title": "Pyeongchang > Yangyang > Seoul"}

TOURS = [
    {"code": "KTE-RT7", "url": "https://www.koreatraveleasy.com/product/korea-round-tour-7-days-all-inclusive-package/", "tour_type": "join_in_group",
     "style": "Join-in group (English, from Seoul)", "title_en": "Korea Round Tour 7 Days All-inclusive Package", "title_cn": "韩国环岛 7 天全包拼团",
     "season": "2026-03 ~ 2026-11 每周六出发", "price": {"min": 1373, "max": 1724, "currency": "USD", "note": "Essential US$2,746 / All-inclusive US$3,448 每房（两人）→ 每人；首尔出发、不含机票"},
     "hotels_note": "All-inclusive 4–5★：Lahan Hotel Jeonju · Holiday Inn Gwangju · Grand Josun Busan (2N) · Lahan Select Gyeongju · InterContinental Pyeongchang",
     "days": [dict(_W1, hotel="Lahan Hotel Jeonju"), dict(_W2, hotel="Holiday Inn Gwangju"), dict(_W3, hotel="Grand Josun Busan"), dict(_B1, hotel="Grand Josun Busan"),
              dict(_E2, hotel="Lahan Select Gyeongju"), dict(_E3, hotel="InterContinental Alpensia Pyeongchang"), _E4]},
    {"code": "KTE-W4", "url": "https://www.koreatraveleasy.com/product/eastern-western-korea-tour-4-days-all-inclusive-package/", "tour_type": "join_in_group",
     "style": "Join-in group (English, from Seoul)", "title_en": "Western Korea 4-Day Tour (Gongju–Jeonju–Gwangju–Busan)", "title_cn": "韩国西线 4 天拼团（公州·全州·光州·釜山）",
     "season": "2026-03 ~ 2026-11 每周六出发", "price": {"min": 655, "max": 655, "currency": "USD", "note": "US$1,309 起每房（两人）→ 每人；首尔出发、末日 KTX/包车回首尔"},
     "days": [dict(_W1, hotel="Lahan Hotel Jeonju"), dict(_W2, hotel="Holiday Inn Gwangju"), dict(_W3, hotel="Grand Josun Busan"),
              {"city": "Seoul", "from": "Busan", "transport": "KTX (≤9 pax) / Coach", "spots": ["UN Memorial Cemetery"], "stay": None, "meals": "BL", "title": "Busan > Seoul"}]},
    {"code": "KTE-E4", "url": "https://www.koreatraveleasy.com/product/eastern-western-korea-tour-4-days-all-inclusive-package/", "tour_type": "join_in_group",
     "style": "Join-in group (English, from Seoul)", "title_en": "Eastern Korea 4-Day Tour (Busan–Gyeongju–Andong–Seorak)", "title_cn": "韩国东线 4 天拼团（釜山·庆州·安东·雪岳山）",
     "season": "2026-03 ~ 2026-11 每周二出发", "price": {"min": 655, "max": 655, "currency": "USD", "note": "US$1,309 起每房（两人）→ 每人；首尔出发 KTX(≤9 pax)/包车"},
     "days": [{"city": "Busan", "from": "Seoul", "transport": "KTX (≤9 pax) / Coach", "spots": ["Jagalchi Market", "Songdo Sea Cable Car"], "stay": "Busan", "meals": "L", "title": "Seoul > Busan", "hotel": "Grand Josun Busan"},
              dict(_E2, hotel="Lahan Select Gyeongju"), dict(_E3, hotel="InterContinental Alpensia Pyeongchang"), _E4]},
    {"code": "KTE-UK16", "url": "https://www.koreatraveleasy.com/product/ultimate-korea-jeju-island-all-inclusive-tour-package/", "tour_type": "join_in_group",
     "style": "Join-in group (English) + private transfers", "title_en": "Ultimate Korea & Jeju Island All-inclusive 16 Days", "title_cn": "韩国全境 + 济州岛 16 天全包",
     "season": "2026-03 ~ 2026-11", "price": {"min": 3939, "max": 3939, "currency": "USD", "note": "US$7,878 每房（两人）→ 每人；含首尔进出、济州往返国内段，不含国际机票"},
     "days": [{"city": "Seoul", "from": "Incheon", "transport": "Airport transfer", "spots": [], "stay": "Seoul", "title": "Arrive Incheon > Seoul"},
              dict(_W1, hotel="Lahan Hotel Jeonju"), dict(_W2, spots=["Jeonju Hanok Village with Hanbok experience", "Baekyangsa Temple tea ceremony"], hotel="Holiday Inn Gwangju"),
              dict(_W3, hotel="Grand Josun Busan"), dict(_B1, hotel="Grand Josun Busan"), dict(_E2, hotel="Lahan Select Gyeongju"),
              dict(_E3, hotel="InterContinental Alpensia Pyeongchang"), dict(_E4, stay="Seoul"),
              {"city": "Jeju", "from": "Seoul", "transport": "Flight (GMP-CJU)", "spots": ["Jeju Stone Park", "Bijarim Forest", "Seongsan Ilchulbong"], "stay": "Jeju", "meals": "BLD", "title": "Seoul > Jeju"},
              {"city": "Jeju", "spots": ["Jusangjeolli Cliff", "Cheonjeyeon Falls", "O'Sulloc Tea Museum", "Gotjawal Jeju Fantasy Forest foot bath", "Hallim Park"], "stay": "Jeju", "meals": "BLD", "title": "Jeju full day"},
              {"city": "Seoul", "from": "Jeju", "transport": "Flight (CJU-GMP)", "spots": [], "stay": "Seoul", "meals": "B", "title": "Jeju > Seoul"},
              {"city": "Seoul", "spots": ["Gwanghwamun Square", "Jogyesa Temple", "Gyeongbokgung Palace", "National Folk Museum"], "stay": "Seoul", "meals": "B", "title": "Seoul morning tour"},
              {"city": "Seoul", "spots": ["Imjingak Park", "3rd Tunnel", "Dora Observatory", "NANTA show Myeongdong"], "stay": "Seoul", "meals": "B", "title": "DMZ & NANTA"},
              {"city": "Seoul", "spots": ["Nami Island", "Lotte World Tower Seoul Sky"], "stay": "Seoul", "meals": "B", "title": "Nami Island & Seoul Sky"},
              {"city": "Seoul", "spots": ["Han River Park", "Han River night cruise"], "stay": "Seoul", "meals": "B", "title": "Han River night"},
              {"city": "Incheon", "from": "Seoul", "transport": "Airport transfer", "spots": [], "stay": None, "meals": "B", "title": "Depart Incheon"}]},
    {"code": "KTE-ULL3", "url": "https://www.koreatraveleasy.com/product/ulleungdo-tour-package-from-seoul-3-days-2-nights-pohang-dokdo/", "tour_type": "join_in_group",
     "style": "Join-in group (from Seoul, overnight ferry)", "title_en": "Ulleungdo 3D2N from Seoul (Pohang / Dokdo)", "title_cn": "郁陵岛 3 天 2 夜（首尔出发，浦项夜船）",
     "season": "夏季指定日期", "price": {"min": 420, "max": 420, "currency": "USD", "note": "US$420 起每人；首尔出发，含往返船票，第 1 晚在船上"},
     "days": [{"city": "Pohang", "from": "Seoul", "transport": "Coach + overnight ferry", "spots": [], "stay": None, "title": "Seoul > Pohang (night ferry)"},
              {"city": "Ulleungdo", "from": "Pohang", "transport": "Ferry", "spots": ["Dodong / Jeodong (Dokdo Observatory)", "Nari Basin", "Taeha sunset trek", "Ulleungdo"], "stay": "Ulleungdo", "meals": "BLD", "title": "Ulleungdo"},
              {"city": "Seoul", "from": "Ulleungdo", "transport": "Ferry to Gangneung + Coach", "spots": ["Jeodong Port"], "stay": None, "meals": "B", "title": "Ulleungdo > Gangneung > Seoul"}]},
    {"code": "KTE-GW2", "url": "https://www.koreatraveleasy.com/product/summer-gangwondo-2d-1n-all-inclusive-overnight-tour/", "tour_type": "join_in_group",
     "style": "Join-in group (KTX from Seoul)", "title_en": "Summer Gangwon-do 2D1N (Donghae–Gangneung)", "title_cn": "江原道夏季 2 天 1 夜（东海·江陵）",
     "season": "夏季指定日期", "price": {"min": None, "max": None, "currency": "USD", "note": "价格见页面选项"},
     "days": [{"city": "Donghae", "from": "Seoul", "transport": "KTX", "spots": ["Cheongok Golden Bat Cave", "Nongoldam-gil", "Mukho Market", "Chuam Candlestick Rock"], "stay": "Gangneung", "meals": "L", "title": "Seoul > Donghae"},
              {"city": "Seoul", "from": "Gangneung", "transport": "KTX", "spots": ["Jeongdongjin Badabuchae-gil", "Gangneung Jungang Market", "Ojukheon House", "Gyeongpodae Beach", "Anmok Beach coffee street"], "stay": None, "meals": "B", "title": "Gangneung > Seoul"}]},
]
