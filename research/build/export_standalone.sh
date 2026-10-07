#!/usr/bin/env bash
# 把 research/ 导出为独立仓库「Japan Tour Planner」的目录结构（kb/ skill/ scripts/ data/）。
# 用法: research/build/export_standalone.sh <目标目录>
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)"
NEW="${1:?目标目录}"
mkdir -p "$NEW/data/selfguidejapan" "$NEW/data/japan-navi-journey" "$NEW/data/merged" "$NEW/kb" "$NEW/scripts" "$NEW/skill"
cp -r "$SRC/selfguidejapan/." "$NEW/data/selfguidejapan/"
cp -r "$SRC/japan-navi-journey/." "$NEW/data/japan-navi-journey/"
cp -r "$SRC/japan_merged/." "$NEW/data/merged/"
cp -r "$SRC/japan_kb/." "$NEW/kb/"
cp "$SRC"/build/*.py "$SRC"/build/*.json "$SRC/build/README.md" "$NEW/scripts/"
cp -r "$SRC/itinerary_skill/." "$NEW/skill/"
cp "$SRC/build/standalone_README.md" "$NEW/README.md"
printf '__pycache__/\n*.pyc\n.DS_Store\nout/\n*.err_*\n' > "$NEW/.gitignore"
python3 - "$NEW" <<'PY'
import sys, glob, os
NEW = sys.argv[1]; os.chdir(NEW)
reps = [("research/build/", "scripts/"), ("research/japan_kb/", "kb/"), ("research/japan_kb", "kb"), ("research/itinerary_skill/", "skill/"), ("research/itinerary_skill", "skill"),
        ("research/selfguidejapan/", "data/selfguidejapan/"), ("research/japan-navi-journey/", "data/japan-navi-journey/"), ("research/japan_merged/", "data/merged/"),
        ("../japan_merged/", "../merged/"), ("`../build/`", "`../../scripts/`"), ("../build/", "../../scripts/")]
for f in glob.glob("**/*.md", recursive=True) + glob.glob("**/*.py", recursive=True):
    s = open(f, encoding="utf-8").read(); o = s
    for a, b in reps: s = s.replace(a, b)
    if s != o: open(f, "w", encoding="utf-8").write(s)
for f in ("scripts/validate_itinerary.py", "scripts/retrieve.py", "scripts/generate_itinerary.py"):
    s = open(f, encoding="utf-8").read().replace('os.path.join(HERE, "..", "japan_kb")', 'os.path.join(HERE, "..", "kb")')
    open(f, "w", encoding="utf-8").write(s)
PY
echo "exported to $NEW"
