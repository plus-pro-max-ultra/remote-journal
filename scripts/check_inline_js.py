#!/usr/bin/env python3
"""Syntax-check inline JavaScript blocks with Node.js, without a browser."""
from pathlib import Path
import re, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/"index.html").read_text(encoding="utf-8")
blocks=[m.group(1) for m in re.finditer(r'<script(?:\s+[^>]*)?>([\s\S]*?)</script>',html) if m.group(1).strip()]
if not shutil.which("node"):
    raise SystemExit("此檢查需要 Node.js；請在支援 Node.js 的環境執行。")
with tempfile.TemporaryDirectory() as td:
    for i, code in enumerate(blocks,1):
        path=Path(td)/f"inline-{i}.js"
        path.write_text(code,encoding="utf-8")
        result=subprocess.run(["node","--check",str(path)],capture_output=True,text=True)
        if result.returncode:
            print(result.stderr,file=sys.stderr)
            raise SystemExit(result.returncode)
print(f"完成：{len(blocks)} 個 inline JavaScript 區塊語法檢查通過。")
