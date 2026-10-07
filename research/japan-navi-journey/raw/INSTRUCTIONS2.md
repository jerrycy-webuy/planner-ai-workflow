# 抓取说明：japan-navi-journey.com（Japan Navi Journey，私人定制团）

背景：该域名被本环境出站代理拦截（curl / WebFetch 都会 403 / EGRESS_BLOCKED）：不要直接抓取，不要通过缓存/存档站绕过。唯一数据通道 = WebSearch（allowed_domains=["japan-navi-journey.com"]）。

**额度纪律（最重要）**：本轮 WebSearch 总额度 200 次、所有子任务共用。你的硬上限写在任务里；达到上限立刻停止搜索并写出文件。若搜索返回「budget is used up」也立刻停止并写出已有结果。先写一次中间结果文件再继续搜，避免成果丢失。

站点结构（已知）：
- 首页 https://japan-navi-journey.com/ ；「Sample Itinerary」索引 https://japan-navi-journey.com/itinerary/ ；每条行程 https://japan-navi-journey.com/itinerary/<slug>/
- 目的地/攻略文章 https://japan-navi-journey.com/column/<id>/ ；客户评价 /reviews/<id>/ ；关于 /about/
- 已知行程 slug：premium-tohoku-gourmet-tour（5D 青森+宫城，大间金枪鱼）、aichi-nagoya-chita（4D 知多半岛）、aomori-unveiled（7D 青森）、nagano-premium-retreat（7D 南信州）、discover-fukuoka（6D 福冈）、nebuta（青森睡魔祭，每日限一组）、osaka-5days（Expo 2025 & Soul of Osaka 5D）；另有 3D2N 津轻温泉旅馆、10D Tokyo & Tohoku 树冰+秘汤、栃木、新潟等行程 slug 未知。

真实性纪律：搜索摘要由小模型生成，可能串标。只记录明确归属到该页面的信息；不编造天数/价格/行程/酒店；拿不到填 null 并在 notes 说明。该站多为定制团，价格通常不公开，price 填 null 并注明「custom quote」。

行程 JSON 元素（写成数组）：
{
  "code": "JNJ-AOMORI-UNVEILED",   // "JNJ-" + slug 大写
  "exists": true, "url": "https://japan-navi-journey.com/itinerary/aomori-unveiled/",
  "title_en": "Aomori Unveiled: Culture of Mountain and Sea at Japan's Northern Edge", "subtitle_en": null,
  "days": 7, "nights": 6, "price_min": null, "price_max": null, "currency": null, "price_note": "custom quote (not published)",
  "series": "JNJ", "themes": ["Luxury", "Culture", "Onsen"], "season": "...或 null", "tour_type": "private custom tour with driver & guide",
  "region": "Tohoku", "prefectures": ["Aomori"],
  "arrival_airport": "...", "departure_airport": "...",
  "route": [{"city": "Aomori", "nights": 2}, ...],
  "day_by_day": [{"day": 1, "title": "...", "from": null, "to": "Aomori", "transport": "private vehicle", "attractions": ["..."], "activities": "...", "meals": "...", "stay": "Aomori (hotel/ryokan name if given)", "notes": null}],
  "hotels": ["..."], "inclusions": ["private vehicle with driver", "English-speaking guide", ...], "exclusions": [],
  "highlights": ["..."], "attractions_all": [{"name_en": "...", "city": "..."}],
  "source_confidence": "high|medium|low", "sources": ["..."], "notes": null
}
写完后校验：python3 -I -c 'import json,sys; json.load(open(sys.argv[1]))' <文件>
最后回复：找到的行程清单（slug/天数/地区）、拿到逐日行程的条数、用了多少次搜索、异常。
