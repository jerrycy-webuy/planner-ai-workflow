# 生成脚本

- `consolidate.py <raw_dir> <out_dir> <site>`：汇总子任务 JSON → 目录 / 标准行程 / 景点列表
- `build_families.py <out_merged> <out_site1> [<out_site2> ...]`：行程家族归并 + 景点按城市 tag（多站合并）
- `families_def.py`：家族定义（人工归并）
- `geo.py`：城市 → 中文 / 区域；`names.py`：线路名 / 景点中文对照

运行时用 `python3 -I`（脚本内部自行 sys.path）。
