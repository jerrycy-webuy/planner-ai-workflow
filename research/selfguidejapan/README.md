# Self-Guided Japan（selfguidejapan.com）线路与景点整理

> 来源：https://selfguidejapan.com（BluePlanet「Self-Guided Japan」自助游套餐：酒店 + 新干线 + 行李托运 + 机场接站 + 24/7 支援，不含国际机票；价格每人、两人一房，SOLO 系列单人价）
> 抓取：2026-10-07 直接抓取全站（sitemap 110 条线路、88 个目的地页）。**私有仓库内部资料。** 两站合并结果见 `../japan_merged/`，脚本见 `../build/`。

## 文件

| 文件 | 内容 |
|---|---|
| `tours_catalog.md` / `.csv` | 线路目录：110 条（代码 / 名称 EN+CN / 天数 / 住宿骨架 / 价格 / 主题 / URL），按系列分组 |
| `package_tours.md` / `.json` | **标准行程（Package Tour 格式）**：每条线路一节，house grammar（`CITY_EN 中文 (2N)`、`>` 陆路 / `✈` 航班），**110 条全部有完整逐日表**，含酒店名/夜数、逐日含餐（B/L/D）、含/不含项、三币种价格与价格表 PDF 链接 |
| `attractions.md` / `.csv` | 景点列表：249 个景点/体验（EN / 中文 / 城市 / 区域 / 类别 / 出现线路），主要来自线路逐日「推荐景点」 |
| `raw/sgj_tours.json` | 110 条线路解析结果（本仓库 schema） · `raw/sgj_tours_raw.json` 站点原始线路对象 · `raw/destinations.json` 88 个目的地（日文名/区域/坐标） · `raw/search_pass/` 前两轮搜索摘要数据（仅溯源） |

## 覆盖情况

| 项 | 数量 |
|---|---|
| 站点 sitemap 线路数 | 110（上两轮搜索索引里的 NT002/NT006/NT007/NT008/SL103 已下架，404） |
| 本次解析线路 | **110**，全部含逐日行程、住宿骨架、酒店名、价格 |
| 景点 / 体验 | 249，覆盖 29 个城市/地点 |

系列分布：BF 5 · EX 4 · FG 5 · GR 20 · HD 2 · HK 9 · HS 3 · KA 3 · KM 8 · KR 4 · KY 5 · LX 3 · NT 5 · SE 5 · SK 15 · SL 5 · TP 9

系列含义：BF 7 天基础 · GR 黄金路线（1xx 豪华版）· KM 高野山 · SE 濑户内 · KY 九州 · HD/HK 北海道夏/冬 · SK 本州滑雪 · NT 阿尔卑斯/熊野 · EX 体验主题（茶道、餐厅列车、雪猴）· KR 近铁短线 · TP 乐园 · FG 家庭 · SL 单人 · LX 奢华 · HS 温泉 · KA 关西进出

## 方法（2026-10-07 第三轮：直接抓取）

1. 域名放行后用 curl 直接下载：站点 sitemap → 全部产品页 / 目的地页 / 行程页 / 攻略文章，原始 HTML 不入库，解析结果 JSON 在 `raw/`。
2. selfguidejapan.com 是 Next.js 站，产品页内嵌完整线路对象（逐日 title/description/destination、酒店名与夜数、逐日含餐、三币种价格、含/不含项、主题），逐日描述中「★景点→说明」结构化为景点库；目的地页给出日文名、区域、经纬度。
3. japan-navi-journey.com 是 WordPress 站，行程页按 `.itinerary-day` 逐日解析，含「SERVICE INCLUDES」与按人数的日元参考报价（data-price-2…5）；景点来自行程正文的地名抽取 + 83 篇 `/column/` 攻略文章标题，并保留第二轮搜索摘要整理的目的地景点作为补充（来源标「目的地指南」）。
4. 前两轮基于搜索索引摘要的数据保留在 `raw/search_pass/` 仅作溯源，不再参与生成。
5. 中文名为本仓库整理时的译名（线路名意译；景点用通用中文名），非站点官方译名。

