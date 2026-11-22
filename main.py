#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122.

Copies the pre-drawn front page (entry.png, produced by draw.py in this
same repository) into the output directory the harness provides.
Standard library only; no network, no extra dependencies.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied", src, "->", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    sys.exit(main())
