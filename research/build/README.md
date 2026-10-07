# 生成脚本

- `scrape_sgj.py <fetch_dir> <out_dir>`：解析 selfguidejapan.com 已下载页面（Next.js RSC 线路对象）→ 线路 JSON + 目的地 JSON
- `scrape_jnj.py <fetch_dir> <out_dir>`：解析 japan-navi-journey.com 已下载页面（WordPress 模板）→ 行程 JSON + 景点 JSON
- `consolidate.py <raw_dir> <out_dir> <site>`：汇总 → 目录 / 标准行程 / 景点列表
- `build_families.py <out_merged> <out_site1> [<out_site2> ...]`：行程家族归并 + 景点按城市 tag（多站合并）
- `families_def.py`：家族定义（人工归并）；`geo.py`：城市 → 中文 / 区域；`names.py`：线路名 / 景点中文对照

运行时用 `python3 -I`（脚本内部自行 sys.path）。下载页面用 curl 配浏览器 UA，间隔 0.4s。
