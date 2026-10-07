# 抓取说明（所有系列子任务共用）

背景：整理 https://selfguidejapan.com（BluePlanet「Self-Guided Japan」）全部线路。
该域名被本环境出站代理拦截（curl / WebFetch 都会 403 / EGRESS_BLOCKED）：
- 不要直接抓取，不要通过缓存/存档站绕过。
- 唯一数据通道 = WebSearch 工具（服务端搜索），它返回该站页面的摘要。

方法（每个线路代码）：
1. WebSearch(query="selfguidejapan.com/tours/<CODE>", allowed_domains=["selfguidejapan.com"], mode="standard")
2. 拿到线路名后再搜一次：query="selfguidejapan.com/tours/<CODE> <线路名> itinerary day by day hotels price"（结果薄就用 mode="extended"）
3. 逐日行程缺天数时补搜：query="selfguidejapan.com/tours/<CODE> <线路名> Day 7 Day 8 Day 9 Day 10 Day 11 Day 12"
4. 判断存在：结果 Links 里出现 https://selfguidejapan.com/tours/<CODE>；页面标题形如「【CODE】Name」或直接是线路名。
   两次搜索 Links 都没有该 URL 且摘要未提到该代码 → exists=false。

真实性纪律：搜索摘要由小模型生成，经常把别的线路的名字/价格套到这个代码上。
- 只记录明确归属到该 CODE 页面（URL/标题匹配）的信息；来自博客或主题页的交叉信息写进 sources 并标明。
- 不编造天数/价格/行程/酒店；拿不到就填 null，并在 notes 说明。
- 价格原样记录币种（USD / A$ 等）。

输出：JSON 数组写到指定文件（Bash heredoc 或 python 写入，目录已存在），每个元素：
{
  "code": "GR001", "exists": true, "url": "https://selfguidejapan.com/tours/GR001",
  "title_en": "Hidden Gems of Japan: Ise-Shima Escape", "subtitle_en": null,
  "days": 12, "nights": 11,
  "price_min": 3300, "price_max": 4400, "currency": "USD",
  "price_note": "per person, two sharing, excl. intl flights",
  "series": "GR", "themes": ["Hidden Gems"], "season": null,
  "arrival_airport": "Haneda/Narita", "departure_airport": "Kansai",
  "route": [{"city": "Tokyo", "nights": 2}, {"city": "Nagoya", "nights": 1}],
  "day_by_day": [
    {"day": 1, "title": "Welcome to Japan", "from": null, "to": "Tokyo",
     "transport": null, "attractions": [], "activities": "Airport meet, hotel check-in",
     "meals": null, "stay": "Tokyo", "notes": null}
  ],
  "inclusions": ["hotels", "Shinkansen", "luggage delivery", "airport meet", "24/7 support"],
  "exclusions": ["international flights"],
  "highlights": ["..."],
  "attractions_all": [{"name_en": "Sensoji Temple", "city": "Tokyo"}],
  "source_confidence": "high|medium|low",
  "sources": ["https://selfguidejapan.com/tours/GR001"],
  "notes": null
}
写完后校验：python3 -I -c 'import json,sys; json.load(open(sys.argv[1]))' <文件>
最后回复：存在/不存在代码清单、拿到逐日行程的代码数、未拿到的代码数、异常。
