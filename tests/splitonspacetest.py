#!/usr/bin/python3
import sys
sys.path.append("..")
import fbutil

"""
with open("lorem.txt") as f:
    lines = fbutil.splitOnSpace(f.read(), 50)
    print("\n".join(lines))
"""
a="po pierwsze, ściągnij emscripten stąd https://kripken.github.io/emscripten-site/docs/getting_started/downloads.html"

print(fbutil.splitOnSpace(a, 86))