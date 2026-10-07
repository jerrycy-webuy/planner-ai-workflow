# 两站合并：行程家族归并 + 可选景点池

> 来源：`../selfguidejapan/`（SGJ，89 条自助游套餐）+ `../japan-navi-journey/`（JNJ，12 条私人定制团） · 2026-10-07

## 文件

| 文件 | 内容 |
|---|---|
| `merged_itineraries.md` / `.json` | **22 个标准行程家族**：每家族给标准住宿骨架、天数带、价格带、成员变体差异（标来源站）、家族景点池 |
| `attractions_by_city.md` / `.csv` | **可选景点池**：582 个景点按区域 → 城市（168 个）分组，每个带 tag：类别、出现线路数、核心/常见/可选、家族、来源站 |

## 归并逻辑

1. **家族** = 住宿城市骨架（城市顺序 + 过夜数）相同或仅差 1–2 个节点的线路；家族内数据最完整的一条为「标准行程」，其余为变体并写明差异（天数、加减节点、豪华版、SOLO 版、家庭版、主题版）。
2. SGJ 的 89 条归成 F01–F15（黄金路线、北陆、飞驒、西日本名城、伊势志摩、高野山熊野、濑户内四国、九州、北海道夏/冬、本州滑雪、立山黑部、温泉、乐园、奢华）；JNJ 的 12 条归成 F16–F22（青森东北、信州长野、福冈近郊、名古屋知多、佐渡、大阪深度、栃木日光）。两站重叠极少，JNJ 更像**可挂在 SGJ 骨架前后的深度模块**（每个 JNJ 家族的「归并说明」已写明接口节点）。
3. **景点 tag**：核心 = 出现 ≥3 条线路（48 个）；常见 = 2 条（34 个）；可选 = 1 条或仅出现在目的地指南（500 个）。两站都出现的景点 17 个。Planner 做产品时按城市先放核心，再按主题补可选。

## 使用建议（对应 Planner 工作流）

- **A2 立项**：按家族看价格带与天数带，找 WEBUY 货架空缺（例如东北、长野、佐渡、栃木目前只有 JNJ 的私人定制形态，没有团体/自助套餐形态）。
- **A5 行程文件**：`package_tours.md` 的逐日表已是 house grammar，可直接作为 TourSpec 底稿；`attractions_by_city` 的「可选」景点可作自费/升级项候选。
- **A7 卖点**：`core` 景点 = 市场公认必去，适合做卖点卡首屏。

## 重新生成

```
python3 -I research/build/consolidate.py <raw_dir_sgj> <out_sgj> selfguidejapan.com
python3 -I research/build/consolidate.py <raw_dir_jnj> <out_jnj> japan-navi-journey.com
python3 -I research/build/build_families.py <out_merged> <out_sgj> <out_jnj>
```
家族定义在 `build/families_def.py`，中英对照在 `build/names.py` / `build/geo.py`。
