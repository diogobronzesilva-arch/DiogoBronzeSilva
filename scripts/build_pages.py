#!/usr/bin/env python3
"""Create a Pages upload containing only public website files."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist"


def main():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    subprocess.run([sys.executable, str(ROOT / "scripts/check_site.py")], check=True)
    OUTPUT.mkdir()
    for name in ("assets", "work", "notes", "contact"):
        shutil.copytree(ROOT / name, OUTPUT / name)
    (OUTPUT / "notes/_template.html").unlink(missing_ok=True)
    for name in ("index.html", "404.html", "favicon.ico", "feed.xml", "sitemap.xml",
                 "robots.txt", "llms.txt", "llms-full.txt", "_headers"):
        shutil.copy2(ROOT / name, OUTPUT / name)
    print("Pages files ready in dist/")


if __name__ == "__main__":
    main()
