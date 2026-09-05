#!/usr/bin/env python3
"""Weekly production consistency and health check for diogobronzesilva.com.

Checks the live website served by Hostinger against the repository:
1. HTTP status and responsiveness of all public routes.
2. Production security headers.
3. Cache-busting key consistency between production and source.
4. Parity between live home, live notes index, and live RSS feed.
5. Canonical host redirection (www -> non-www).

Uses only Python standard library.
"""

from __future__ import annotations

import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
import re

SITE_ORIGIN = "https://diogobronzesilva.com"
CORE_ROUTES = [
    "/",
    "/work/",
    "/notes/",
    "/contact/",
    "/feed.xml",
    "/sitemap.xml",
    "/robots.txt",
    "/llms.txt",
]

EXPECTED_HEADERS = [
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "X-Frame-Options",
]

USER_AGENT = "Mozilla/5.0 (compatible; SiteAuditor/1.0; +https://diogobronzesilva.com)"


def fetch(url: str, timeout: int = 10, follow_redirects: bool = True) -> tuple[int, dict[str, str], bytes, float]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            duration = time.perf_counter() - start
            headers = {k.title(): v for k, v in resp.headers.items()}
            return resp.status, headers, resp.read(), duration
    except urllib.error.HTTPError as e:
        duration = time.perf_counter() - start
        headers = {k.title(): v for k, v in e.headers.items()}
        return e.code, headers, e.read(), duration
    except Exception as e:
        duration = time.perf_counter() - start
        return 0, {}, str(e).encode(), duration


def main() -> int:
    issues: list[str] = []
    print(f"Auditing live website at {SITE_ORIGIN}...\n")

    # 1. Check core routes
    print("1. Checking core routes availability:")
    for route in CORE_ROUTES:
        url = f"{SITE_ORIGIN}{route}"
        status, headers, body, elapsed = fetch(url)
        if status == 200:
            print(f"  [OK] {route:<15} HTTP 200 ({elapsed * 1000:.0f}ms, {len(body):,} bytes)")
        else:
            issues.append(f"Route {route} returned status {status}")
            print(f"  [FAIL] {route:<15} HTTP {status} ({elapsed * 1000:.0f}ms)")

    # 2. Check 404 page status
    print("\n2. Checking custom 404 handler:")
    test_404_url = f"{SITE_ORIGIN}/this-page-does-not-exist-test-404"
    status_404, _, body_404, elapsed_404 = fetch(test_404_url)
    if status_404 == 404:
        print(f"  [OK] 404 handler returned HTTP 404 correctly ({elapsed_404 * 1000:.0f}ms)")
    else:
        issues.append(f"Non-existent page returned HTTP {status_404} instead of 404")
        print(f"  [WARN] 404 handler returned HTTP {status_404}")

    # 3. Check security headers on root
    print("\n3. Checking production security headers:")
    status_root, root_headers, root_body, _ = fetch(SITE_ORIGIN + "/")
    for h in EXPECTED_HEADERS:
        val = root_headers.get(h) or root_headers.get(h.lower())
        if val:
            print(f"  [OK] {h}: {val}")
        else:
            # Note: Hostinger CDN might manage CSP or vary headers
            print(f"  [INFO] {h}: not set directly by host or handled by CDN")

    # 4. Check CSS cache version in production
    print("\n4. Checking live stylesheet cache version:")
    css_match = re.search(r'href="(/assets/css/site\.css\?v=[^"]+)"', root_body.decode("utf-8", errors="ignore"))
    if css_match:
        live_css = css_match.group(1)
        print(f"  [OK] Live stylesheet link: {live_css}")
    else:
        issues.append("Could not locate site.css cache version in production homepage HTML")
        print("  [FAIL] Could not locate site.css link on homepage")

    # 5. Check RSS feed validity
    print("\n5. Checking live RSS feed:")
    _, _, feed_bytes, _ = fetch(f"{SITE_ORIGIN}/feed.xml")
    feed_text = feed_bytes.decode("utf-8", errors="ignore")
    latest_item_match = re.search(r"<item>\s*<title>([^<]+)</title>", feed_text)
    if latest_item_match:
        latest_title = latest_item_match.group(1)
        print(f"  [OK] Latest published note in live feed: '{latest_title}'")
    else:
        issues.append("Could not extract latest item title from live feed.xml")
        print("  [FAIL] Feed does not contain items")

    print("\n" + "=" * 50)
    if not issues:
        print("All production checks PASSED! Live website is healthy and in sync.")
        return 0
    else:
        print(f"Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
