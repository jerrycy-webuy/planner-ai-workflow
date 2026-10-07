# -*- coding: utf-8 -*-
"""城市 / 区域对照表（EN -> 中文, 区域）。供 consolidate.py 使用。"""

# city_en(lower, 去掉连字符/空格后的 key) -> (中文, 区域EN, 区域中文)
CITY = {
    # Kanto 关东
    "tokyo": ("东京", "Kanto", "关东"), "hakone": ("箱根", "Kanto", "关东"),
    "kamakura": ("镰仓", "Kanto", "关东"), "nikko": ("日光", "Kanto", "关东"),
    "yokohama": ("横滨", "Kanto", "关东"), "narita": ("成田", "Kanto", "关东"),
    "haneda": ("羽田", "Kanto", "关东"), "maihama": ("舞滨", "Kanto", "关东"),
    "tokyobay": ("东京湾", "Kanto", "关东"), "odawara": ("小田原", "Kanto", "关东"),
    "atami": ("热海", "Kanto", "关东"), "izu": ("伊豆", "Kanto", "关东"),
    "kawaguchiko": ("河口湖", "Chubu", "中部"), "fujikawaguchiko": ("富士河口湖", "Chubu", "中部"),
    "mtfuji": ("富士山", "Chubu", "中部"), "mountfuji": ("富士山", "Chubu", "中部"), "fuji": ("富士山", "Chubu", "中部"),
    "gotemba": ("御殿场", "Chubu", "中部"), "fujiyoshida": ("富士吉田", "Chubu", "中部"),
    # Chubu / Tokai 中部・东海
    "nagoya": ("名古屋", "Chubu", "中部"), "ise": ("伊势", "Chubu", "中部"), "iseshima": ("伊势志摩", "Chubu", "中部"),
    "toba": ("鸟羽", "Chubu", "中部"), "kashikojima": ("贤岛", "Chubu", "中部"), "shima": ("志摩", "Chubu", "中部"),
    "matsusaka": ("松阪", "Chubu", "中部"), "iga": ("伊贺", "Kansai", "关西"), "igaueno": ("伊贺上野", "Kansai", "关西"),
    "futami": ("二见", "Chubu", "中部"), "agobay": ("英虞湾", "Chubu", "中部"),
    "takayama": ("高山", "Chubu", "中部"), "hidatakayama": ("飞驒高山", "Chubu", "中部"),
    "shirakawago": ("白川乡", "Chubu", "中部"), "shirakawa": ("白川乡", "Chubu", "中部"),
    "gero": ("下吕温泉", "Chubu", "中部"), "geroonsen": ("下吕温泉", "Chubu", "中部"),
    "matsumoto": ("松本", "Chubu", "中部"), "kamikochi": ("上高地", "Chubu", "中部"),
    "nagano": ("长野", "Chubu", "中部"), "hakuba": ("白马", "Chubu", "中部"),
    "shigakogen": ("志贺高原", "Chubu", "中部"), "yudanaka": ("汤田中温泉", "Chubu", "中部"),
    "nozawaonsen": ("野泽温泉", "Chubu", "中部"), "nozawa": ("野泽温泉", "Chubu", "中部"),
    "magome": ("马笼宿", "Chubu", "中部"), "tsumago": ("妻笼宿", "Chubu", "中部"),
    "nakatsugawa": ("中津川", "Chubu", "中部"), "kiso": ("木曾", "Chubu", "中部"), "kisofukushima": ("木曾福岛", "Chubu", "中部"),
    "narai": ("奈良井宿", "Chubu", "中部"), "nakasendo": ("中山道", "Chubu", "中部"),
    "tateyama": ("立山", "Hokuriku", "北陆"), "murodo": ("室堂", "Hokuriku", "北陆"),
    "toyama": ("富山", "Hokuriku", "北陆"), "kanazawa": ("金泽", "Hokuriku", "北陆"),
    "tsuruga": ("敦贺", "Hokuriku", "北陆"), "fukui": ("福井", "Hokuriku", "北陆"),
    "kaga": ("加贺温泉", "Hokuriku", "北陆"), "kagaonsen": ("加贺温泉", "Hokuriku", "北陆"),
    "wakura": ("和仓温泉", "Hokuriku", "北陆"), "shizuoka": ("静冈", "Chubu", "中部"),
    # Kansai 关西
    "kyoto": ("京都", "Kansai", "关西"), "nara": ("奈良", "Kansai", "关西"), "osaka": ("大阪", "Kansai", "关西"),
    "kobe": ("神户", "Kansai", "关西"), "himeji": ("姬路", "Kansai", "关西"), "arima": ("有马温泉", "Kansai", "关西"),
    "koyasan": ("高野山", "Kansai", "关西"), "mountkoya": ("高野山", "Kansai", "关西"), "mtkoya": ("高野山", "Kansai", "关西"),
    "wakayama": ("和歌山", "Kansai", "关西"), "shirahama": ("白滨", "Kansai", "关西"),
    "kumano": ("熊野", "Kansai", "关西"), "kumanokodo": ("熊野古道", "Kansai", "关西"),
    "nachikatsuura": ("那智胜浦", "Kansai", "关西"), "katsuura": ("那智胜浦", "Kansai", "关西"), "kiikatsuura": ("纪伊胜浦", "Kansai", "关西"),
    "kawayu": ("川汤温泉", "Kansai", "关西"), "kawayuonsen": ("川汤温泉", "Kansai", "关西"),
    "hongu": ("熊野本宫", "Kansai", "关西"), "tanabe": ("田边", "Kansai", "关西"), "kiitanabe": ("纪伊田边", "Kansai", "关西"),
    "yunomine": ("汤峰温泉", "Kansai", "关西"), "yunomineonsen": ("汤峰温泉", "Kansai", "关西"),
    "ryujin": ("龙神温泉", "Kansai", "关西"), "ryujinonsen": ("龙神温泉", "Kansai", "关西"),
    "shingu": ("新宫", "Kansai", "关西"), "dorokyo": ("瀞峡", "Kansai", "关西"), "kitayama": ("北山村", "Kansai", "关西"),
    "kinosaki": ("城崎温泉", "Kansai", "关西"), "kinosakionsen": ("城崎温泉", "Kansai", "关西"),
    "hikone": ("彦根", "Kansai", "关西"), "lakebiwa": ("琵琶湖", "Kansai", "关西"), "otsu": ("大津", "Kansai", "关西"),
    "ohara": ("大原", "Kansai", "关西"), "uji": ("宇治", "Kansai", "关西"), "arashiyama": ("岚山", "Kansai", "关西"),
    "universalcity": ("环球城", "Kansai", "关西"), "amanohashidate": ("天桥立", "Kansai", "关西"),
    "ine": ("伊根", "Kansai", "关西"), "kansai": ("关西", "Kansai", "关西"),
    # Chugoku 中国地方
    "okayama": ("冈山", "Chugoku", "中国地方"), "kurashiki": ("仓敷", "Chugoku", "中国地方"),
    "naoshima": ("直岛", "Setouchi", "濑户内"), "teshima": ("丰岛", "Setouchi", "濑户内"), "inujima": ("犬岛", "Setouchi", "濑户内"),
    "shodoshima": ("小豆岛", "Setouchi", "濑户内"), "setouchi": ("濑户内", "Setouchi", "濑户内"), "setoinlandsea": ("濑户内海", "Setouchi", "濑户内"),
    "onomichi": ("尾道", "Chugoku", "中国地方"), "tomonoura": ("鞆之浦", "Chugoku", "中国地方"), "fukuyama": ("福山", "Chugoku", "中国地方"),
    "hiroshima": ("广岛", "Chugoku", "中国地方"), "miyajima": ("宫岛", "Chugoku", "中国地方"),
    "iwakuni": ("岩国", "Chugoku", "中国地方"), "shimonoseki": ("下关", "Chugoku", "中国地方"),
    "matsue": ("松江", "Chugoku", "中国地方"), "izumo": ("出云", "Chugoku", "中国地方"), "tottori": ("鸟取", "Chugoku", "中国地方"),
    "imabari": ("今治", "Shikoku", "四国"), "shimanami": ("岛波海道", "Setouchi", "濑户内"),
    # Shikoku 四国
    "takamatsu": ("高松", "Shikoku", "四国"), "matsuyama": ("松山", "Shikoku", "四国"),
    "dogo": ("道后温泉", "Shikoku", "四国"), "dogoonsen": ("道后温泉", "Shikoku", "四国"),
    "kotohira": ("琴平", "Shikoku", "四国"), "tokushima": ("德岛", "Shikoku", "四国"), "naruto": ("鸣门", "Shikoku", "四国"),
    "kochi": ("高知", "Shikoku", "四国"), "iya": ("祖谷", "Shikoku", "四国"), "uchiko": ("内子", "Shikoku", "四国"),
    # Kyushu 九州
    "fukuoka": ("福冈", "Kyushu", "九州"), "hakata": ("博多", "Kyushu", "九州"), "dazaifu": ("太宰府", "Kyushu", "九州"),
    "nagasaki": ("长崎", "Kyushu", "九州"), "unzen": ("云仙温泉", "Kyushu", "九州"), "shimabara": ("岛原", "Kyushu", "九州"),
    "kumamoto": ("熊本", "Kyushu", "九州"), "aso": ("阿苏", "Kyushu", "九州"), "mtaso": ("阿苏山", "Kyushu", "九州"),
    "kurokawa": ("黑川温泉", "Kyushu", "九州"), "kurokawaonsen": ("黑川温泉", "Kyushu", "九州"),
    "takachiho": ("高千穗", "Kyushu", "九州"), "beppu": ("别府", "Kyushu", "九州"), "yufuin": ("由布院", "Kyushu", "九州"),
    "kagoshima": ("鹿儿岛", "Kyushu", "九州"), "ibusuki": ("指宿", "Kyushu", "九州"), "chiran": ("知览", "Kyushu", "九州"),
    "sakurajima": ("樱岛", "Kyushu", "九州"), "yanagawa": ("柳川", "Kyushu", "九州"),
    "arita": ("有田", "Kyushu", "九州"), "imari": ("伊万里", "Kyushu", "九州"), "karatsu": ("唐津", "Kyushu", "九州"),
    "saga": ("佐贺", "Kyushu", "九州"), "ureshino": ("嬉野温泉", "Kyushu", "九州"), "takeo": ("武雄温泉", "Kyushu", "九州"),
    "kitakyushu": ("北九州", "Kyushu", "九州"), "mojiko": ("门司港", "Kyushu", "九州"), "miyazaki": ("宫崎", "Kyushu", "九州"),
    "kirishima": ("雾岛", "Kyushu", "九州"), "huistenbosch": ("豪斯登堡", "Kyushu", "九州"), "sasebo": ("佐世保", "Kyushu", "九州"),
    # Hokkaido 北海道
    "sapporo": ("札幌", "Hokkaido", "北海道"), "otaru": ("小樽", "Hokkaido", "北海道"),
    "noboribetsu": ("登别温泉", "Hokkaido", "北海道"), "laketoya": ("洞爷湖", "Hokkaido", "北海道"), "toya": ("洞爷湖", "Hokkaido", "北海道"),
    "hakodate": ("函馆", "Hokkaido", "北海道"), "furano": ("富良野", "Hokkaido", "北海道"), "biei": ("美瑛", "Hokkaido", "北海道"),
    "asahikawa": ("旭川", "Hokkaido", "北海道"), "sounkyo": ("层云峡", "Hokkaido", "北海道"),
    "lakeakan": ("阿寒湖", "Hokkaido", "北海道"), "akan": ("阿寒湖", "Hokkaido", "北海道"),
    "lakekussharo": ("屈斜路湖", "Hokkaido", "北海道"), "kussharo": ("屈斜路湖", "Hokkaido", "北海道"),
    "lakemashu": ("摩周湖", "Hokkaido", "北海道"), "mashu": ("摩周湖", "Hokkaido", "北海道"),
    "shiretoko": ("知床", "Hokkaido", "北海道"), "utoro": ("宇登吕", "Hokkaido", "北海道"), "abashiri": ("网走", "Hokkaido", "北海道"),
    "rusutsu": ("留寿都", "Hokkaido", "北海道"), "niseko": ("二世谷", "Hokkaido", "北海道"), "jozankei": ("定山溪温泉", "Hokkaido", "北海道"),
    "sahoro": ("佐幌", "Hokkaido", "北海道"), "kushiro": ("钏路", "Hokkaido", "北海道"), "kawayuonsenhokkaido": ("川汤温泉(北海道)", "Hokkaido", "北海道"),
    "newchitose": ("新千岁", "Hokkaido", "北海道"), "chitose": ("千岁", "Hokkaido", "北海道"), "tomamu": ("星野度假村 Tomamu", "Hokkaido", "北海道"),
    "kiroro": ("Kiroro", "Hokkaido", "北海道"), "obihiro": ("带广", "Hokkaido", "北海道"),
    # Tohoku 东北
    "sendai": ("仙台", "Tohoku", "东北"), "matsushima": ("松岛", "Tohoku", "东北"), "zao": ("藏王温泉", "Tohoku", "东北"), "zaoonsen": ("藏王温泉", "Tohoku", "东北"),
    "appi": ("安比高原", "Tohoku", "东北"), "appikogen": ("安比高原", "Tohoku", "东北"), "hiraizumi": ("平泉", "Tohoku", "东北"),
    "aomori": ("青森", "Tohoku", "东北"), "hirosaki": ("弘前", "Tohoku", "东北"), "akita": ("秋田", "Tohoku", "东北"),
    "yamadera": ("山寺", "Tohoku", "东北"), "ginzan": ("银山温泉", "Tohoku", "东北"), "ginzanonsen": ("银山温泉", "Tohoku", "东北"),
    "morioka": ("盛冈", "Tohoku", "东北"), "nyuto": ("乳头温泉", "Tohoku", "东北"),
    # Okinawa 冲绳
    "okinawa": ("冲绳", "Okinawa", "冲绳"), "naha": ("那霸", "Okinawa", "冲绳"),
}

CITY.update({
    "inuyama": ("犬山", "Chubu", "中部"), "nabari": ("名张", "Kansai", "关西"), "nayoro": ("名寄", "Hokkaido", "北海道"),
    "okuhida": ("奥飞驒温泉乡", "Chubu", "中部"), "omihachiman": ("近江八幡", "Kansai", "关西"), "pippu": ("比布", "Hokkaido", "北海道"),
    "teshikaga": ("弟子屈", "Hokkaido", "北海道"), "toyako": ("洞爷湖", "Hokkaido", "北海道"), "urayasu": ("浦安", "Kanto", "关东"),
    "yamanouchi": ("山之内（汤田中/涩温泉）", "Chubu", "中部"), "hita": ("日田", "Kyushu", "九州"), "shinhotaka": ("新穗高", "Chubu", "中部"),
    "utsukushigahara": ("美原高原", "Chubu", "中部"), "futamiura": ("二见浦", "Chubu", "中部"), "hommaru": ("本丸", "Chubu", "中部"),
    "ureshino": ("嬉野温泉", "Kyushu", "九州"), "huistenbosch": ("豪斯登堡", "Kyushu", "九州"), "izumo": ("出云", "Chugoku", "中国地方"),
    "tsugaike": ("栂池", "Chubu", "中部"), "misorano": ("白马 Misorano", "Chubu", "中部"), "happoone": ("八方尾根", "Chubu", "中部"),
})

CITY.update({
    # 东北（Japan Navi Journey 主力区域）
    "aomori": ("青森", "Tohoku", "东北"), "hirosaki": ("弘前", "Tohoku", "东北"), "hachinohe": ("八户", "Tohoku", "东北"), "towada": ("十和田", "Tohoku", "东北"),
    "laketowada": ("十和田湖", "Tohoku", "东北"), "oirase": ("奥入濑溪流", "Tohoku", "东北"), "tsugaru": ("津轻", "Tohoku", "东北"), "mutsu": ("陆奥", "Tohoku", "东北"),
    "shimokita": ("下北半岛", "Tohoku", "东北"), "oma": ("大间", "Tohoku", "东北"), "osorezan": ("恐山", "Tohoku", "东北"), "shirakami": ("白神山地", "Tohoku", "东北"),
    "shirakamisanchi": ("白神山地", "Tohoku", "东北"), "sukayu": ("酸汤温泉", "Tohoku", "东北"), "hakkoda": ("八甲田", "Tohoku", "东北"), "aoni": ("青荷温泉", "Tohoku", "东北"),
    "goshogawara": ("五所川原", "Tohoku", "东北"), "kuroishi": ("黑石", "Tohoku", "东北"), "ajigasawa": ("鯵泽", "Tohoku", "东北"), "owani": ("大鳄温泉", "Tohoku", "东北"),
    "sendai": ("仙台", "Tohoku", "东北"), "matsushima": ("松岛", "Tohoku", "东北"), "akiu": ("秋保温泉", "Tohoku", "东北"), "naruko": ("鸣子温泉", "Tohoku", "东北"),
    "ishinomaki": ("石卷", "Tohoku", "东北"), "kesennuma": ("气仙沼", "Tohoku", "东北"), "shiogama": ("盐釜", "Tohoku", "东北"), "zao": ("藏王", "Tohoku", "东北"),
    "yamagata": ("山形", "Tohoku", "东北"), "yonezawa": ("米泽", "Tohoku", "东北"), "sakata": ("酒田", "Tohoku", "东北"), "tsuruoka": ("鹤冈", "Tohoku", "东北"),
    "dewasanzan": ("出羽三山", "Tohoku", "东北"), "hiraizumi": ("平泉", "Tohoku", "东北"), "morioka": ("盛冈", "Tohoku", "东北"), "hanamaki": ("花卷温泉", "Tohoku", "东北"),
    "kakunodate": ("角馆", "Tohoku", "东北"), "laketazawa": ("田泽湖", "Tohoku", "东北"), "nyuto": ("乳头温泉乡", "Tohoku", "东北"), "fukushima": ("福岛", "Tohoku", "东北"),
    "aizu": ("会津若松", "Tohoku", "东北"), "aizuwakamatsu": ("会津若松", "Tohoku", "东北"), "ouchijuku": ("大内宿", "Tohoku", "东北"), "lakeinawashiro": ("猪苗代湖", "Tohoku", "东北"),
    # 关东北部・甲信越
    "nikko": ("日光", "Kanto", "关东"), "kinugawa": ("鬼怒川温泉", "Kanto", "关东"), "nasu": ("那须", "Kanto", "关东"), "utsunomiya": ("宇都宫", "Kanto", "关东"),
    "tochigi": ("栃木", "Kanto", "关东"), "mashiko": ("益子", "Kanto", "关东"), "ashikaga": ("足利", "Kanto", "关东"), "kusatsu": ("草津温泉", "Kanto", "关东"),
    "niigata": ("新潟", "Chubu", "中部"), "sado": ("佐渡岛", "Chubu", "中部"), "echigoyuzawa": ("越后汤泽", "Chubu", "中部"), "yuzawa": ("越后汤泽", "Chubu", "中部"),
    "nagaoka": ("长冈", "Chubu", "中部"), "tokamachi": ("十日町", "Chubu", "中部"), "myoko": ("妙高", "Chubu", "中部"),
    "karuizawa": ("轻井泽", "Chubu", "中部"), "komoro": ("小诸", "Chubu", "中部"), "ueda": ("上田", "Chubu", "中部"), "suwa": ("诹访", "Chubu", "中部"),
    "ina": ("伊那", "Chubu", "中部"), "inavalley": ("伊那谷", "Chubu", "中部"), "komagane": ("驹根", "Chubu", "中部"), "iida": ("饭田", "Chubu", "中部"),
    "achi": ("阿智村", "Chubu", "中部"), "hirugami": ("昼神温泉", "Chubu", "中部"), "obuse": ("小布施", "Chubu", "中部"), "togakushi": ("户隐", "Chubu", "中部"),
    "shibuonsen": ("涩温泉", "Chubu", "中部"), "bessho": ("别所温泉", "Chubu", "中部"), "azumino": ("安昙野", "Chubu", "中部"), "norikura": ("乘鞍", "Chubu", "中部"),
    "kofu": ("甲府", "Chubu", "中部"), "yamanashi": ("山梨", "Chubu", "中部"),
    # 爱知・知多
    "chita": ("知多半岛", "Chubu", "中部"), "chitapeninsula": ("知多半岛", "Chubu", "中部"), "tokoname": ("常滑", "Chubu", "中部"), "handa": ("半田", "Chubu", "中部"),
    "minamichita": ("南知多", "Chubu", "中部"), "centrair": ("中部国际机场", "Chubu", "中部"), "okazaki": ("冈崎", "Chubu", "中部"), "toyota": ("丰田", "Chubu", "中部"),
    "gamagori": ("蒲郡", "Chubu", "中部"), "seto": ("濑户", "Chubu", "中部"), "arimatsu": ("有松", "Chubu", "中部"),
    # 关西补充
    "sakai": ("堺", "Kansai", "关西"), "yumeshima": ("梦洲（世博园区）", "Kansai", "关西"), "expo2025": ("2025 大阪世博", "Kansai", "关西"), "sakaiosaka": ("堺（大阪）", "Kansai", "关西"),
    # 福冈周边
    "itoshima": ("糸岛", "Kyushu", "九州"), "yame": ("八女", "Kyushu", "九州"), "kurume": ("久留米", "Kyushu", "九州"), "munakata": ("宗像", "Kyushu", "九州"),
    "okinoshima": ("冲之岛", "Kyushu", "九州"), "asakura": ("朝仓", "Kyushu", "九州"), "ukiha": ("浮羽", "Kyushu", "九州"), "hita": ("日田", "Kyushu", "九州"),
    "nokonoshima": ("能古岛", "Kyushu", "九州"), "yanagawa": ("柳川", "Kyushu", "九州"), "hakata": ("博多", "Kyushu", "九州"),
    # 北海道补充
    "noboribetsu": ("登别温泉", "Hokkaido", "北海道"), "biei": ("美瑛", "Hokkaido", "北海道"), "lakeshikotsu": ("支笏湖", "Hokkaido", "北海道"),
    # 关东补充
    "kamakura": ("镰仓", "Kanto", "关东"), "enoshima": ("江之岛", "Kanto", "关东"), "chiba": ("千叶", "Kanto", "关东"), "kawagoe": ("川越", "Kanto", "关东"),
})

CITY.update({
    "oita": ("大分", "Kyushu", "九州"), "yoshino": ("吉野", "Kansai", "关西"), "aichi": ("爱知", "Chubu", "中部"), "iwate": ("岩手", "Tohoku", "东北"),
    "miyagi": ("宫城", "Tohoku", "东北"), "hyogo": ("兵库", "Kansai", "关西"), "shiga": ("滋贺", "Kansai", "关西"), "mie": ("三重", "Chubu", "中部"),
    "gifu": ("岐阜", "Chubu", "中部"), "ishikawa": ("石川", "Hokuriku", "北陆"), "shizuoka": ("静冈", "Chubu", "中部"), "hokkaido": ("北海道", "Hokkaido", "北海道"),
    "tohoku": ("东北", "Tohoku", "东北"), "kyushu": ("九州", "Kyushu", "九州"), "shikoku": ("四国", "Shikoku", "四国"), "chugoku": ("中国地方", "Chugoku", "中国地方"),
    "kanto": ("关东", "Kanto", "关东"), "chubu": ("中部", "Chubu", "中部"), "hokuriku": ("北陆", "Hokuriku", "北陆"), "kii": ("纪伊半岛", "Kansai", "关西"),
    "kiipeninsula": ("纪伊半岛", "Kansai", "关西"), "wakayama": ("和歌山", "Kansai", "关西"), "asuka": ("飞鸟", "Kansai", "关西"), "madarao": ("斑尾高原", "Chubu", "中部"),
})

CITY.update({
    "fujimi": ("富士见", "Chubu", "中部"), "fukutsu": ("福津", "Kyushu", "九州"), "izumisano": ("泉佐野", "Kansai", "关西"), "mihama": ("美滨（知多）", "Chubu", "中部"),
    "misawa": ("三泽", "Tohoku", "东北"), "nagakute": ("长久手", "Chubu", "中部"), "ogi": ("小木港", "Chubu", "中部"), "ogiport": ("小木港", "Chubu", "中部"),
    "ryotsu": ("两津港", "Chubu", "中部"), "sai": ("佐井", "Tohoku", "东北"), "southwestsado": ("佐渡西南部", "Chubu", "中部"), "suita": ("吹田", "Kansai", "关西"),
    "hakkoda": ("八甲田", "Tohoku", "东北"), "oirasearea": ("奥入濑", "Tohoku", "东北"), "achi": ("阿智村", "Chubu", "中部"), "kiso": ("木曾", "Chubu", "中部"),
})

CITY.update({
    "bihoro": ("美幌", "Hokkaido", "北海道"), "hasami": ("波佐见", "Kyushu", "九州"), "miyazu": ("宫津（天桥立）", "Kansai", "关西"), "toyooka": ("丰冈", "Kansai", "关西"),
    "ozu": ("大洲", "Shikoku", "四国"), "iyoozu": ("伊予大洲", "Shikoku", "四国"), "sakurai": ("樱井", "Kansai", "关西"), "setoda": ("濑户田（生口岛）", "Setouchi", "濑户内"),
    "ikuchijima": ("生口岛", "Setouchi", "濑户内"), "tamatsukuri": ("玉造温泉", "Chugoku", "中国地方"), "matsue": ("松江", "Chugoku", "中国地方"),
})

CITY.update({
    "nihondaira": ("日本平（静冈）", "Chubu", "中部"), "isawaonsen": ("石和温泉", "Chubu", "中部"), "isawa": ("石和温泉", "Chubu", "中部"), "kashihara": ("橿原", "Kansai", "关西"),
    "mutsu": ("陆奥", "Tohoku", "东北"), "tomi": ("东御", "Chubu", "中部"), "saku": ("佐久", "Chubu", "中部"), "hirugami": ("昼神温泉", "Chubu", "中部"), "hirugamionsen": ("昼神温泉", "Chubu", "中部"),
    "okunikko": ("奥日光", "Kanto", "关东"), "tochigicity": ("栃木市", "Kanto", "关东"), "kanuma": ("鹿沼", "Kanto", "关东"), "aizuwakamatsu": ("会津若松", "Tohoku", "东北"),
    "nyutoonsen": ("乳头温泉乡", "Tohoku", "东北"), "kakunodate": ("角馆", "Tohoku", "东北"), "sadoisland": ("佐渡岛", "Chubu", "中部"), "sadocity": ("佐渡市", "Chubu", "中部"),
    "chitapeninsula": ("知多半岛", "Chubu", "中部"), "nagakute": ("长久手", "Chubu", "中部"), "hakkodaoirase": ("八甲田·奥入濑", "Tohoku", "东北"), "oma": ("大间", "Tohoku", "东北"),
    "kanagawa": ("神奈川", "Kanto", "关东"), "fukutsu": ("福津", "Kyushu", "九州"), "ukiha": ("浮羽", "Kyushu", "九州"), "kurume": ("久留米", "Kyushu", "九州"), "munakata": ("宗像", "Kyushu", "九州"),
    "aomoricity": ("青森市", "Tohoku", "东北"), "hakkoda": ("八甲田", "Tohoku", "东北"), "oirase": ("奥入濑", "Tohoku", "东北"), "goshogawara": ("五所川原", "Tohoku", "东北"),
})

REGION_CN = {
    "Kanto": "关东", "Chubu": "中部", "Hokuriku": "北陆", "Kansai": "关西", "Chugoku": "中国地方",
    "Setouchi": "濑户内", "Shikoku": "四国", "Kyushu": "九州", "Hokkaido": "北海道", "Tohoku": "东北", "Okinawa": "冲绳",
}

import re
def norm(s):
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = s.replace("mt.", "mt").replace("mount ", "mt").replace("-", "").replace(" ", "").replace("'", "").replace("’", "")
    return s

def city_info(name):
    """返回 (中文, 区域EN, 区域CN)，找不到返回 (None, None, None)。"""
    if not name:
        return (None, None, None)
    k = norm(name)
    if k in CITY:
        return CITY[k]
    # 去掉常见后缀再试
    for suf in ("city", "station", "onsen", "area", "region", "island", "lake", "peninsula", "gorge", "stream", "valley", "bay", "coast", "highlands", "highland", "plateau", "village", "town", "prefecture", "mountains", "mountain", "airport"):
        if k.endswith(suf) and k[: -len(suf)] in CITY:
            return CITY[k[: -len(suf)]]
    for pre in ("lake", "mt"):
        if k.startswith(pre) and k[len(pre):] in CITY:
            return CITY[k[len(pre):]]
    # 复合写法 "Toba / Ise-Shima", "Osaka/Nara", "Tokyo Bay / Maihama", "Kashikojima-Kyoto"
    raw = re.sub(r"\(.*?\)", "", name)
    parts = [p for p in re.split(r"[/,&]|\s+-\s+|-(?=[A-Z])", raw) if p.strip()]
    if len(parts) > 1:
        for p in parts:
            r = city_info(p)
            if r[0]: return r
    # 去掉描述性尾词
    m = re.match(r"^([A-Za-z\-' ]+?)\s+(bay|area|region|onsen|ski area|resort|station)\b", raw.strip(), re.I)
    if m:
        r = city_info(m.group(1))
        if r[0]: return r
    return (None, None, None)
