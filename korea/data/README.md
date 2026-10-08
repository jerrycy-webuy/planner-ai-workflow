# 韩国线竞品数据（2026-10-08 抓取）

| 目录 | 来源 | 形态 | 条数 | 抓取方式 |
|---|---|---|---|---|
| `chanbrothers/` | https://www.chanbrothers.com （新加坡） | Package Tours 跟团 18 · Free & Easy+ 10 · Private Tours 3 | 31 | 站点 sitemap 取韩国线 → 产品页 `__NEXT_DATA__` 取 entity_id → `cms.chanbrothers.com/api/trip-detail/<id>`（结构化逐日：路线城市、交通方式、每日亮点、酒店、含餐） |
| `euholidays/` | https://www.euholidays.com.sg （新加坡） | Group Holidays 跟团 | 7 | 产品页 Next.js RSC 流：逐日中英文描述、按出发日期的价格矩阵（双人/单人/儿童/税）与航班 |
| `dynastytravel/` | https://www.dynastytravel.com.sg （新加坡） | 高端小团 | 9 | 同上（与 EU 同一 Tourix 后台）；逐日描述含酒店 |
| `koreatraveleasy/` | https://www.koreatraveleasy.com （首尔地接） | 首尔出发英文拼团 | 6 | WordPress 自由排版，人工转写（`scripts/kte_multiday.py`） |
| `merged/` | 四站合并 | — | 14 家族 / 359 景点 | `scripts/build_kb_kr.py` |

每个站点目录：`tours_catalog.md/.csv`（目录）· `package_tours.md`（逐日标准行程）· `attractions.md/.csv`（景点）· `raw/<site>_tours.json`（统一 schema 的解析结果，含逐日原文描述，供溯源）。

EU Holidays 站点 sitemap 里另有 9 个韩国线 URL 已下架（页面无行程数据），Chan Brothers 有 17 个已下架（404），均未计入。
