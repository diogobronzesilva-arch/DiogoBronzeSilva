#!/usr/bin/env python3
"""Static consistency checks for diogobronzesilva.com.

The checker intentionally uses only Python's standard library so the GitHub
Action stays small, deterministic and dependency-free.
"""

from __future__ import annotations

import json
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE_ORIGIN = "https://diogobronzesilva.com"
SITE_HOST = "diogobronzesilva.com"
TEMPLATE = Path("notes/_template.html")
NOT_FOUND = Path("404.html")

REQUIRED_META_NAMES = {
    "description",
    "author",
    "twitter:card",
    "twitter:title",
    "twitter:description",
    "twitter:image",
    "twitter:image:alt",
}
REQUIRED_OG_PROPERTIES = {
    "og:title",
    "og:description",
    "og:type",
    "og:url",
    "og:image",
    "og:image:alt",
    "og:site_name",
}
PLACEHOLDERS = (
    "TITLE OF THE NOTE",
    "ONE SENTENCE ABOUT THIS NOTE",
    "SLUG-DA-NOTA",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.title_parts: list[str] = []
        self.in_title = False
        self.meta_names: dict[str, str] = {}
        self.meta_properties: dict[str, str] = {}
        self.canonicals: list[str] = []
        self.references: list[tuple[str, str, str]] = []
        self.images: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.inputs: list[dict[str, str]] = []
        self.labels_for: set[str] = set()
        self.ids: list[str] = []
        self.stylesheets: list[str] = []
        self.rss_links: list[str] = []
        self.json_ld_blocks: list[str] = []
        self._json_ld_buffer: list[str] | None = None

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key.lower(): (value or "") for key, value in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        data = self._attrs(attrs)

        if tag == "html" and self.lang is None:
            self.lang = data.get("lang", "").strip()
        if tag == "title":
            self.in_title = True
        if "id" in data:
            self.ids.append(data["id"])

        if tag == "meta":
            content = data.get("content", "").strip()
            if data.get("name"):
                self.meta_names[data["name"].lower()] = content
            if data.get("property"):
                self.meta_properties[data["property"].lower()] = content

        if tag == "link" and data.get("href"):
            href = data["href"]
            rel_tokens = {token.lower() for token in data.get("rel", "").split()}
            self.references.append((tag, "href", href))
            if "canonical" in rel_tokens:
                self.canonicals.append(href)
            if "stylesheet" in rel_tokens:
                self.stylesheets.append(href)
            if (
                "alternate" in rel_tokens
                and data.get("type", "").lower() == "application/rss+xml"
            ):
                self.rss_links.append(href)

        if tag == "a":
            self.anchors.append(data)
            if data.get("href"):
                self.references.append((tag, "href", data["href"]))

        if tag == "img":
            self.images.append(data)
            if data.get("src"):
                self.references.append((tag, "src", data["src"]))

        if tag in {"script", "source"} and data.get("src"):
            self.references.append((tag, "src", data["src"]))

        if tag == "source" and data.get("srcset"):
            for item in data["srcset"].split(","):
                url = item.strip().split()[0] if item.strip() else ""
                if url:
                    self.references.append((tag, "srcset", url))

        if tag == "input":
            self.inputs.append(data)

        if tag == "label" and data.get("for"):
            self.labels_for.add(data["for"])

        if tag == "script" and data.get("type", "").lower() == "application/ld+json":
            self._json_ld_buffer = []

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        if tag == "script" and self._json_ld_buffer is not None:
            self.json_ld_blocks.append("".join(self._json_ld_buffer).strip())
            self._json_ld_buffer = None

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self._json_ld_buffer is not None:
            self._json_ld_buffer.append(data)

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()


class Report:
    def __init__(self) -> None:
        self.errors: list[tuple[str | None, str]] = []
        self.sections: list[str] = []

    def error(self, message: str, path: Path | str | None = None) -> None:
        self.errors.append((str(path) if path is not None else None, message))

    def passed(self, label: str) -> None:
        self.sections.append(label)

    def finish(self) -> int:
        if self.errors:
            print(f"Site validation failed with {len(self.errors)} error(s).")
            for path, message in self.errors:
                safe = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
                if path:
                    print(f"::error file={path}::{safe}")
                    print(f"ERROR {path}: {message}")
                else:
                    print(f"::error::{safe}")
                    print(f"ERROR: {message}")
            return 1

        for label in self.sections:
            print(f"OK  {label}")
        print("\nSite validation passed.")
        return 0


def relative(path: Path) -> Path:
    return path.relative_to(ROOT)


def published_html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        rel = relative(path)
        if ".git" in rel.parts or rel in {TEMPLATE, NOT_FOUND}:
            continue
        files.append(path)
    return sorted(files)


def all_html_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if ".git" not in relative(path).parts
    )


def public_path_for_file(rel: Path) -> str:
    if rel == Path("index.html"):
        return "/"
    if rel.name == "index.html":
        return "/" + rel.parent.as_posix().strip("/") + "/"
    return "/" + rel.as_posix()


def expected_url(rel: Path) -> str:
    return SITE_ORIGIN + public_path_for_file(rel)


def parse_page(path: Path, report: Report) -> PageParser | None:
    parser = PageParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
    except (OSError, UnicodeError) as exc:
        report.error(f"Could not read HTML: {exc}", relative(path))
        return None
    return parser


def local_target(page_rel: Path, raw_url: str) -> Path | None:
    raw_url = raw_url.strip()
    if not raw_url or raw_url.startswith("#"):
        return None

    split = urlsplit(raw_url)
    scheme = split.scheme.lower()
    if scheme in {"mailto", "tel", "javascript", "data"}:
        return None
    if scheme and scheme not in {"http", "https"}:
        return None
    if split.netloc and split.hostname != SITE_HOST:
        return None

    path = unquote(split.path)
    if not path:
        path = "/"

    if path.startswith("/"):
        normalized = posixpath.normpath(path).lstrip("/")
    else:
        normalized = posixpath.normpath((page_rel.parent / path).as_posix())

    if normalized in {"", "."}:
        return Path("index.html")
    if normalized == ".." or normalized.startswith("../"):
        return Path(normalized)

    candidate = Path(normalized)
    if path.endswith("/"):
        candidate = candidate / "index.html"
    elif not candidate.suffix and (ROOT / candidate).is_dir():
        candidate = candidate / "index.html"
    return candidate


def check_reference(page_rel: Path, raw_url: str, report: Report, label: str) -> None:
    target = local_target(page_rel, raw_url)
    if target is None:
        return
    if target.as_posix().startswith("../") or not (ROOT / target).exists():
        report.error(f"Broken internal {label}: {raw_url}", page_rel)


def check_html(report: Report) -> dict[Path, PageParser]:
    parsed: dict[Path, PageParser] = {}
    stylesheet_versions: dict[Path, str] = {}

    for path in all_html_files():
        rel = relative(path)
        parser = parse_page(path, report)
        if parser is None:
            continue
        parsed[rel] = parser

        if not parser.lang:
            report.error("Missing non-empty <html lang>.", rel)
        if not parser.title:
            report.error("Missing or empty <title>.", rel)

        seen_ids: set[str] = set()
        for element_id in parser.ids:
            if not element_id:
                report.error("Empty id attribute.", rel)
            elif element_id in seen_ids:
                report.error(f"Duplicate id: {element_id}", rel)
            seen_ids.add(element_id)

        for img in parser.images:
            if "alt" not in img:
                report.error(f"Image is missing alt attribute: {img.get('src', '<no src>')}", rel)

        for anchor in parser.anchors:
            if anchor.get("target", "").lower() == "_blank":
                rel_tokens = {token.lower() for token in anchor.get("rel", "").split()}
                if "noopener" not in rel_tokens:
                    report.error(
                        f"target=\"_blank\" link is missing rel=\"noopener\": {anchor.get('href', '')}",
                        rel,
                    )

        for field in parser.inputs:
            input_type = field.get("type", "text").lower()
            if input_type == "hidden":
                continue
            field_id = field.get("id", "")
            if not field_id:
                report.error("Non-hidden input is missing an id.", rel)
            elif (
                field_id not in parser.labels_for
                and not field.get("aria-label")
                and not field.get("aria-labelledby")
            ):
                report.error(f"Input #{field_id} has no associated label.", rel)
            if input_type == "email" and "required" not in field:
                report.error(f"Email input #{field_id or '<no id>'} should be required.", rel)

        for tag, attr, url in parser.references:
            if rel == TEMPLATE and "SLUG-DA-NOTA" in url:
                continue
            check_reference(rel, url, report, f"{tag} {attr}")

        for key in ("og:image",):
            value = parser.meta_properties.get(key)
            if value:
                check_reference(rel, value, report, key)
        for key in ("twitter:image",):
            value = parser.meta_names.get(key)
            if value:
                check_reference(rel, value, report, key)

        local_styles = [href for href in parser.stylesheets if urlsplit(href).path == "/assets/css/site.css"]
        if len(local_styles) != 1:
            report.error("Expected exactly one /assets/css/site.css stylesheet reference.", rel)
        else:
            version = parse_qs(urlsplit(local_styles[0]).query).get("v", [])
            if len(version) != 1 or not version[0]:
                report.error("site.css reference must include exactly one non-empty ?v= cache key.", rel)
            else:
                stylesheet_versions[rel] = version[0]

    if stylesheet_versions:
        unique_versions = sorted(set(stylesheet_versions.values()))
        if len(unique_versions) != 1:
            details = ", ".join(f"{path}={version}" for path, version in sorted(stylesheet_versions.items()))
            report.error(f"Mixed site.css cache versions: {details}")

    published = {relative(path) for path in published_html_files()}
    for rel in sorted(published):
        parser = parsed.get(rel)
        if parser is None:
            continue

        text = (ROOT / rel).read_text(encoding="utf-8")
        for placeholder in PLACEHOLDERS:
            if placeholder in text:
                report.error(f"Published page contains template placeholder: {placeholder}", rel)

        for name in sorted(REQUIRED_META_NAMES):
            if not parser.meta_names.get(name):
                report.error(f"Missing meta name=\"{name}\".", rel)
        for prop in sorted(REQUIRED_OG_PROPERTIES):
            if not parser.meta_properties.get(prop):
                report.error(f"Missing meta property=\"{prop}\".", rel)

        if len(parser.canonicals) != 1:
            report.error("Published page must have exactly one canonical URL.", rel)
        else:
            canonical = parser.canonicals[0]
            if canonical != expected_url(rel):
                report.error(
                    f"Canonical mismatch: expected {expected_url(rel)}, found {canonical}",
                    rel,
                )

        og_url = parser.meta_properties.get("og:url")
        if og_url and og_url != expected_url(rel):
            report.error(f"og:url mismatch: expected {expected_url(rel)}, found {og_url}", rel)

        if parser.rss_links != ["/feed.xml"]:
            report.error("Published page must expose one RSS alternate link to /feed.xml.", rel)

        if not parser.json_ld_blocks:
            report.error("Published page is missing JSON-LD.", rel)
        for index, block in enumerate(parser.json_ld_blocks, start=1):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                report.error(f"Invalid JSON-LD block {index}: {exc.msg} at line {exc.lineno}", rel)

    template = parsed.get(TEMPLATE)
    if template is None:
        report.error("Missing notes/_template.html.", TEMPLATE)
    elif "noindex" not in template.meta_names.get("robots", "").lower():
        report.error("Notes template must remain noindex.", TEMPLATE)

    not_found = parsed.get(NOT_FOUND)
    if not_found is None:
        report.error("Missing 404.html.", NOT_FOUND)
    elif "noindex" not in not_found.meta_names.get("robots", "").lower():
        report.error("404 page must remain noindex.", NOT_FOUND)

    report.passed("HTML structure, metadata, accessibility basics and internal references")
    report.passed("JSON-LD syntax and canonical/Open Graph URL consistency")
    report.passed("Single stylesheet cache version across all HTML files")
    return parsed


def check_sitemap(report: Report) -> None:
    path = ROOT / "sitemap.xml"
    try:
        tree = ET.parse(path)
    except (ET.ParseError, OSError) as exc:
        report.error(f"Invalid sitemap.xml: {exc}", Path("sitemap.xml"))
        return

    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    locs = [(node.text or "").strip() for node in tree.getroot().iter(namespace + "loc")]
    if len(locs) != len(set(locs)):
        report.error("sitemap.xml contains duplicate <loc> URLs.", Path("sitemap.xml"))

    expected = {expected_url(relative(path)) for path in published_html_files()}
    actual = set(locs)
    for url in sorted(expected - actual):
        report.error(f"Published page missing from sitemap: {url}", Path("sitemap.xml"))
    for url in sorted(actual - expected):
        report.error(f"Sitemap URL has no matching published HTML page: {url}", Path("sitemap.xml"))

    report.passed("sitemap.xml syntax and published-page coverage")


def check_feed(report: Report) -> None:
    path = ROOT / "feed.xml"
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        report.error(f"Invalid feed.xml: {exc}", Path("feed.xml"))
        return

    if root.tag != "rss":
        report.error("feed.xml root element must be <rss>.", Path("feed.xml"))
        return

    channel = root.find("channel")
    if channel is None:
        report.error("feed.xml is missing <channel>.", Path("feed.xml"))
        return
    if channel.find("lastBuildDate") is None:
        report.error("feed.xml is missing <lastBuildDate>.", Path("feed.xml"))

    links: list[str] = []
    for item in channel.findall("item"):
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or "").strip()
        title = (item.findtext("title") or "").strip()
        if not title:
            report.error("RSS item has an empty title.", Path("feed.xml"))
        if not link:
            report.error("RSS item has an empty link.", Path("feed.xml"))
            continue
        if guid != link:
            report.error(f"RSS guid must match link for {link}", Path("feed.xml"))
        links.append(link)
        target = local_target(Path("feed.xml"), link)
        if target is None or not (ROOT / target).exists():
            report.error(f"RSS item points to a missing page: {link}", Path("feed.xml"))

    if len(links) != len(set(links)):
        report.error("feed.xml contains duplicate item links.", Path("feed.xml"))

    note_articles = {
        expected_url(relative(path))
        for path in published_html_files()
        if relative(path).parts[:1] == ("notes",) and relative(path) != Path("notes/index.html")
    }
    actual_links = set(links)
    for url in sorted(note_articles - actual_links):
        report.error(f"Published written note missing from RSS: {url}", Path("feed.xml"))
    for url in sorted(actual_links - note_articles):
        report.error(f"RSS contains a non-note or unpublished URL: {url}", Path("feed.xml"))

    report.passed("feed.xml syntax and written-note policy")


def check_text_files(report: Report) -> None:
    llms_path = ROOT / "llms.txt"
    try:
        llms = llms_path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(f"Could not read llms.txt: {exc}", Path("llms.txt"))
    else:
        urls = re.findall(r"https://diogobronzesilva\.com/[^\s\]\)>]*", llms)
        for url in urls:
            cleaned = url.rstrip(".,;:")
            target = local_target(Path("llms.txt"), cleaned)
            if target is None or not (ROOT / target).exists():
                report.error(f"llms.txt points to a missing internal URL: {cleaned}", Path("llms.txt"))

    robots_path = ROOT / "robots.txt"
    try:
        robots = robots_path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(f"Could not read robots.txt: {exc}", Path("robots.txt"))
    else:
        expected_line = f"Sitemap: {SITE_ORIGIN}/sitemap.xml"
        if expected_line not in robots.splitlines():
            report.error(f"robots.txt must contain: {expected_line}", Path("robots.txt"))

    report.passed("llms.txt internal URLs and robots.txt sitemap declaration")


def main() -> int:
    report = Report()
    check_html(report)
    check_sitemap(report)
    check_feed(report)
    check_text_files(report)
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
