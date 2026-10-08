# -*- coding: utf-8 -*-
"""台湾地接模板的预填清单（人工整理的常见团体景点/路段/节庆，供地接直接填价；非竞品抓取数据）。"""

# (縣市, 景點英文, 景點中文, 類別, 建議停留小時)
ATTRACTIONS = [
    ("台北 Taipei", "Taipei 101 Observatory", "台北101觀景台", "觀景台", 1.5), ("台北 Taipei", "National Palace Museum", "國立故宮博物院", "博物館", 2),
    ("台北 Taipei", "Chiang Kai-shek Memorial Hall", "中正紀念堂", "史蹟", 1), ("台北 Taipei", "Longshan Temple", "艋舺龍山寺", "寺廟", 0.5),
    ("台北 Taipei", "Ximending", "西門町", "街區", 2), ("台北 Taipei", "Shilin Night Market", "士林夜市", "夜市", 1.5),
    ("台北 Taipei", "Raohe Night Market", "饒河街觀光夜市", "夜市", 1.5), ("台北 Taipei", "Yangmingshan National Park", "陽明山國家公園", "自然", 2),
    ("台北 Taipei", "Beitou Hot Spring", "北投溫泉", "溫泉", 2), ("台北 Taipei", "Maokong Gondola", "貓空纜車", "纜車", 1.5),
    ("台北 Taipei", "Dadaocheng & Dihua Street", "大稻埕·迪化街", "老街", 1), ("台北 Taipei", "Huashan 1914 Creative Park", "華山1914文創園區", "文創", 1),
    ("新北 New Taipei", "Jiufen Old Street", "九份老街", "老街", 2), ("新北 New Taipei", "Shifen Sky Lantern & Waterfall", "十分天燈·十分瀑布", "體驗", 1.5),
    ("新北 New Taipei", "Yehliu Geopark", "野柳地質公園", "自然", 1.5), ("新北 New Taipei", "Tamsui Old Street & Fisherman's Wharf", "淡水老街·漁人碼頭", "老街", 2),
    ("新北 New Taipei", "Houtong Cat Village", "猴硐貓村", "村落", 1), ("新北 New Taipei", "Gold Museum (Jinguashi)", "黃金博物館（金瓜石）", "博物館", 1.5),
    ("新北 New Taipei", "Wulai Hot Spring & Atayal Village", "烏來溫泉·泰雅部落", "溫泉", 2), ("新北 New Taipei", "Yingge Ceramics Old Street", "鶯歌陶瓷老街", "老街", 1.5),
    ("基隆 Keelung", "Miaokou Night Market", "基隆廟口夜市", "夜市", 1), ("基隆 Keelung", "Heping Island Geopark", "和平島地質公園", "自然", 1),
    ("桃園 Taoyuan", "Daxi Old Street", "大溪老街", "老街", 1), ("桃園 Taoyuan", "Xpark Aquarium", "Xpark 水族館", "主題樂園", 2),
    ("新竹 Hsinchu", "Neiwan Old Street", "內灣老街", "老街", 1), ("苗栗 Miaoli", "Shengxing Station & Longteng Bridge", "勝興車站·龍騰斷橋", "史蹟", 1),
    ("宜蘭 Yilan", "Jiaoxi Hot Spring", "礁溪溫泉", "溫泉", 2), ("宜蘭 Yilan", "National Center for Traditional Arts", "國立傳統藝術中心", "文創", 2),
    ("宜蘭 Yilan", "Lanyang Museum", "蘭陽博物館", "博物館", 1), ("宜蘭 Yilan", "Taipingshan", "太平山國家森林遊樂區", "自然", 4),
    ("花蓮 Hualien", "Taroko Gorge (Swallow Grotto / Tunnel of Nine Turns)", "太魯閣國家公園（燕子口·九曲洞）", "自然", 3), ("花蓮 Hualien", "Eternal Spring Shrine", "長春祠", "自然", 0.5),
    ("花蓮 Hualien", "Qingshui Cliff", "清水斷崖", "自然", 0.5), ("花蓮 Hualien", "Qixingtan Beach", "七星潭", "海岸", 1),
    ("花蓮 Hualien", "Dongdamen Night Market", "東大門夜市", "夜市", 1.5), ("花蓮 Hualien", "Liyu Lake", "鯉魚潭", "自然", 1),
    ("台東 Taitung", "Sanxiantai", "三仙台", "海岸", 1), ("台東 Taitung", "Mr. Brown Avenue (Chishang)", "伯朗大道（池上）", "自然", 1),
    ("台東 Taitung", "Luye Highland", "鹿野高台", "自然", 1), ("台東 Taitung", "Zhiben Hot Spring", "知本溫泉", "溫泉", 2),
    ("台中 Taichung", "Gaomei Wetlands", "高美濕地", "自然", 1.5), ("台中 Taichung", "Rainbow Village", "彩虹眷村", "文創", 0.5),
    ("台中 Taichung", "Miyahara", "宮原眼科", "伴手禮", 0.5), ("台中 Taichung", "Fengjia Night Market", "逢甲夜市", "夜市", 2),
    ("台中 Taichung", "Wuling Farm", "武陵農場", "自然", 3), ("彰化 Changhua", "Lukang Old Street", "鹿港老街", "老街", 1.5),
    ("南投 Nantou", "Sun Moon Lake Cruise", "日月潭遊湖", "遊船", 1.5), ("南投 Nantou", "Sun Moon Lake Ropeway", "日月潭纜車", "纜車", 1.5),
    ("南投 Nantou", "Wenwu Temple", "文武廟", "寺廟", 0.5), ("南投 Nantou", "Ita Thao", "伊達邵", "村落", 1),
    ("南投 Nantou", "Cingjing Farm", "清境農場", "牧場", 2), ("南投 Nantou", "Hehuanshan", "合歡山", "自然", 2),
    ("南投 Nantou", "Xitou Nature Education Area & Monster Village", "溪頭自然教育園區·妖怪村", "自然", 2),
    ("嘉義 Chiayi", "Alishan National Forest Recreation Area", "阿里山國家森林遊樂區", "自然", 4), ("嘉義 Chiayi", "Alishan Forest Railway", "阿里山林業鐵路", "火車", 1),
    ("嘉義 Chiayi", "Alishan Sunrise (Zhushan)", "阿里山祝山日出", "自然", 2), ("嘉義 Chiayi", "Fenqihu Old Street", "奮起湖老街", "老街", 1),
    ("台南 Tainan", "Chihkan Tower", "赤崁樓", "史蹟", 0.5), ("台南 Tainan", "Anping Old Fort & Tree House", "安平古堡·安平樹屋", "史蹟", 1.5),
    ("台南 Tainan", "Shennong Street", "神農街", "老街", 1), ("台南 Tainan", "Chimei Museum", "奇美博物館", "博物館", 2),
    ("台南 Tainan", "Jingzaijiao Salt Field", "井仔腳瓦盤鹽田", "自然", 1), ("高雄 Kaohsiung", "Pier-2 Art Center", "駁二藝術特區", "文創", 1.5),
    ("高雄 Kaohsiung", "Lotus Pond & Dragon Tiger Pagodas", "蓮池潭龍虎塔", "寺廟", 1), ("高雄 Kaohsiung", "Fo Guang Shan Buddha Museum", "佛光山佛陀紀念館", "寺廟", 2),
    ("高雄 Kaohsiung", "Cijin Island", "旗津", "海岸", 2), ("高雄 Kaohsiung", "Formosa Boulevard Station", "美麗島站光之穹頂", "地標", 0.5),
    ("高雄 Kaohsiung", "Liuhe Night Market", "六合夜市", "夜市", 1.5), ("屏東 Pingtung", "Kenting National Park (Eluanbi Lighthouse)", "墾丁國家公園（鵝鑾鼻燈塔）", "自然", 2),
    ("屏東 Pingtung", "Maobitou", "貓鼻頭", "海岸", 0.5), ("屏東 Pingtung", "Kenting Street Night Market", "墾丁大街", "夜市", 1.5),
    ("屏東 Pingtung", "National Museum of Marine Biology & Aquarium", "國立海洋生物博物館", "博物館", 2.5),
]

# (路段, 方式, 參考車程)
SEGMENTS = [
    ("桃園機場 TPE → 台北市區", "遊覽車 Coach", "1h"), ("台北 → 宜蘭（雪山隧道）", "遊覽車 Coach", "1h"), ("宜蘭 → 花蓮（蘇花改）", "遊覽車 Coach", "2h"),
    ("台北 → 花蓮", "台鐵 太魯閣/普悠瑪號 TRA", "2h10m"), ("花蓮 → 台東（花東縱谷）", "遊覽車 Coach", "3h"), ("台東 → 墾丁（南迴）", "遊覽車 Coach", "2h30m"),
    ("墾丁 → 高雄", "遊覽車 Coach", "2h"), ("高雄 → 台南", "遊覽車 Coach", "1h"), ("台南 → 阿里山", "遊覽車 Coach（山區中巴）", "3h"),
    ("阿里山 → 日月潭", "遊覽車 Coach", "3h30m"), ("日月潭 → 台中", "遊覽車 Coach", "1h30m"), ("台中 → 台北", "遊覽車 Coach", "2h30m"),
    ("台北 → 台中", "高鐵 HSR", "50m"), ("台北 → 左營（高雄）", "高鐵 HSR", "1h35m"), ("台中 → 清境 / 合歡山", "遊覽車 Coach（山區限中巴）", "2h"),
    ("高雄 KHH 機場接送", "遊覽車 Coach", "—"), ("台中 RMQ 機場接送", "遊覽車 Coach", "—"), ("松山 TSA 機場接送", "遊覽車 Coach", "—"),
]

# (名稱, 時間（2027，請地接確認）, 影響)
SEASONS = [
    ("春節 Lunar New Year", "2027-02-05 ~ 02-10（以官方公布為準）", "酒店旺季加價、餐廳休息多、遊覽車司機加班費"),
    ("元宵 / 平溪天燈節", "2027-02-20 前後", "十分/平溪人潮管制，需預約接駁"), ("武陵櫻花季", "2 月中 ~ 3 月上旬", "武陵農場總量管制、需預約入園"),
    ("阿里山花季（櫻花）", "3 月中 ~ 4 月中", "阿里山交通管制、小火車一票難求"), ("清明連假", "2027-04-03 ~ 04-06", "國旅高峰，酒店滿房"),
    ("賞螢 / 油桐花", "4 月 ~ 5 月", "夜間活動，需安排導覽"), ("梅雨季", "5 月 ~ 6 月", "山區落石、行程備案"),
    ("端午節", "2027-06-09 前後", "連假加價"), ("颱風季", "7 月 ~ 9 月", "停班停課時改行程/退費政策需註明"),
    ("暑假（國旅 / 陸客）", "7 月 ~ 8 月", "墾丁、花東酒店旺季價"), ("中秋節", "2027-09-15 前後", "烤肉潮、連假加價"),
    ("國慶日", "10 月 10 日", "台北封路、酒店加價"), ("跨年 101 煙火", "12 月 31 日", "台北酒店 3–5 倍價、信義區封路"),
    ("合歡山降雪", "1 月 ~ 2 月（不定期）", "需雪鏈、交通管制，遊覽車不一定能上山"), ("太魯閣步道 / 蘇花公路管制", "不定期", "地震、落石後封閉，請提供最新開放狀態"),
]

SHOPPING = [("茶葉（高山茶）", "購物站"), ("鳳梨酥 / 伴手禮", "購物站"), ("珊瑚 / 寶石", "購物站"), ("台灣玉 / 玉石", "購物站"), ("靈芝 / 保健品", "購物站"),
            ("免稅店（昇恆昌）", "購物站"), ("日月潭遊湖加纜車", "自費"), ("阿里山日出小火車", "自費"), ("台北 101 觀景台", "自費"), ("溫泉湯屋", "自費")]

MEALS = [("台北 Taipei", "鼎泰豐小籠包套餐", "午 / 晚"), ("台北 Taipei", "台菜合菜（10 人桌）", "午 / 晚"), ("南投 Nantou", "日月潭總統魚 / 奇力魚風味餐", "午"),
         ("嘉義 Chiayi", "阿里山便當 / 山產合菜", "午"), ("台南 Tainan", "台南小吃宴（擔仔麵、虱目魚）", "午 / 晚"), ("花蓮 Hualien", "原住民風味餐", "午 / 晚"),
         ("高雄 Kaohsiung", "海鮮合菜", "晚"), ("台中 Taichung", "火鍋（涮涮鍋）", "晚"), ("宜蘭 Yilan", "溫泉會館自助晚餐", "晚")]
