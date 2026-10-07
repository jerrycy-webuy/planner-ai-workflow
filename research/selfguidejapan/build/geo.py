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
    for suf in ("city", "station", "onsen", "area", "region", "island", "lake"):
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
