#!/usr/bin/env python3
from pathlib import Path
root = Path(__file__).resolve().parent
body = (root/"gp_partA.txt").read_text() + (root/"gp_partB.txt").read_text()
target = root/"_body.py"
target.write_text(body)
import runpy
runpy.run_path(str(target), run_name="__main__")
