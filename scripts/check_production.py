#!/usr/bin/env python3
"""Weekly production consistency and health check for diogobronzesilva.com.

Checks the live website served by Hostinger against the repository source:
1. HTTP status and responsiveness of all public routes.
2. Production security headers.
3. Cache-busting key consistency between production and source index.html.
4. Parity between live feed.xml and repository feed.xml (title and link).
5. Completeness of live sitemap.xml compared to repository.
6. Canonical host redirection (www -> non-www).

Uses only Python standard library.
"""

from __future__ import annotations

import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    start = time.perf_counter()
    try:
        opener = urllib.request.build_opener() if follow_redirects else urllib.request.build_opener(NoRedirect)
        with opener.open(req, timeout=timeout) as resp:
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
    print(f"Auditing live website at {SITE_ORIGIN} against repository {ROOT}...\n")

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
            print(f"  [WARN] {h}: not set directly by origin or handled upstream by CDN")

    # 4. Check CSS cache version in production against repository index.html
    print("\n4. Checking live stylesheet cache version against repository:")
    css_match = re.search(r'href="(/assets/css/site\.css\?v=[^"]+)"', root_body.decode("utf-8", errors="ignore"))
    local_index_path = ROOT / "index.html"
    local_css_match = None
    if local_index_path.is_file():
        local_css_match = re.search(r'href="(/assets/css/site\.css\?v=[^"]+)"', local_index_path.read_text(encoding="utf-8"))

    if css_match:
        live_css = css_match.group(1)
        if local_css_match:
            expected_css = local_css_match.group(1)
            if live_css == expected_css:
                print(f"  [OK] Live stylesheet link matches repository: {live_css}")
            else:
                issues.append(f"CSS cache version mismatch: live={live_css} vs repository={expected_css}")
                print(f"  [FAIL] CSS cache version mismatch: live={live_css} vs repository={expected_css}")
        else:
            print(f"  [OK] Live stylesheet link: {live_css}")
    else:
        issues.append("Could not locate site.css cache version in production homepage HTML")
        print("  [FAIL] Could not locate site.css link on homepage")

    # 5. Check RSS feed validity and parity with repository
    print("\n5. Checking live RSS feed against repository:")
    _, _, feed_bytes, _ = fetch(f"{SITE_ORIGIN}/feed.xml")
    feed_text = feed_bytes.decode("utf-8", errors="ignore")
    latest_item_match = re.search(r"<item>\s*<title>([^<]+)</title>\s*<link>([^<]+)</link>", feed_text)

    local_feed_path = ROOT / "feed.xml"
    local_item_match = None
    if local_feed_path.is_file():
        local_item_match = re.search(r"<item>\s*<title>([^<]+)</title>\s*<link>([^<]+)</link>", local_feed_path.read_text(encoding="utf-8"))

    if latest_item_match:
        live_title = latest_item_match.group(1).strip()
        live_link = latest_item_match.group(2).strip()
        if local_item_match:
            expected_title = local_item_match.group(1).strip()
            expected_link = local_item_match.group(2).strip()
            if live_title == expected_title and live_link == expected_link:
                print(f"  [OK] Latest published note in live feed matches repository: '{live_title}' ({live_link})")
            else:
                issues.append(f"Latest note mismatch in feed.xml: live='{live_title}' ({live_link}) vs repository='{expected_title}' ({expected_link})")
                print(f"  [FAIL] Live feed out of sync with repository: live='{live_title}', expected='{expected_title}'")
        else:
            print(f"  [OK] Latest published note in live feed: '{live_title}'")
    else:
        issues.append("Could not extract latest item title/link from live feed.xml")
        print("  [FAIL] Live feed does not contain expected item structure")

    # 6. Check sitemap parity with repository
    print("\n6. Checking sitemap parity against repository:")
    _, _, sitemap_bytes, _ = fetch(f"{SITE_ORIGIN}/sitemap.xml")
    sitemap_text = sitemap_bytes.decode("utf-8", errors="ignore")
    local_sitemap_path = ROOT / "sitemap.xml"
    if local_sitemap_path.is_file():
        local_sitemap_text = local_sitemap_path.read_text(encoding="utf-8")
        live_urls = set(re.findall(r"<loc>([^<]+)</loc>", sitemap_text))
        local_urls = set(re.findall(r"<loc>([^<]+)</loc>", local_sitemap_text))
        missing_live = local_urls - live_urls
        if missing_live:
            issues.append(f"Production sitemap missing URLs present in repository: {missing_live}")
            print(f"  [FAIL] Production sitemap missing {len(missing_live)} URL(s)")
        else:
            print(f"  [OK] Production sitemap contains all {len(local_urls)} repository URLs")

    # 7. Check canonical host redirection (www -> non-www)
    print("\n7. Checking www canonical redirect:")
    www_status, www_headers, _, www_elapsed = fetch("https://www.diogobronzesilva.com/", follow_redirects=False)
    www_location = www_headers.get("Location", "")
    if www_status == 301 and www_location.rstrip("/") == SITE_ORIGIN:
        print(f"  [OK] https://www.diogobronzesilva.com/ redirects 301 -> {www_location} ({www_elapsed * 1000:.0f}ms)")
    else:
        issues.append(f"www redirect check failed: HTTP {www_status}, Location: {www_location}")
        print(f"  [FAIL] Expected 301 redirect to {SITE_ORIGIN}/, got HTTP {www_status} (Location: {www_location})")

    print("\n" + "=" * 50)
    if not issues:
        print("All production checks PASSED! Live website is healthy and in sync with repository.")
        return 0
    else:
        print(f"Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
