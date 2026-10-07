# -*- coding: utf-8 -*-
"""线路名 / 景点 中文对照表（人工整理；consolidate.py 会做归一化匹配）。"""

TITLE_CN = {
    "Japan Golden Route Highlights": "日本黄金路线精华",
    "Traditions & Gardens of Japan": "日本传统与庭园",
    "Hidden Gems of Japan: Ise-Shima Escape": "日本秘境：伊势志摩之旅",
    "Hidden Gems of Japan: Ise-Shima Escape – Deluxe": "日本秘境：伊势志摩之旅（豪华版）",
    "Japan Highlights & World Heritage": "日本精华与世界遗产",
    "Timeless Traditions: Kanazawa & Hida Journey": "永恒传统：金泽与飞驒之旅",
    "Timeless Traditions: Shirakawago & Hida Journey": "永恒传统：白川乡与飞驒之旅",
    "Scenic Japan: Culture & Countryside": "风景日本：文化与乡野",
    "Castles & Heritage of West Japan": "西日本名城与遗产",
    "Cultural Essence: Kyoto & Kanazawa Short Escape": "文化精粹：京都金泽短旅",
    "Sea of Serenity: Kashikojima & Cultural Japan": "宁静之海：贤岛与文化日本",
    "Taste Your Way through Japan": "舌尖上的日本",
    "Spirit of Tradition: Shirakawago & Cultural Japan": "传统之魂：白川乡与文化日本",
    "Spirit of Tradition: Shirakawa-go & Cultural Japan": "传统之魂：白川乡与文化日本",
    "Cultural Odyssey: Tokyo to Fukuoka": "文化长旅：东京到福冈",
    "Koyasan: Sacred Sites and Quiet Beauty": "高野山：圣地与静美",
    "SOLO Hidden Gems: Ise-Shima Escape": "单人·日本秘境：伊势志摩",
    "SOLO Koyasan: Sacred Sites and Quiet Beauty": "单人·高野山：圣地与静美",
    "SOLO Castles: Culture & Countryside": "单人·名城：文化与乡野",
    "SOLO Scenic Japan: Culture & Countryside": "单人·风景日本：文化与乡野",
    "SOLO Castles & Heritage of West Japan": "单人·西日本名城与遗产",
    "SOLO Sea of Serenity: Kashikojima & Cultural Japan": "单人·宁静之海：贤岛与文化日本",
    "SOLO/Timeless Traditions: Shirakawago & Hida Journey": "单人·永恒传统：白川乡与飞驒之旅",
    "Vibrant Cities, Scenic Hakone & Shirakawago": "活力都市、箱根风光与白川乡",
    "Family Holidays: Shared Journey Through Japan's Classics": "家庭假期：共游日本经典",
    "Family Holidays: Family Journey to Japan's Classics": "家庭假期：日本经典亲子之旅",
    "Family Holidays: Castles, Villages & Sacred Shrines Together": "家庭假期：名城、村落与神社",
    "Family-Friendly Japan Holiday: Ninja Adventure": "亲子日本假期：忍者冒险",
    "Family Holidays: Tokyo Bay, Creative Parks & Osaka Thrills": "家庭假期：东京湾乐园、创意乐园与大阪刺激之旅",
    "Tokyo Bay, Creative Parks & Osaka Thrills": "东京湾乐园、创意乐园与大阪刺激之旅",
    "15 Days Through Japan & Universal City": "15 天纵览日本与环球影城",
    "Culture, Nature, and Universal City Adventure": "文化、自然与环球影城冒险",
    "Japan Highlights & Theme Park in Osaka": "日本精华与大阪主题乐园",
    "Hidden Kyushu: Nature, Onsen & Culture Adventure": "秘境九州：自然、温泉与文化",
    "Kyushu Discovery: Volcanoes, Onsen & Scenic Wonders": "探索九州：火山、温泉与绝景",
    "Premium Kyushu: Serenity, Onsen & Coastal Heritage": "尊享九州：静谧、温泉与海岸遗产",
    "Discover Hokkaido": "发现北海道",
    "Southern Hokkaido Escape": "道南北海道之旅",
    "Sapporo City Break & Furano Ski": "札幌城市假期与富良野滑雪",
    "Sapporo Discovery & Rusutsu Ski": "探索札幌与留寿都滑雪",
    "Rusutsu & Furano Ski Journey": "留寿都与富良野滑雪之旅",
    "Artful Setouchi & Japan's Timeless Hot Springs": "艺术濑户内与日本经典温泉",
    "Setouchi Shores & Shikoku Heartlands": "濑户内海岸与四国腹地",
    "Setouchi Sea Paths & Historic Port Towns": "濑户内海路与历史港町",
    "Kansai Essentials: Osaka, Nara, and Kyoto": "关西精华：大阪、奈良、京都",
    "Beyond Kansai: Villages & Timeless Japan": "关西之外：村落与永恒日本",
    "Kansai & Setouchi: History, Onsen & Island Beauty": "关西与濑户内：历史、温泉与岛屿之美",
    "Healing Waters & Timeless Towns: Onsen Journey Across Japan": "疗愈之泉与永恒小镇：日本温泉之旅",
    "Hop Through Japan's Hot Springs & Highlights": "穿梭日本温泉与精华",
    "The Art of Onsen: A Premium Japan Experience": "温泉之道：日本尊享体验",
    "From Sacred Mountains to Coastal Calm": "从圣山到静谧海岸",
    "Walking Japan's Coastal & Sacred Trails": "徒步日本海岸与圣道",
    "Sacred Trails & Hot Springs of the Kii Peninsula": "纪伊半岛圣道与温泉",
    "Nature & Trails: Historic Paths & Sacred Kii": "自然与古道：历史小径与神圣纪伊",
    "Alpine Wonders of Central Japan": "中部日本阿尔卑斯奇观",
    "Summer IKADA Rafting & Sacred Trails of Japan": "夏日筏流与日本圣道",
    "Koyasan, Kumano & Shirahama-Wakayama Journey": "高野山、熊野与白滨和歌山之旅",
    "Luxury Japan Journey: Ise-Shima Escape": "奢华日本之旅：伊势志摩",
    "Refined Kansai Journey: Lake Biwa & Castles": "精致关西之旅：琵琶湖与名城",
    "Luxury Journey, Your Way: Hiroshima & Kyoto": "随心奢华之旅：广岛与京都",
}

ATTR_CN = {
    # 东京
    "Sensoji Temple": "浅草寺", "Senso-ji Temple": "浅草寺", "Asakusa": "浅草", "Nakamise Shopping Street": "仲见世商店街",
    "Tokyo Skytree": "东京晴空塔", "Tokyo Sky Tree": "东京晴空塔", "Imperial Palace": "皇居", "Imperial Palace East Gardens": "皇居东御苑",
    "Shibuya Scramble Crossing": "涩谷十字路口", "Shibuya Crossing": "涩谷十字路口", "Shibuya": "涩谷", "Harajuku": "原宿", "Takeshita Street": "竹下通",
    "Meiji Shrine": "明治神宫", "Meiji Jingu": "明治神宫", "Tsukiji Outer Market": "筑地场外市场", "Toyosu Market": "丰洲市场",
    "Ueno Park": "上野公园", "Akihabara": "秋叶原", "Shinjuku": "新宿", "Shinjuku Gyoen": "新宿御苑", "Ginza": "银座",
    "teamLab Planets": "teamLab Planets 数字艺术馆", "teamLab Borderless": "teamLab Borderless 数字艺术馆", "Odaiba": "台场", "Tokyo Tower": "东京塔",
    "Tokyo Disneyland": "东京迪士尼乐园", "Tokyo DisneySea": "东京迪士尼海洋", "Tokyo Disney Resort": "东京迪士尼度假区", "Shibuya Sky": "Shibuya Sky 观景台",
    "Tokyo Metropolitan Government Building": "东京都厅观景台", "Yanaka": "谷中", "Roppongi": "六本木", "Tokyo National Museum": "东京国立博物馆",
    "Hamarikyu Gardens": "滨离宫恩赐庭园", "Sumida River cruise": "隅田川游船", "Kabukicho": "歌舞伎町", "Omoide Yokocho": "回忆横丁",
    "Pokemon Cafe": "宝可梦咖啡厅", "Ghibli Museum": "三鹰之森吉卜力美术馆",
    # 箱根 / 富士
    "Hakone Open-Air Museum": "箱根雕刻之森美术馆", "Lake Ashi": "芦之湖", "Lake Ashinoko": "芦之湖", "Owakudani": "大涌谷", "Hakone Ropeway": "箱根空中缆车",
    "Hakone Shrine": "箱根神社", "Hakone Tozan Railway": "箱根登山铁道", "Hakone Loop": "箱根周游线", "Lake Ashi cruise": "芦之湖海贼船",
    "Mount Fuji": "富士山", "Mt. Fuji": "富士山", "Mt Fuji": "富士山", "Lake Kawaguchiko": "河口湖", "Chureito Pagoda": "新仓山浅间公园忠灵塔",
    "Oshino Hakkai": "忍野八海", "Fuji-Q Highland": "富士急乐园", "Gotemba Premium Outlets": "御殿场奥特莱斯", "Mt. Fuji 5th Station": "富士山五合目",
    # 镰仓 / 日光
    "Kamakura Great Buddha": "镰仓大佛", "Kotoku-in": "高德院（镰仓大佛）", "Hase-dera Temple": "长谷寺", "Tsurugaoka Hachimangu": "鹤冈八幡宫", "Enoshima": "江之岛",
    "Nikko Toshogu Shrine": "日光东照宫", "Kegon Falls": "华严瀑布", "Lake Chuzenji": "中禅寺湖",
    # 金泽
    "Kenroku-en Garden": "兼六园", "Kenrokuen Garden": "兼六园", "Kenrokuen": "兼六园", "Kanazawa Castle": "金泽城", "Kanazawa Castle Park": "金泽城公园",
    "21st Century Museum of Contemporary Art": "金泽 21 世纪美术馆", "Higashi Chaya District": "东茶屋街", "Higashi Chayagai": "东茶屋街",
    "Nagamachi Samurai District": "长町武家屋敷", "Omicho Market": "近江町市场", "Myoryuji (Ninja Temple)": "妙立寺（忍者寺）", "Oyama Shrine": "尾山神社",
    "D.T. Suzuki Museum": "铃木大拙馆", "Kazue-machi": "主计町茶屋街", "Gold leaf experience": "金箔体验",
    # 京都
    "Kiyomizu-dera Temple": "清水寺", "Kiyomizudera": "清水寺", "Gion": "祇园", "Yasaka Shrine": "八坂神社", "Kinkaku-ji Temple": "金阁寺", "Kinkakuji": "金阁寺", "Golden Pavilion": "金阁寺",
    "Arashiyama": "岚山", "Arashiyama Bamboo Grove": "岚山竹林", "Bamboo Grove": "岚山竹林", "Fushimi Inari Taisha": "伏见稻荷大社", "Fushimi Inari Shrine": "伏见稻荷大社",
    "Nishiki Market": "锦市场", "Nijo Castle": "二条城", "Ginkaku-ji": "银阁寺", "Silver Pavilion": "银阁寺", "Philosopher's Path": "哲学之道",
    "Tenryu-ji Temple": "天龙寺", "Togetsukyo Bridge": "渡月桥", "Sanjusangendo": "三十三间堂", "Ryoan-ji": "龙安寺", "Heian Shrine": "平安神宫",
    "Pontocho": "先斗町", "Mount Hiei": "比叡山", "Enryaku-ji": "延历寺", "Sanzen-in": "三千院", "Ohara": "大原", "Byodo-in": "平等院",
    "Kyoto Imperial Palace": "京都御所", "Nanzen-ji": "南禅寺", "Eikando": "永观堂", "Tofuku-ji": "东福寺", "Kodai-ji": "高台寺", "Ninenzaka": "二年坂", "Sannenzaka": "三年坂",
    "Kyoto Tower": "京都塔", "Saga Scenic Railway": "岚山小火车", "Sagano Romantic Train": "岚山小火车", "Hozugawa River Boat Ride": "保津川游船",
    "Kawadoko riverside dining": "川床料理", "Kibune": "贵船", "Kurama": "鞍马", "Uji": "宇治", "Kaiseki": "怀石料理", "Tea ceremony": "茶道体验", "Kimono rental": "和服体验",
    # 奈良
    "Todai-ji Temple": "东大寺", "Todaiji": "东大寺", "Great Buddha": "东大寺大佛", "Nara Park": "奈良公园", "Kasuga Taisha": "春日大社", "Kasuga Taisha Shrine": "春日大社",
    "Kofuku-ji": "兴福寺", "Naramachi": "奈良町", "Isuien Garden": "依水园", "Nara deer": "奈良鹿", "Horyu-ji": "法隆寺",
    # 大阪
    "Osaka Castle": "大阪城", "Dotonbori": "道顿堀", "Shinsekai": "新世界", "Umeda Sky Building": "梅田蓝天大厦", "Universal Studios Japan": "日本环球影城",
    "Universal City": "环球城", "Super Nintendo World": "超级任天堂世界", "Kuromon Market": "黑门市场", "Namba": "难波", "Osaka Aquarium Kaiyukan": "海游馆",
    "Shitennoji": "四天王寺", "Abeno Harukas": "阿倍野 Harukas", "Tsutenkaku": "通天阁", "Minoo Falls": "箕面瀑布", "Osaka Expo": "大阪世博",
    # 神户 / 姬路 / 关西其他
    "Himeji Castle": "姬路城", "Koko-en Garden": "好古园", "Kobe Harborland": "神户港湾乐园", "Kitano Ijinkan": "北野异人馆", "Arima Onsen": "有马温泉", "Kobe beef": "神户牛",
    "Mount Rokko": "六甲山", "Hikone Castle": "彦根城", "Lake Biwa": "琵琶湖", "Omihachiman": "近江八幡", "Miho Museum": "美秀美术馆",
    "Amanohashidate": "天桥立", "Ine Funaya": "伊根舟屋", "Kinosaki Onsen": "城崎温泉", "Seven public baths": "城崎七汤外汤",
    "Iga Ninja Museum": "伊贺流忍者博物馆", "Ninja Museum of Igaryu": "伊贺流忍者博物馆", "Iga Ueno Castle": "伊贺上野城", "Ninja training": "忍者体验",
    # 高野山 / 熊野 / 和歌山
    "Okunoin": "奥之院", "Okunoin Cemetery": "奥之院", "Kongobu-ji": "金刚峰寺", "Danjo Garan": "坛上伽蓝", "Temple stay": "宿坊体验", "Shukubo": "宿坊",
    "Koyasan": "高野山", "Mount Koya": "高野山", "Kumano Kodo": "熊野古道", "Kumano Hongu Taisha": "熊野本宫大社", "Kumano Nachi Taisha": "熊野那智大社",
    "Nachi Falls": "那智瀑布", "Nachi Waterfall": "那智瀑布", "Kumano Hayatama Taisha": "熊野速玉大社", "Daimonzaka": "大门坂", "Oyunohara": "大斋原",
    "Dorokyo Gorge": "瀞峡", "Dorokyo cruise": "瀞峡游船", "Yunomine Onsen": "汤峰温泉", "Kawayu Onsen": "川汤温泉", "Ryujin Onsen": "龙神温泉",
    "Shirarahama Beach": "白良滨", "Engetsuto": "圆月岛", "Sandanbeki": "三段壁", "Senjojiki": "千叠敷", "Adventure World": "白滨冒险世界",
    "Cave onsen": "洞窟温泉", "IKADA rafting": "北山川筏流", "Kitayama River": "北山川",
    # 伊势志摩
    "Ise Jingu": "伊势神宫", "Ise Grand Shrine": "伊势神宫", "Naiku": "伊势神宫内宫", "Inner Shrine": "伊势神宫内宫", "Geku": "伊势神宫外宫", "Outer Shrine": "伊势神宫外宫",
    "Uji Bridge": "宇治桥", "Okage Yokocho": "托福横丁", "Oharai-machi": "御祓町", "Meoto Iwa": "夫妇岩", "Wedded Rocks": "夫妇岩",
    "Mikimoto Pearl Island": "御木本真珠岛", "Ago Bay": "英虞湾", "Ago Bay cruise": "英虞湾游船", "Ama hut": "海女小屋", "Ama diver hut": "海女小屋",
    "Toba Aquarium": "鸟羽水族馆", "Shimakaze": "观光列车 Shimakaze", "Yokoyama Observatory": "横山展望台", "Matsusaka beef": "松阪牛",
    # 高山 / 白川乡 / 下吕
    "Takayama Old Town": "高山老街", "Sanmachi Suji": "三町筋", "Miyagawa Morning Market": "宫川朝市", "Takayama Jinya": "高山阵屋", "Hida Folk Village": "飞驒之里",
    "Hida beef": "飞驒牛", "Shirakawa-go": "白川乡", "Shirakawago": "白川乡", "Gassho-zukuri": "合掌造民家", "Ogimachi": "荻町", "Shiroyama Viewpoint": "城山展望台",
    "Wada House": "和田家", "Gero Onsen": "下吕温泉", "Gokayama": "五箇山",
    # 中部山岳 / 中山道
    "Tateyama Kurobe Alpine Route": "立山黑部阿尔卑斯路线", "Yuki-no-Otani": "雪之大谷", "Snow Corridor": "雪之大谷", "Kurobe Dam": "黑部水坝", "Murodo": "室堂",
    "Mikurigaike": "御库里池", "Matsumoto Castle": "松本城", "Kamikochi": "上高地", "Kappa Bridge": "河童桥", "Taisho Pond": "大正池",
    "Nakasendo": "中山道", "Nakasendo Trail": "中山道", "Magome": "马笼宿", "Tsumago": "妻笼宿", "Magome-Tsumago": "马笼—妻笼古道", "Narai-juku": "奈良井宿",
    "Kiso Valley": "木曾谷", "Jigokudani Monkey Park": "地狱谷野猿公苑", "Snow monkeys": "雪猴", "Zenko-ji": "善光寺", "Matsumoto City Museum of Art": "松本市美术馆",
    # 名古屋
    "Nagoya Castle": "名古屋城", "Atsuta Jingu": "热田神宫", "Atsuta Shrine": "热田神宫", "Osu Kannon": "大须观音", "Legoland Japan": "日本乐高乐园", "Ghibli Park": "吉卜力公园",
    "Toyota Commemorative Museum": "丰田产业技术纪念馆", "Nagoya meshi": "名古屋美食", "SCMaglev and Railway Park": "磁浮铁道馆",
    # 广岛 / 宫岛
    "Hiroshima Peace Memorial Park": "广岛和平纪念公园", "Peace Memorial Park": "广岛和平纪念公园", "Atomic Bomb Dome": "原爆圆顶", "A-Bomb Dome": "原爆圆顶",
    "Peace Memorial Museum": "广岛和平纪念资料馆", "Hiroshima Castle": "广岛城", "Shukkeien Garden": "缩景园", "Itsukushima Shrine": "严岛神社",
    "Miyajima": "宫岛", "Floating torii": "宫岛大鸟居", "Great Torii": "宫岛大鸟居", "Mount Misen": "弥山", "Miyajima Ropeway": "宫岛缆车", "Okonomiyaki": "广岛烧",
    "Orizuru Tower": "折鹤塔", "Daisho-in": "大圣院",
    # 冈山 / 仓敷 / 濑户内 / 尾道
    "Okayama Korakuen": "冈山后乐园", "Korakuen Garden": "后乐园", "Okayama Castle": "冈山城", "Kurashiki Bikan Historical Quarter": "仓敷美观地区", "Bikan Historical Quarter": "仓敷美观地区",
    "Ohara Museum of Art": "大原美术馆", "Naoshima": "直岛", "Benesse House": "倍乐生之家", "Chichu Art Museum": "地中美术馆", "Yayoi Kusama Pumpkin": "草间弥生南瓜",
    "Art House Project": "家 Project", "Teshima Art Museum": "丰岛美术馆", "Onomichi": "尾道", "Temple Walk": "尾道古寺巡礼", "Senko-ji": "千光寺", "Shimanami Kaido": "岛波海道",
    "Tomonoura": "鞆之浦", "Kibitsu Shrine": "吉备津神社", "Bizen pottery": "备前烧",
    # 四国
    "Matsuyama Castle": "松山城", "Dogo Onsen": "道后温泉", "Dogo Onsen Honkan": "道后温泉本馆", "Ritsurin Garden": "栗林公园", "Kotohira-gu": "金刀比罗宫", "Konpira": "金刀比罗宫",
    "Naruto whirlpools": "鸣门漩涡", "Iya Valley": "祖谷溪", "Kazurabashi": "祖谷葛桥", "Uchiko": "内子", "Shimanami cycling": "岛波海道骑行",
    # 福冈 / 九州
    "Dazaifu Tenmangu": "太宰府天满宫", "Dazaifu Tenmangu Shrine": "太宰府天满宫", "Yatai": "福冈屋台", "Canal City Hakata": "博多运河城", "Ohori Park": "大濠公园",
    "Kushida Shrine": "栉田神社", "Nakasu": "中洲", "Tonkotsu ramen": "豚骨拉面", "Fukuoka Tower": "福冈塔", "Momochi Seaside Park": "百道滨海滨公园",
    "Nagasaki Peace Park": "长崎和平公园", "Nagasaki Atomic Bomb Museum": "长崎原爆资料馆", "Glover Garden": "哥拉巴园", "Dejima": "出岛", "Oura Church": "大浦天主堂",
    "Mount Inasa": "稻佐山", "Gunkanjima": "军舰岛", "Hashima Island": "军舰岛", "Nagasaki Chinatown": "长崎新地中华街", "Megane Bridge": "眼镜桥", "Huis Ten Bosch": "豪斯登堡",
    "Kumamoto Castle": "熊本城", "Suizenji Jojuen Garden": "水前寺成趣园", "Suizenji Park": "水前寺成趣园", "Mount Aso": "阿苏山", "Mt Aso": "阿苏山", "Nakadake Crater": "阿苏中岳火口",
    "Kusasenri": "草千里", "Aso-Kuju National Park": "阿苏九重国立公园", "Kurokawa Onsen": "黑川温泉", "Daikanbo": "大观峰",
    "Takachiho Gorge": "高千穗峡", "Manai Falls": "真名井瀑布", "Takachiho Shrine": "高千穗神社", "Amano Iwato Shrine": "天岩户神社", "Yokagura": "高千穗夜神乐",
    "Beppu Hells": "别府地狱巡游", "Hell Tour": "别府地狱巡游", "Jigoku Meguri": "别府地狱巡游", "Umi Jigoku": "海地狱", "Chinoike Jigoku": "血池地狱", "Yufuin": "由布院", "Kinrin Lake": "金鳞湖",
    "Sengan-en": "仙岩园", "Sengan-en Garden": "仙岩园", "Sakurajima": "樱岛", "Chiran Samurai Residences": "知览武家屋敷", "Ibusuki sand bath": "指宿砂蒸温泉", "Sand bath": "砂蒸温泉",
    "Ibusuki no Tamatebako": "观光列车「指宿之玉手箱」", "Yanagawa river cruise": "柳川游船", "Unzen Jigoku": "云仙地狱", "Unzen Onsen": "云仙温泉", "Arita": "有田烧之乡",
    "Arita porcelain": "有田烧", "Imari": "伊万里", "Karatsu Castle": "唐津城", "Yufuin Floral Village": "由布院花卉村", "Kirishima Shrine": "雾岛神宫",
    # 北海道
    "Odori Park": "大通公园", "Sapporo Clock Tower": "札幌时计台", "Sapporo TV Tower": "札幌电视塔", "Susukino": "薄野", "Mt. Moiwa": "藻岩山", "Mount Moiwa": "藻岩山",
    "Sapporo Beer Museum": "札幌啤酒博物馆", "Hokkaido Shrine": "北海道神宫", "Nijo Market": "二条市场", "Shiroi Koibito Park": "白色恋人公园", "Sapporo Snow Festival": "札幌雪祭",
    "Former Hokkaido Government Office": "北海道厅旧本厅舍", "Moerenuma Park": "莫埃来沼公园", "Miso ramen": "味噌拉面", "Ramen Alley": "拉面横丁",
    "Otaru Canal": "小樽运河", "Sakaimachi Street": "堺町通", "Otaru Music Box Museum": "小樽音乐盒堂", "Noboribetsu Hell Valley": "登别地狱谷", "Jigokudani": "地狱谷",
    "Lake Toya": "洞爷湖", "Showa Shinzan": "昭和新山", "Usuzan Ropeway": "有珠山缆车", "Hakodate Morning Market": "函馆朝市", "Mount Hakodate": "函馆山夜景",
    "Mount Hakodate night view": "函馆山夜景", "Goryokaku": "五棱郭", "Goryokaku Tower": "五棱郭塔", "Motomachi": "函馆元町", "Kanemori Red Brick Warehouses": "金森红砖仓库",
    "Yunokawa Onsen": "汤川温泉", "Furano lavender": "富良野薰衣草田", "Farm Tomita": "富田农场", "Blue Pond": "美瑛青池", "Biei Blue Pond": "美瑛青池", "Patchwork Road": "美瑛拼布之路",
    "Asahiyama Zoo": "旭山动物园", "Sounkyo Gorge": "层云峡", "Ginga and Ryusei Falls": "银河·流星瀑布", "Kurodake Ropeway": "黑岳缆车", "Lake Akan": "阿寒湖", "Marimo": "球藻",
    "Ainu Kotan": "阿伊努村", "Lake Kussharo": "屈斜路湖", "Lake Mashu": "摩周湖", "Mount Io": "硫磺山", "Shiretoko Five Lakes": "知床五湖", "Shiretoko cruise": "知床观光船",
    "Oshinkoshin Falls": "双美瀑布", "Kamuiwakka Falls": "卡姆伊瓦卡温泉瀑布", "Shiretoko Pass": "知床峠", "Rusutsu Resort": "留寿都度假村", "Furano Ski Resort": "富良野滑雪场",
    "Niseko": "二世谷", "Jozankei Onsen": "定山溪温泉", "Sapporo Teine": "手稻滑雪场", "Hokkaido crab": "北海道螃蟹",
    # 东北
    "Zao Onsen": "藏王温泉", "Zao Snow Monsters": "藏王树冰", "Matsushima Bay": "松岛湾", "Zuiganji": "瑞岩寺", "Yamadera": "山寺（立石寺）", "Ginzan Onsen": "银山温泉",
    "Appi Kogen": "安比高原", "Hiraizumi Chusonji": "中尊寺", "Hirosaki Castle": "弘前城", "Nyuto Onsen": "乳头温泉",
    # 通用体验
    "Sumo": "相扑", "Grand Sumo Tournament": "大相扑", "Sake brewery": "酒藏参观", "Cooking class": "料理课", "Onsen": "温泉", "Ryokan": "日式旅馆", "Shinkansen": "新干线",
    "Green Car": "新干线绿色车厢", "Luggage forwarding": "行李托运", "Private taxi": "包车", "Chartered taxi": "包车",
}

TITLE_CN.update({'Historic Towns & Mountain Heritage': '历史小镇与山岳遗产', 'Japan History & Modern Cities': '日本历史与现代都市', 'From Tokyo to Kyushu Journey': '从东京到九州之旅', 'Timeless Traditions: Kanazawa & Hida – Deluxe': '永恒传统：金泽与飞驒（豪华版）', 'Sea of Serenity: Kashikojima – Deluxe': '宁静之海：贤岛（豪华版）', 'Discover Hokkaido: Nature & Scenic Views': '发现北海道：自然与绝景', 'Rusutsu & Hakuba Tsugaike Ski Journey': '留寿都与白马栂池滑雪之旅', 'Sahoro & Furano Ski Journey': '佐幌与富良野滑雪之旅', 'Asahikawa Ski Safari: Pippu, Nayoro Piyashiri & Kamui': '旭川滑雪巡游：比布、名寄 Piyashiri 与神居', 'Rusutsu & Furano Ski with Hokkaido Highlights': '留寿都与富良野滑雪 + 北海道精华', 'Rusutsu Ski with Sapporo & Noboribetsu Onsen': '留寿都滑雪 + 札幌与登别温泉', 'From Sacred Mountains to Coastal Calm: A Journey of Culture, Peace, and Spiritual Reflection': '从圣山到静谧海岸：文化、和平与心灵之旅', 'From Urban Energy to the Soul of Koyasan': '从都市活力到高野山之魂', 'Hidden Cherry Blossom & Ancient Temple of Nara': '奈良秘境樱花与古寺', 'Kyushu Pottery Towns & All of Nagasaki': '九州陶瓷小镇与长崎全览', 'Kyushu Premium Experience: Nature, Heritage & Onsen': '九州尊享体验：自然、遗产与温泉', 'Alpine Routes & Cultural Japan': '阿尔卑斯路线与文化日本', 'Koyasan, Kumano & Shirahama- Wakayama Journey': '高野山、熊野与白滨和歌山之旅', 'Kumano Pilgrimage Paths to Ise': '熊野朝圣之路到伊势', 'Gourmet Rail Journey: Fuji, Ise & Kanazawa': '美食铁道之旅：富士、伊势与金泽', 'Setouchi Garden Isles, Art Shores & Castle Towns': '濑户内庭园岛屿、艺术海岸与城下町', 'Sacred Izumo & Setouchi Sea Paths': '神圣出云与濑户内海路', 'Hakuba Tsugaike & Zao': '白马栂池与藏王（两周滑雪）', 'Shiga Kogen & Zao': '志贺高原与藏王（两周滑雪）', 'Hakuba Tsugaike with Snow Monkeys': '白马栂池滑雪 + 雪猴', 'Shiga Kogen with Snow Monkeys': '志贺高原滑雪 + 雪猴', 'Hakuba Misorano & Zao': '白马 Misorano 与藏王（两周滑雪）', 'Sacred Trails & Hot Springs of the Kii Peninsula': '纪伊半岛圣道与温泉'})
ATTR_CN.update({'Hakuba Tsugaike ski area': '白马栂池滑雪场', 'Hakuba Misorano (Happo-one area) ski': '白马八方尾根滑雪区', 'Futamiura Wedded Rocks (Meoto Iwa)': '二见浦夫妇岩', 'Ise Jingu Geku (Outer Shrine)': '伊势神宫外宫', 'Ise Jingu Naiku (Inner Shrine)': '伊势神宫内宫', 'Coastal viewpoints': '海岸观景点', 'Ryokan stay': '日式旅馆住宿', 'Shimakaze train': '观光特急 Shimakaze', 'Utsukushigahara': '美原高原', 'Wadakin (Matsusaka wagyu)': '和田金（松阪牛）', 'Brick theme park popular with children': '积木主题乐园（名古屋乐高乐园）', 'Inuyama': '犬山', 'Nabana no Sato illumination': '名花之里灯光秀', 'Nagoya Castle and Hommaru Palace': '名古屋城与本丸御殿', 'Osu shopping district': '大须商店街', 'Tokugawa collection (Tokugawa Art Museum)': '德川美术馆', 'Toyota site': '丰田产业技术纪念馆', "New park themed on Japan's iconic animated films": '吉卜力公园', 'Shirakawa-go gassho-zukuri village': '白川乡合掌造村落', 'Takayama': '高山', 'Festival floats exhibition hall': '高山祭屋台会馆', 'Shirakawa-go day trip': '白川乡一日游', 'Takayama Festival': '高山祭', 'Takayama morning markets': '高山朝市', 'Toba': '鸟羽', 'Tomonoura historic port': '鞆之浦历史港町', 'Miyajima / Itsukushima Shrine': '宫岛·严岛神社', 'Hiroshima-style okonomiyaki': '广岛烧', 'Momijidani (Maple Valley)': '红叶谷公园', 'Peace Boulevard': '和平大道', 'Peace Memorial Park and Museum': '广岛和平纪念公园与资料馆', 'Miyajima / Itsukushima floating shrine': '宫岛·严岛神社海上鸟居', 'Onomichi hillside streets': '尾道坡道老街', 'Kamui Ski Links': '神居滑雪场', 'Hachiman-zaka slope': '八幡坂', 'Noboribetsu Onsen': '登别温泉', 'Otaru': '小樽', "Geisha districts (Higashi Chaya etc., per page summary 'geisha districts')": '茶屋街（东茶屋街等）', 'Yuki-no-Otani snow corridor': '雪之大谷', 'Hosshinmon-oji – Kumano Hongu Taisha walk': '发心门王子→熊野本宫大社徒步段', 'Kinosaki Onsen public bathhouses': '城崎温泉外汤', 'Kitayama River IKADA rafting': '北山川筏流', 'Koyasan / Fukuchi-in shukubo': '高野山福智院宿坊', 'Koyasan temple lodging': '高野山宿坊', 'Koyasan temple complex / shukubo': '高野山寺院群·宿坊', 'Fukuchi-in': '福智院（宿坊）', 'Kongobuji': '金刚峰寺', 'Shukubo temple stay': '宿坊体验', 'Kumano Sanzan shrines': '熊野三山', 'Kyoto': '京都', 'Fushimi': '伏见', 'Akame 48 Falls (ninja training)': '赤目四十八瀑（忍者修行）', 'Ise Jingu Inner Shrine (Naiku)': '伊势神宫内宫', 'Ise Jingu Outer Shrine (Geku)': '伊势神宫外宫', 'Kawadoko dining': '川床料理', 'Kyoto gardens': '京都庭园', 'Ryoan-ji rock garden': '龙安寺石庭', 'Sanzen-in (Ohara) moss garden': '大原三千院苔庭', 'Higashiyama slopes': '东山坂道（二年坂·三年坂）', 'Kyoto Station area': '京都站周边', 'Shijo-Kawaramachi': '四条河原町', 'Nachi Falls / Kumano Nachi Taisha': '那智瀑布·熊野那智大社', 'UNESCO World Heritage sites of Nara': '奈良世界遗产群', 'Mount Yoshino': '吉野山', 'Universal City theme park': '日本环球影城', 'Osaka street food': '大阪街头小吃', 'Universal City theme-park area': '环球城乐园区', 'Universal City – Hollywood-themed movie park': '日本环球影城', 'Ebisubashi Bridge': '戎桥', 'Tenjin Matsuri': '天神祭', 'Ishiyama-dera': '石山寺', 'Lake Biwa Michigan cruise': '琵琶湖密歇根号游船', 'Mii-dera': '三井寺', 'Shirahama': '白滨', 'Lake Ashi / Mount Fuji views': '芦之湖·富士山景观', 'Mt. Fuji views': '富士山景观', 'The Fujiya Hotel (Miyanoshita)': '富士屋酒店（宫之下）', 'Hakone Freepass': '箱根周游券', 'Hakone Shrine torii gate': '箱根神社平和鸟居', 'Hakone Sightseeing Cruise (pirate ships)': '芦之湖海贼观光船', 'Hakone museums': '箱根美术馆群', 'Onsen night': '温泉旅馆之夜', 'Asakusa / Senso-ji': '浅草·浅草寺', 'Hotel Chinzanso gardens': '椿山庄庭园', 'Kabuki-za': '歌舞伎座', 'Senso-ji / Asakusa': '浅草寺·浅草', 'Hakone day trip': '箱根一日游', 'Mt Fuji day trip': '富士山一日游', 'Observation decks': '观景台', 'Tsukiji': '筑地', 'Beppu Onsen': '别府温泉', 'Fukuoka yatai street-food stalls': '福冈屋台', 'Solaria Nishitetsu Hotel Fukuoka (or similar) – hotel': '（酒店）Solaria 西铁福冈', 'Yatai street food stalls': '屋台', 'Dazaifu': '太宰府', 'Fukuoka Castle ruins': '福冈城迹', 'Hakata ramen': '博多拉面', 'Nanzoin': '南藏院（卧佛）', 'Yanagawa': '柳川', 'Yatai food stalls': '屋台', 'Yanagawa canal cruise (donko boat)': '柳川川下り游船', 'Naoshima art island': '直岛艺术岛', "Naoshima - Yayoi Kusama 'Red Pumpkin' and contemporary art museums": '直岛草间弥生红南瓜与当代美术馆', 'Matsuyama historic streets': '松山历史街区', 'Zao Onsen ski resort': '藏王温泉滑雪场', 'Inuyama Castle': '犬山城', 'Shimakaze sightseeing limited express': '观光特急 Shimakaze', 'Akame 48 Falls ninja training': '赤目四十八瀑忍者修行', 'Nayoro Piyashiri Ski Area': '名寄 Piyashiri 滑雪场', 'Shinhotaka': '新穗高缆车', 'Omihachiman canal town': '近江八幡水乡', 'Osaka or Nara (free-day option)': '大阪或奈良（自由日可选）', 'Pippu Ski Area': '比布滑雪场', 'Ama hut (pearl-diver hut) lunch': '海女小屋午餐', 'Two theme resorts on the Maihama coastline (Tokyo Bay)': '东京迪士尼度假区（舞滨两园）', 'Tokyo Bay theme-park area (Maihama)': '东京湾乐园区（舞滨）', 'Shiga Kogen ski area': '志贺高原滑雪场', 'Yudanaka Onsen': '汤田中温泉'})

ATTR_CN.update({"Koyasan shukubo": "高野山宿坊", "Sacred Trails & Hot Springs of the Kii Peninsula": "纪伊半岛圣道与温泉"})

TITLE_CN.update({'Nagoya Chita Peninsula: A Luxury Cultural Escape in Central Japan': '名古屋·知多半岛：中部日本奢华文化之旅', "Aomori Unveiled: Culture of Mountain and Sea at Japan's Northern Edge": '青森全览：本州最北端的山海文化', 'Discover Fukuoka: Gateway to Asia, Heart of Japan': '发现福冈：亚洲门户、日本之心', "Eastern Nagano Escape: A Journey into Japan's Serene Highlands and Cultural Elegance": '东信州之旅：静谧高原与雅致文化', 'Nagano Premium Retreat': '长野尊享静养之旅（南信州）', 'Expo 2025 & The Soul of Osaka: A Journey Through Time and Tradition': '2025 世博与大阪之魂：穿越时光与传统', 'Discover Osaka: City Adventures, Skyline Views and Cultural Experiences': '发现大阪：都市探索、天际线与文化体验', 'Premium Tohoku Gourmet Tour: Oma Tuna & Shimokita': '东北尊享美食之旅：大间金枪鱼与下北半岛', 'Explore Sado: A 4-Day Private Tour of Nature, Culture, and History': '探索佐渡：4 天私人自然·文化·历史之旅', 'Tochigi in Four Days: World Heritage, Hot Springs & Cultural Charms': '栃木 4 天：世界遗产、温泉与文化魅力', 'Tokyo & Tohoku Snow Monsters and Hidden Onsen': '东京与东北：树冰与秘汤', 'Slow Travel in Tsugaru - 3 Days, 2 Nights at an Onsen Ryokan Beneath Mt. Iwaki': '津轻慢旅：岩木山下温泉旅馆 3 天 2 晚', 'JNJ-NEBUTA': '青森睡魔祭奥德赛（每日限一组）', 'Sacred Trails & Coastal Traditions': '圣道与海岸传统', 'Hakuba Wadano with Snow Monkeys': '白马和田野滑雪 + 雪猴', 'Tradition, Nature, and the Theme Park Magic': '传统、自然与主题乐园魔法'})
ATTR_CN.update({'Achi Village stargazing tour': '阿智村观星之旅', 'Hirugami Onsen': '昼神温泉', 'Noma Lighthouse': '野间灯塔', 'Osu Shopping Street & Osu Kannon': '大须商店街与大须观音', 'Local farm (farm-to-table)': '本地农场（农场到餐桌）', 'Hirugami Onsen village': '昼神温泉乡', 'Ina Valley': '伊那谷', 'Suwa local shrines (Suwa Taisha implied, not confirmed)': '诹访当地神社（疑为诹访大社）', 'Komagatake Ropeway & Senjojiki Cirque': '驹岳缆车与千叠敷冰斗', 'Shimoguri village': '下栗之里', 'Snowshoeing in the Central Alps': '中央阿尔卑斯雪鞋徒步', 'Soba-making and local wine & sake tasting': '荞麦面制作与本地葡萄酒·清酒品鉴', 'Takato Castle Ruins Park': '高远城址公园', 'Tenryu River cruise (Tenryukyo Gorge)': '天龙峡游船', 'Traditional festivals of the Ina Valley': '伊那谷传统祭典', 'Karuizawa': '轻井泽', 'Kiso-Fukushima post town': '木曾福岛宿场', 'Senjojiki Cirque / Komagatake Ropeway': '千叠敷冰斗·驹岳缆车', 'Karuizawa Prince Hotel Ski Resort': '轻井泽王子大饭店滑雪场', 'Karuizawa Prince Shopping Plaza': '轻井泽王子购物广场', 'Karuizawa bakeries, cafes & Shinshu cuisine': '轻井泽面包房、咖啡馆与信州料理', 'Komoro Castle Ruins (Kaikoen Park)': '小诸城址怀古园', 'Kumoba Pond (Swan Lake)': '云场池', 'Shiraito Falls': '白丝瀑布', 'Tobira Onsen Myojinkan': '扉温泉 明神馆', 'Fukashi Shrine': '深志神社', 'Matsumoto Castle festivals': '松本城祭典', 'Nakamachi Street': '中町通', 'Tobira Onsen': '扉温泉', 'Komagatake Ropeway': '驹岳缆车', 'Senjojiki Cirque (Central Alps)': '千叠敷冰斗（中央阿尔卑斯）', 'Anrakuji Temple': '安乐寺（八角三重塔）', 'Bessho Onsen': '别所温泉', 'Fruit picking in Nagano': '长野采果体验', 'Hakuba': '白马', 'Kanbayashi Onsen': '上林温泉', 'Kitamuki Kannon': '北向观音', 'Madarao Kogen Ski Resort': '斑尾高原滑雪场', 'Matsushiro Castle Ruins / Matsushiro samurai district': '松代城址与松代武家屋敷', 'Nagano Olympics sites': '长野冬奥场馆', 'Nagano Shinkansen (Hokuriku Shinkansen) travel': '北陆新干线（长野）', 'Nagano local dishes & specialties': '长野乡土料理', 'Nagano shopping spots': '长野购物', 'Nozawa Onsen': '野泽温泉', 'Shibu Onsen': '涩温泉', 'Shiga Kogen Ski Resort': '志贺高原滑雪场', 'Shirahone Onsen': '白骨温泉', 'Soba-making experience': '荞麦面制作体验', "Togakushi Ninja Village / Kids' Ninja Village": '户隐忍者村', 'Togakushi Shrine': '户隐神社', 'Higashiyama Botanical Garden': '东山动植物园', 'Miwa Shrine': '三轮神社（知多）', 'Nagoya Castle / Honmaru Palace': '名古屋城·本丸御殿', 'Magome-juku': '马笼宿', 'Tsumago-juku': '妻笼宿', 'Tsumago–Magome walk': '妻笼—马笼古道徒步', 'Onogame & Futatsugame': '大野龟与二龟', 'Sado Island': '佐渡岛', 'Futatsugame': '二龟', 'Japanese Crested Ibis (toki) viewing': '朱鹮观察', 'Ogi Port': '小木港（盆舟）', 'Onogame': '大野龟', 'Ryotsu Port': '两津港', 'Sado Gold Mine': '佐渡金山', 'Sado Island cultural landmarks': '佐渡文化地标', 'Lake Suwa': '诹访湖', 'Suwa Five Sake Brewery Tour': '诹访五藏酒藏巡游', 'Katakurakan': '片仓馆', 'Suwa Gokura sake breweries': '诹访五藏', 'Suwa Taisha': '诹访大社', 'Takashima Castle': '高岛城', 'Tateishi Park': '立石公园', 'Yokoya Gorge': '横谷溪谷', 'Tokoname pottery walk': '常滑陶瓷散步道', 'Flight of Dreams': 'Flight of Dreams（中部机场波音展馆）', 'Maruyama Park': '圆山公园', 'Expo 2025 Yumeshima': '2025 大阪世博（梦洲）', 'Nagai Botanical Garden (teamLab)': '长居植物园 teamLab', 'Toyokuni Shrine': '丰国神社', 'De Sakai blacksmith experience': '堺打刃物锻造体验', 'Expo 2025 Osaka kid-friendly activities': '大阪世博亲子活动', 'Hozenji Yokocho': '法善寺横丁', 'Maruichi Kashiho wagashi workshop': '丸一菓子舗和菓子工坊', 'Mozu kofun burial mounds (Sakai)': '百舌鸟古坟群（堺）', 'Nagai Botanical Garden – teamLab': '长居植物园 teamLab', 'Nishikinohama Beach Park': '二色之滨公园', 'Osaka transport guide': '大阪交通指南', 'Sakai Plaza of Rikyu and Akiko (tea ceremony)': '堺利晶之杜（茶道体验）', 'Sumiyoshi Taisha Shrine': '住吉大社', 'Tempozan Ferris Wheel': '天保山大摩天轮', 'Tsutenkaku Tower (Shinsekai)': '通天阁（新世界）', 'Maruichi Kashiho': '丸一菓子舗', 'Mozu Kofun (balloon flight)': '百舌鸟古坟群热气球', 'Mozu kofun tombs (balloon flight)': '百舌鸟古坟群热气球', 'Ryurei-style tea room': '立礼式茶室', 'Sakai blacksmith workshop': '堺刃物锻造工坊', 'Sakai knife blacksmith workshop': '堺打刃物工坊', 'Asuka Village – Ishibutai Tumulus': '飞鸟村石舞台古坟', 'Chikurin-in Temple (Gunpoen garden)': '竹林院群芳园', 'Mount Yoshinoyama (Senbonzakura)': '吉野山千本樱', 'Yoshino Mikumari Shrine & Hanayagura Observatory': '吉野水分神社与花矢仓展望台', 'Engakuji Temple': '圆觉寺', 'Hasedera Temple': '长谷寺（镰仓）', 'Hokokuji Temple (Bamboo Temple)': '报国寺（竹寺）', 'Komachi-dori Street': '小町通', 'Kamakura day trip from Tokyo': '东京出发镰仓一日游', 'Meguro River cherry blossoms': '目黑川樱花', 'Hakata Old Town': '博多旧市街', 'Shikanoshima Island': '志贺岛', 'Shikaumi Shrine': '志贺海神社', 'Tochoji Temple': '东长寺（福冈大佛）', 'Fukuoka City shopping': '福冈市购物', 'Fukutsu seaside town (seasonal flowers)': '福津海滨小镇（季节花田）', "Itoshima artists' studios & seaside galleries": '糸岛艺术家工作室与海滨画廊', 'Sakurai Futamigaura (Meoto Iwa)': '樱井二见浦夫妇岩', 'Kurume Kasuri craft studio': '久留米絣工坊', 'Kurume Kasuri studio': '久留米絣工坊', 'Local sake brewery': '本地酒藏', 'Munakata Taisha': '宗像大社', 'Munakata museum (Kaino-michi)': '宗像·海之道博物馆', 'Beppu Jigoku Meguri (Hells of Beppu)': '别府地狱巡游', 'Jigoku-mushi (hell-steamed cuisine)': '地狱蒸料理', 'Toriten (chicken tempura)': '炸鸡天妇罗（大分名物）', 'Yunotsubo Kaido (Yufuin)': '汤之坪街道（由布院）', 'Ukiha fruit farms': '浮羽水果农园', 'Ukiha white-walled streets': '浮羽白壁街道', 'Ukihane Inari Shrine': '浮羽稻荷神社', 'Aomori Nebuta Festival': '青森睡魔祭', 'Hakkoda / Mt. Tamoyachidake snow monsters (juhyo)': '八甲田树冰', 'Mount Hakkoda': '八甲田山', 'Nebuta Museum Wa Rasse': '睡魔之家 WA RASSE', 'Nebuta workshop (dance & music)': '睡魔祭舞蹈·音乐工作坊', 'Sukayu Onsen': '酸汤温泉（千人风吕）', 'A-Factory': 'A-Factory（青森苹果西打工坊）', 'Aomori autumn foliage (koyo) spots': '青森红叶名所', 'Aomori beaches': '青森海滩', 'Aomori local food (5 must-try dishes)': '青森乡土美食', 'Asamushi Onsen': '浅虫温泉', 'Furukawa Fish Market': '古川市场（海鲜丼）', 'Hakkoda Mountains': '八甲田山', 'Hakkoda Mountains year-round guide': '八甲田四季', 'Hirosaki Castle / Hirosaki Park': '弘前城·弘前公园', 'Inakadate Rice Paddy Art': '田舍馆村稻田艺术', 'Jomon Prehistoric Sites (UNESCO)': '绳文遗迹群（世界遗产·三内丸山）', 'Kabushima Shrine': '蕪岛神社', 'Koganezaki Furofushi Onsen': '黄金崎不老不死温泉', 'Lake Towada': '十和田湖', 'Lake Towada cruises & scenic trails': '十和田湖游船与步道', 'Lamp no Yado Aoni Onsen (Lamp Inn)': '青荷温泉（灯之宿）', 'Oirase Gorge / Oirase Stream': '奥入濑溪流', 'Oku-Yagen Onsen (Kappa-no-Yu)': '奥药研温泉（河童之汤）', 'Owani Onsen': '大鳄温泉', 'Takayama Inari Shrine': '高山稻荷神社（青森）', 'Yagen Onsen': '药研温泉', 'Yagen Valley': '药研溪流', 'Aomori City cafes, galleries, craft shops': '青森市咖啡馆·画廊·工艺店', 'Aomori City': '青森市', 'Nebuta culture (workshop)': '睡魔祭文化工作坊', 'Hachinohe': '八户', 'Hachinohe morning market': '八户馆鼻岸壁朝市', 'Kabushima Island': '蕪岛', 'Tanesashi Coast': '种差海岸', 'Mount Hakkoda primeval beech forest': '八甲田山毛榉原生林', 'Oirase (gorge/stream area)': '奥入濑溪流', 'Motsuji Hondo, Cultural Assets Repository & Kaizando': '毛越寺本堂·宝物馆·开山堂', 'Motsuji Temple': '毛越寺', 'Oizumi-ga-ike Pond (Motsuji Pure Land Garden)': '毛越寺净土庭园大泉池', 'Hirosaki Apple Park': '弘前苹果公园', 'Hirosaki Castle Botanical Garden': '弘前城植物园', 'Hirosaki Castle Snow Lantern Festival': '弘前城雪灯笼祭', 'Hirosaki Castle keep exhibits': '弘前城天守展示', 'Hirosaki Neputa Festival': '弘前睡魔祭', 'Kimori Cider Factory': 'Kimori 苹果酒工坊', 'Shirakami-Sanchi': '白神山地', 'Mt. Iwaki': '岩木山', 'Aoni Onsen (Lamp Inn)': '青荷温泉（灯之宿）', 'Mount Osore (Osorezan)': '恐山', 'Shimokita Peninsula': '下北半岛', 'Fugen-in temple lodging': '普贤院宿坊', 'Oma fishing port (tuna line fishing)': '大间渔港（金枪鱼一本钓）', 'Akiu Winery': '秋保酒庄', 'Akiu wineries (Akiu Winery)': '秋保酒庄', 'Sendai City': '仙台市', 'Shozan restaurant': 'Shozan 餐厅（仙台）', 'Aoba Castle (Sendai Castle) ruins': '青叶城（仙台城）址', 'Aoba Castle Museum and Exhibition Hall': '青叶城资料展示馆', 'Shimokita fishing villages': '下北渔村', 'Oma (tuna fishing port)': '大间（金枪鱼渔港）', 'Hotokegaura cliffs': '仏之浦奇岩', 'Oma Town & harbour': '大间町与港口', 'Oma Tuna Fishing Experience': '大间金枪鱼垂钓体验', 'Oma Tuna Monument (Cape Oma)': '大间崎金枪鱼纪念碑', 'Oma tuna (bluefin) dining': '大间蓝鳍金枪鱼料理', 'Taijima Island': '弁天岛（大间崎）', 'Oirase Gorge': '奥入濑溪流', 'Fujimi Panorama Resort': '富士见全景度假村（缆车）', 'Fukutsu': '福津', 'Sumo demonstration, Izumisano': '泉佐野相扑表演', 'Sumo experience': '相扑体验', 'Ebisenbei no Sato': '虾仙贝之里', 'Misawa': '三泽', 'Farm Aichi': 'Farm Aichi 农场', 'Ghibli Park - Mononoke no Sato': '吉卜力公园·魔法公主之里', 'Higashiyama Botanical Garden (teahouse) or Farm Aichi': '东山植物园茶室或 Farm Aichi', 'Japanese Crested Ibis (toki) observation': '朱鹮观察', 'Local morning market': '本地早市', 'Hotokegaura': '仏之浦', 'Southwest Sado coast': '佐渡西南海岸', "Expo '70 Commemorative Park": '万博纪念公园（太阳之塔）'})

ATTR_CN.update({'Hakuba Wadano ski area': '白马和田野滑雪场', 'Animation-world park at Ai-Chikyuhaku Kinen Koen': '吉卜力公园（爱·地球博纪念公园）', 'Animation-themed park at Ai-Chikyuhaku Kinen Koen (Expo 2005 Commemorative Park)': '吉卜力公园（爱·地球博纪念公园）', 'Brick-toy theme park at Nagoya Port': '名古屋乐高乐园（名古屋港）', 'Brick-toy theme park, Nagoya Port': '名古屋乐高乐园（名古屋港）', 'Noritake Forest': '则武之森', 'Tsugaike Kogen ski area (Hakuba)': '栂池高原滑雪场（白马）', 'Shirakawa-go gassho villages': '白川乡合掌村', 'Hida no Sato': '飞驒之里', 'Hida-Takayama old town': '飞驒高山老街', 'Sanmachi Street (Old Town)': '三町筋老街', 'Shirakawa-go Observatory (Ogimachi Castle viewpoint)': '荻町城迹展望台', 'Ama hut seafood lunch': '海女小屋海鲜午餐', 'Hiroshima city (by streetcar)': '广岛市区（路面电车）', 'Izumo Taisha (implied by title; not named in summary)': '出云大社（据标题推断）', 'Kurashiki Bikan historic quarter (implied by stay; not named in summary)': '仓敷美观地区（据住宿推断）', 'Tamatsukuri Onsen': '玉造温泉', 'Kurashiki': '仓敷', 'Setouchi Islands': '濑户内诸岛', 'Onomichi hillside streets and temples': '尾道坡道与寺庙', 'Onomichi retro buildings': '尾道复古建筑', 'Onomichi sloping streets': '尾道坡道', 'Onomichi temples': '尾道寺庙', 'Ikuchijima Island': '生口岛', 'Shiomachi Shopping Street': '濑户田汐町商店街', 'Noboribetsu Jigokudani (Hell Valley)': '登别地狱谷', 'Rusutsu Resort ski area': '留寿都度假村滑雪场', "Amanohashidate sandbar (3.6 km pine-lined path, one of Japan's Three Great Views)": '天桥立（日本三景）', 'Takami-no-Sato': '高见之乡（枝垂樱）', 'Samurai residences and Japanese gardens near Himeji Castle': '姬路城旁武家屋敷与庭园（好古园）', 'Kinosaki Onsen bathhouses': '城崎温泉外汤', 'Kondo Hall': '金堂（坛上伽蓝）', 'Konpon Daito Pagoda': '根本大塔', 'Koyasan sacred grounds': '高野山圣域', 'Shinsaibashi': '心斋桥', 'Old Tokaido Highway Cedar Avenue': '旧东海道杉并木', 'Togendai': '桃源台', 'Second Maihama park': '东京迪士尼海洋（舞滨第二园区）', 'Tokyo Bay theme resort - castle park (classic rides, parades)': '东京迪士尼乐园（城堡园区）', 'Tokyo Bay theme resort - sea-themed park': '东京迪士尼海洋', "Tokyo Disneyland / Tokyo DisneySea (page wording: 'Tokyo Bay theme resorts', 'a castle with classic rides and parades', 'a sea-themed park')": '东京迪士尼乐园 / 迪士尼海洋', 'Tokyo historic streets & shopping areas': '东京老街与购物区', 'Tokyo historic streets and shopping areas': '东京老街与购物区', 'Asakusa / Kaminarimon Gate / Sensoji Temple': '浅草·雷门·浅草寺', 'Asakusa / Sensoji': '浅草·浅草寺', 'Asakusa / Sensoji Temple / Kaminarimon': '浅草·浅草寺·雷门', 'Kamakura (option)': '镰仓（可选）', 'Kaminarimon Gate': '雷门', 'Nikko (option)': '日光（可选）', 'Senso-ji Temple / Nakamise': '浅草寺·仲见世', 'Tokyo Station area': '东京站周边', 'Tokyo Bay theme resort (two Maihama parks)': '东京迪士尼度假区（舞滨两园）', 'Arita pottery town': '有田陶瓷小镇', 'Hita': '日田', 'Ibusuki Onsen': '指宿温泉', 'Imari pottery town': '伊万里陶瓷小镇', 'Kagoshima': '鹿儿岛', 'Gunkanjima (Battleship Island) landing cruise': '军舰岛登岛游船', 'Yanagawa canal river cruise': '柳川川下り游船', 'Yanagawa canals': '柳川水道', 'Setouchi art islands': '濑户内艺术岛', 'Uchiko historic town': '内子历史小镇', 'Bihoro Pass': '美幌峠', 'Hasami pottery town': '波佐见陶瓷小镇', 'Tango Ao-Matsu sightseeing train': '丹后青松号观光列车', 'Iyo-Ozu': '伊予大洲', 'Ikuchijima Island / Shiomachi Shopping Street': '生口岛·汐町商店街'})
