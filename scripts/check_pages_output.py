#!/usr/bin/env python3
"""Ensure dist/ contains exactly the public Cloudflare Pages files."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist"
PUBLIC_DIRECTORIES = ("assets", "work", "notes", "contact")
PUBLIC_ROOT_FILES = (
    "index.html",
    "404.html",
    "favicon.ico",
    "feed.xml",
    "sitemap.xml",
    "robots.txt",
    "llms.txt",
    "llms-full.txt",
    "_headers",
)
TEMPLATE = Path("notes/_template.html")


def expected_files() -> set[str]:
    files = {Path(name).as_posix() for name in PUBLIC_ROOT_FILES}
    for directory in PUBLIC_DIRECTORIES:
        for path in (ROOT / directory).rglob("*"):
            if path.is_file():
                relative = path.relative_to(ROOT)
                if relative != TEMPLATE:
                    files.add(relative.as_posix())
    return files


def main() -> int:
    if not OUTPUT.is_dir():
        print("Pages output check failed: dist/ does not exist.")
        return 1

    expected = expected_files()
    actual = {
        path.relative_to(OUTPUT).as_posix()
        for path in OUTPUT.rglob("*")
        if path.is_file()
    }
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    mismatched = sorted(
        relative
        for relative in expected & actual
        if (ROOT / relative).read_bytes() != (OUTPUT / relative).read_bytes()
    )
    if missing or unexpected or mismatched:
        print("Pages output check failed.")
        for path in missing:
            print(f"Missing public file: {path}")
        for path in unexpected:
            print(f"Unexpected deployment file: {path}")
        for path in mismatched:
            print(f"Output does not match source: {path}")
        return 1

    print(f"Pages output contains exactly {len(actual)} expected public files, byte-for-byte.")
    print("Repository documentation, scripts, GitHub workflow, and notes template are excluded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
