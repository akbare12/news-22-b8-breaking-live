#!/usr/bin/env python3
"""Copy the entry image to /output/entry.png and verify it.

The image itself is drawn by draw.py (PIL, stdlib + Pillow) and stored in this
repository as entry.png; this program only reproduces it byte-identically.
"""
import hashlib
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST = "/output/entry.png"
EXPECTED_SHA256 = "0eeeef5b68570a7bacc6b6b42cdd589b7205e4d75d665a8301e57d60e83f12a2"
EXPECTED_BYTES = 174072


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print(f"missing source image: {SRC}", file=sys.stderr)
        sys.exit(1)
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    size = os.path.getsize(DST)
    digest = sha256_of(DST)
    if size != EXPECTED_BYTES:
        print(f"size mismatch: got {size}, expected {EXPECTED_BYTES}", file=sys.stderr)
        sys.exit(1)
    if digest != EXPECTED_SHA256:
        print(f"sha256 mismatch: got {digest}", file=sys.stderr)
        sys.exit(1)
    print(f"wrote {DST} ({size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
