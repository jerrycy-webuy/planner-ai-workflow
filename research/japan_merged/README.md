# 两站合并：行程家族归并 + 可选景点池

> 来源：`../selfguidejapan/`（SGJ，110 条自助游套餐）+ `../japan-navi-journey/`（JNJ，11 条私人定制团） · 2026-10-07 直接抓取版

## 文件

| 文件 | 内容 |
|---|---|
| `merged_itineraries.md` / `.json` | **22 个标准行程家族**：每家族给标准住宿骨架、天数带、价格带、成员变体差异（标来源站）、家族景点池 |
| `attractions_by_city.md` / `.csv` | **可选景点池**：523 个景点按区域 → 城市（79 个）分组，每个带 tag：类别、出现线路数、核心/常见/可选、家族、来源站 |

## 归并逻辑

1. **家族** = 住宿城市骨架（城市顺序 + 过夜数）相同或仅差 1–2 个节点的线路；家族内数据最完整的一条为「标准行程」，其余为变体并写明差异（天数、加减节点、豪华版、SOLO 版、家庭版、主题版）。一条线路可同时属于多个家族（如 KM004 属高野山家族，也属西日本名城与温泉家族）。
2. SGJ 的 110 条归成 F01–F15（黄金路线、北陆、飞驒、西日本名城、伊势志摩、高野山熊野、濑户内四国、九州、北海道夏/冬、本州滑雪、立山黑部、温泉、乐园、奢华）；JNJ 的 11 条归成 F16–F22（青森东北、信州长野、福冈近郊、名古屋知多、佐渡、大阪深度、栃木日光）。JNJ 更像**可挂在 SGJ 骨架前后的深度模块**，每个 JNJ 家族的「归并说明」写明接口节点。
3. **景点 tag**：核心 = 出现 ≥3 条线路（82 个）；常见 = 2 条（34 个）；可选 = 1 条或仅出现在目的地指南/攻略（407 个）。两站都出现 20 个。Planner 做产品时按城市先放核心，再按主题补可选。

## 使用建议（对应 Planner 工作流）

- **A2 立项**：按家族看价格带与天数带，找 WEBUY 货架空缺（东北、长野深度、佐渡、栃木目前只有 JNJ 的私人定制形态）。
- **A4 定价**：SGJ 每条线路的 `price_pdf` 指向站点按出发期的价格表 PDF，可作竞品价带基准。
- **A5 行程文件**：`package_tours.md` 的逐日表已是 house grammar，含酒店与含餐，可直接作为 TourSpec 底稿。
- **A7 卖点**：`core` 景点 = 市场公认必去，适合卖点卡首屏；`可选` 景点可作自费/升级项候选。

## 重新生成

```
python3 -I research/build/scrape_sgj.py <fetch_dir_sgj> <raw_sgj>      # 需先 curl 下载 tours/*.html, destinations/*.html
python3 -I research/build/scrape_jnj.py <fetch_dir_jnj> <raw_jnj>      # itinerary/*.html, itinerary_index.html, column/*.html
python3 -I research/build/consolidate.py <raw_sgj> <out_sgj> selfguidejapan.com
python3 -I research/build/consolidate.py <raw_jnj> <out_jnj> japan-navi-journey.com
python3 -I research/build/build_families.py <out_merged> <out_sgj> <out_jnj>
```
家族定义 `build/families_def.py`，中英对照 `build/names.py` / `build/geo.py`。
