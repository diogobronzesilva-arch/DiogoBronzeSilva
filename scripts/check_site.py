#!/usr/bin/env python3
"""Static consistency checks for diogobronzesilva.com.

The checker intentionally uses only Python's standard library so the GitHub
Action stays small, deterministic and dependency-free.
"""

from __future__ import annotations

from datetime import datetime
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
    "Title of the note",
    "ONE SENTENCE ABOUT THIS NOTE",
    "One line that states the argument.",
    "SLUG-DA-NOTA",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.title_parts: list[str] = []
        self.in_title = False
        self.h1_count = 0
        self.has_video_player = False
        self.body_text_parts: list[str] = []
        self._in_body = False
        self._ignore_body_text = False
        self._hidden_elements: list[str] = []
        self.meta_names: dict[str, str] = {}
        self.meta_properties: dict[str, str] = {}
        self.duplicate_meta_names: list[str] = []
        self.duplicate_meta_properties: list[str] = []
        self.canonicals: list[str] = []
        self.references: list[tuple[str, str, str]] = []
        self.images: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.executable_scripts: list[dict[str, str]] = []
        self.unprotected_mailtos: list[str] = []
        self._email_off = False
        self.navigation_links: list[str] = []
        self._in_navigation = False
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
        if tag == "body":
            self._in_body = True
        if tag in {"script", "style"}:
            self._ignore_body_text = True
        # Closed details remain reader-accessible; hidden/template content does not.
        void_tags = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
        hidden_style = re.search(r"(?:^|;)\s*(?:display\s*:\s*none|visibility\s*:\s*hidden)\b", data.get("style", ""), re.I)
        if self._in_body and tag not in void_tags and (
            self._hidden_elements or "hidden" in data or hidden_style or tag == "template"
        ):
            self._hidden_elements.append(tag)
        if tag == "video" or (tag == "iframe" and data.get("src")):
            self.has_video_player = True
        if tag == "h1":
            self.h1_count += 1

        if tag == "html" and self.lang is None:
            self.lang = data.get("lang", "").strip()
        if tag == "title":
            self.in_title = True
        if "id" in data:
            self.ids.append(data["id"])

        if tag == "meta":
            content = data.get("content", "").strip()
            if data.get("name"):
                meta_name = data["name"].lower()
                if meta_name in self.meta_names:
                    self.duplicate_meta_names.append(meta_name)
                self.meta_names[meta_name] = content
            if data.get("property"):
                meta_prop = data["property"].lower()
                if meta_prop in self.meta_properties:
                    self.duplicate_meta_properties.append(meta_prop)
                self.meta_properties[meta_prop] = content

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

        if tag == "nav" and "nav" in data.get("class", "").split():
            self._in_navigation = True
        if tag == "script" and data.get("type", "").lower() not in {"application/ld+json", "application/json"}:
            self.executable_scripts.append(data)
        if tag == "a":
            self.anchors.append(data)
            if data.get("href", "").lower().startswith("mailto:") and not self._email_off:
                self.unprotected_mailtos.append(data["href"])
            if self._in_navigation:
                self.navigation_links.append(data.get("href", ""))
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
        if tag in self._hidden_elements:
            last = len(self._hidden_elements) - 1 - self._hidden_elements[::-1].index(tag)
            del self._hidden_elements[last:]
        if tag == "body":
            self._in_body = False
        if tag in {"script", "style"}:
            self._ignore_body_text = False
        if tag == "nav":
            self._in_navigation = False
        if tag == "title":
            self.in_title = False
        if tag == "script" and self._json_ld_buffer is not None:
            self.json_ld_blocks.append("".join(self._json_ld_buffer).strip())
            self._json_ld_buffer = None

    def handle_comment(self, data: str) -> None:
        if data.strip() == "email_off":
            self._email_off = True
        elif data.strip() == "/email_off":
            self._email_off = False

    def handle_data(self, data: str) -> None:
        if self._in_body and not self._ignore_body_text and not self._hidden_elements:
            self.body_text_parts.append(data)
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
        if any(part in {".git", "dist"} for part in rel.parts) or rel in {TEMPLATE, NOT_FOUND}:
            continue
        files.append(path)
    return sorted(files)


def all_html_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if not any(part in {".git", "dist"} for part in relative(path).parts)
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


def check_page_shell(report: Report, rel: Path, parser: PageParser) -> None:
    """Keep the shared shell usable and isolate the demonstration script."""
    if not any(a.get("href") == "#main" and "skip" in a.get("class", "").split() for a in parser.anchors):
        report.error("Missing styled skip link to #main.", rel)
    if not any(a.get("href") == "/" and "wordmark" in a.get("class", "").split() for a in parser.anchors):
        report.error("Missing shared wordmark link to Home.", rel)
    for href in parser.unprotected_mailtos:
        report.error(f"Unprotected mailto link: {href}; use Cloudflare email_off markers.", rel)

    scripts = parser.executable_scripts
    if rel == Path("vitachart/index.html"):
        expected = "/assets/js/vitachart-demo.js"
        source = urlsplit(scripts[0].get("src", "")) if scripts else None
        if len(scripts) != 1 or source is None or source.scheme or source.netloc or source.path != expected or "defer" not in scripts[0]:
            report.error("VitaChart demonstration must load only its deferred local script.", rel)
    elif scripts:
        report.error("Executable JavaScript is limited to the VitaChart demonstration.", rel)


def check_html(report: Report) -> dict[Path, PageParser]:
    parsed: dict[Path, PageParser] = {}
    stylesheet_versions: dict[Path, str] = {}

    for path in all_html_files():
        rel = relative(path)
        parser = parse_page(path, report)
        if parser is None:
            continue
        parsed[rel] = parser
        check_page_shell(report, rel, parser)

        expected_navigation = ["/", "/work/", "/projects/", "https://bronzeart.pt", "/notes/", "/contact/"]
        if parser.navigation_links != expected_navigation:
            report.error("Global navigation must include Home, Work, Projects, Photography, Notes and Contact in order.", rel)

        if not parser.lang:
            report.error("Missing non-empty <html lang>.", rel)
        if not parser.title:
            report.error("Missing or empty <title>.", rel)
        for dup_name in parser.duplicate_meta_names:
            report.error(f"Duplicate <meta name=\"{dup_name}\">.", rel)
        for dup_prop in parser.duplicate_meta_properties:
            report.error(f"Duplicate <meta property=\"{dup_prop}\">.", rel)

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

    for i, link in enumerate(links):
        target = local_target(Path("feed.xml"), link)
        if target is None or not (ROOT / target).exists():
            continue
        try:
            page_html = (ROOT / target).read_text(encoding="utf-8")
        except OSError as exc:
            report.error(f"Could not read note HTML: {exc}", target)
            continue

        footer_match = re.search(r'<footer class="article__foot[^"]*">(.*?)</footer>', page_html, re.DOTALL)
        if not footer_match:
            report.error("Note article is missing an article__foot navigation footer.", target)
            continue
        footer_content = footer_match.group(1)

        if i > 0:
            newer_slug = links[i - 1].rstrip("/").split("/")[-1]
            if f"/notes/{newer_slug}/" not in footer_content:
                report.error(
                    f"Note navigation footer missing link to newer article: /notes/{newer_slug}/",
                    target,
                )
        elif "&larr;" in footer_content or "Mais recente" in footer_content or "Newer" in footer_content:
            report.error("Most recent note should not have a link to a newer note.", target)

        if i < len(links) - 1:
            older_slug = links[i + 1].rstrip("/").split("/")[-1]
            if f"/notes/{older_slug}/" not in footer_content:
                report.error(
                    f"Note navigation footer missing link to older article: /notes/{older_slug}/",
                    target,
                )
        elif "&rarr;" in footer_content or "Mais antigo" in footer_content or "Older" in footer_content:
            report.error("Oldest note should not have a link to an older note.", target)

    expected_paths = [urlsplit(link).path for link in links]

    home_path = ROOT / "index.html"
    if home_path.is_file() and expected_paths:
        home_html = home_path.read_text(encoding="utf-8")
        home_entries = re.findall(
            r'<a\s+class="([^"]*\bentry\b[^"]*)"\s+href="(/notes/[^"]+)"',
            home_html,
        )
        home_note_paths = [href for _, href in home_entries]
        if home_note_paths != expected_paths[:3]:
            report.error(
                f"Home Latest Notes must match the 3 most recent RSS notes {expected_paths[:3]}, found {home_note_paths}",
                Path("index.html"),
            )
        home_featured = [href for cls, href in home_entries if "entry--featured" in cls.split()]
        if home_featured != expected_paths[:1]:
            report.error(
                f"Home must mark only the newest note ({expected_paths[0]}) as entry--featured.",
                Path("index.html"),
            )

    notes_index_path = ROOT / "notes/index.html"
    if notes_index_path.is_file() and expected_paths:
        notes_html = notes_index_path.read_text(encoding="utf-8")
        index_entries = re.findall(
            r'<a\s+class="([^"]*\bentry\b[^"]*)"\s+href="(/notes/[^"]+)"',
            notes_html,
        )
        index_note_paths = [href for _, href in index_entries]
        if index_note_paths != expected_paths:
            report.error(
                "notes/index.html written notes order/completeness does not match feed.xml.",
                Path("notes/index.html"),
            )
        index_featured = [href for cls, href in index_entries if "entry--featured" in cls.split()]
        if index_featured != expected_paths[:1]:
            report.error(
                f"notes/index.html must mark only the newest note ({expected_paths[0]}) as entry--featured.",
                Path("notes/index.html"),
            )

    report.passed("feed.xml syntax, written-note policy, Home/Notes index parity and bidirectional article navigation")


def check_text_files(report: Report) -> None:
    published_pages = {expected_url(relative(path)) for path in published_html_files()}

    for doc_name in ("llms.txt", "llms-full.txt"):
        doc_path = ROOT / doc_name
        try:
            content = doc_path.read_text(encoding="utf-8")
        except OSError as exc:
            report.error(f"Could not read {doc_name}: {exc}", Path(doc_name))
            continue

        urls = re.findall(r"https://diogobronzesilva\.com/[^\s\]\)>]*", content)
        cleaned_urls: set[str] = set()
        for url in urls:
            cleaned = url.rstrip(".,;:")
            cleaned_urls.add(cleaned)
            target = local_target(Path(doc_name), cleaned)
            if target is None or not (ROOT / target).exists():
                report.error(f"{doc_name} points to a missing internal URL: {cleaned}", Path(doc_name))

        for page_url in sorted(published_pages - cleaned_urls):
            report.error(f"Published page missing from {doc_name}: {page_url}", Path(doc_name))

    robots_path = ROOT / "robots.txt"
    try:
        robots = robots_path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error(f"Could not read robots.txt: {exc}", Path("robots.txt"))
    else:
        expected_line = f"Sitemap: {SITE_ORIGIN}/sitemap.xml"
        if expected_line not in robots.splitlines():
            report.error(f"robots.txt must contain: {expected_line}", Path("robots.txt"))
        if "README.md" in robots:
            report.error("robots.txt should not reference legacy /README.md Disallow rule.", Path("robots.txt"))

    report.passed("llms.txt, llms-full.txt internal URLs/published-page coverage and robots.txt sitemap declaration")


def check_cloudflare_infrastructure(report: Report) -> None:
    for legacy_file in (".htaccess", "_redirects"):
        if (ROOT / legacy_file).exists():
            report.error(f"Legacy {legacy_file} file should not exist in the repository.", Path(legacy_file))

    headers_path = ROOT / "_headers"
    if not headers_path.exists():
        report.error("Missing Cloudflare Pages _headers file.", Path("_headers"))
    else:
        try:
            headers_content = headers_path.read_text(encoding="utf-8")
        except OSError as exc:
            report.error(f"Could not read _headers: {exc}", Path("_headers"))
        else:
            required_security_headers = [
                "Strict-Transport-Security",
                "X-Content-Type-Options: nosniff",
                "X-Frame-Options: SAMEORIGIN",
                "Referrer-Policy: strict-origin-when-cross-origin",
                "Permissions-Policy",
            ]
            for header in required_security_headers:
                if header not in headers_content:
                    report.error(f"_headers is missing required security directive: {header}", Path("_headers"))

            if not re.search(
                r"Cache-Control:\s*public,\s*max-age=0,\s*must-revalidate",
                headers_content,
                re.IGNORECASE,
            ):
                report.error(
                    "_headers must keep HTML and unversioned files revalidatable.",
                    Path("_headers"),
                )

            for asset_rule in ("/assets/fonts/*", "/assets/css/*", "/assets/img/*"):
                if asset_rule not in headers_content:
                    report.error(
                        f"_headers must include an explicit cache policy for {asset_rule}.",
                        Path("_headers"),
                    )

    css_path = ROOT / "assets/css/site.css"
    if css_path.is_file():
        css_text = css_path.read_text(encoding="utf-8")
        font_urls = re.findall(r"url\(['\"](/assets/fonts/[^'\"]+)['\"]\)", css_text)
        if not font_urls:
            report.error("site.css does not declare any self-hosted /assets/fonts/ @font-face URLs.", Path("assets/css/site.css"))
        for font_url in font_urls:
            if not (ROOT / font_url.lstrip("/")).is_file():
                report.error(f"Missing self-hosted font file referenced in site.css: {font_url}", Path("assets/css/site.css"))

    mailto_pattern = re.compile(
        r"<!--email_off-->\s*<a\b[^>]*href=\"mailto:hello@diogobronzesilva\.com\"[^>]*>.*?</a>\s*<!--/email_off-->",
        re.DOTALL,
    )
    for page in (Path("contact/index.html"), Path("work/index.html")):
        try:
            content = (ROOT / page).read_text(encoding="utf-8")
        except OSError as exc:
            report.error(f"Could not read {page}: {exc}", page)
        else:
            if not mailto_pattern.search(content):
                report.error(
                    "Public mailto link must be wrapped in Cloudflare email_off markers to remain usable without JavaScript.",
                    page,
                )

    report.passed("Cloudflare Pages infrastructure (_headers, font caching and mailto safeguards)")


def as_list(value: object) -> list:
    return value if isinstance(value, list) else ([] if value is None else [value])


def structured_nodes(value: object):
    """Visit JSON-LD objects, including arrays, graphs and nested entities."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from structured_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from structured_nodes(child)


def readable_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    parser = PageParser()
    parser.feed("<body>" + value + "</body>")
    return " ".join(" ".join(parser.body_text_parts).split()).casefold()


def check_discovery(report: Report, parsed: dict[Path, PageParser]) -> None:
    """Check search-facing consistency and crawlable in-page navigation."""
    def normal(value: str) -> str:
        return " ".join(value.split()).casefold()

    titles: dict[str, Path] = {}
    descriptions: dict[str, Path] = {}
    for rel, parser in parsed.items():
        if rel in {TEMPLATE, NOT_FOUND}:
            continue
        if parser.h1_count != 1:
            report.error(f"Published page must have one H1, found {parser.h1_count}.", rel)
        robots = parser.meta_names.get("robots", "").lower()
        if "noindex" in robots or "none" in {x.strip() for x in robots.split(",")}:
            report.error("Published page must remain indexable.", rel)
        for value, seen, label in ((parser.title, titles, "title"), (parser.meta_names.get("description", ""), descriptions, "description")):
            key = normal(value)
            if key and key in seen:
                report.error(f"Duplicate published {label}; also used by {seen[key]}.", rel)
            elif key:
                seen[key] = rel

        locale = parser.meta_properties.get("og:locale", "")
        if not locale or locale.split("_")[0] != (parser.lang or "").split("-")[0]:
            report.error("Open Graph locale must match the page language.", rel)
        visible = normal(" ".join(parser.body_text_parts))
        for block in parser.json_ld_blocks:
            try:
                data = json.loads(block)
            except json.JSONDecodeError:
                continue  # check_html reports the syntax error.
            for node in structured_nodes(data):
                types = as_list(node.get("@type"))
                if "FAQPage" in types:
                    questions = as_list(node.get("mainEntity"))
                    if not questions:
                        report.error("Structured FAQ must contain questions and answers.", rel)
                    for question in questions:
                        if not isinstance(question, dict):
                            report.error("Structured FAQ question must be an object.", rel)
                            continue
                        name = readable_text(question.get("name"))
                        answers = as_list(question.get("acceptedAnswer"))
                        if not name or not answers or name not in visible:
                            report.error("Structured FAQ questions and answers must match visible page content.", rel)
                        for answer in answers:
                            value = readable_text(answer.get("text")) if isinstance(answer, dict) else ""
                            if not value or value not in visible:
                                report.error("Structured FAQ questions and answers must match visible page content.", rel)
                if "VideoObject" in types:
                    for field in ("name", "thumbnailUrl", "uploadDate"):
                        if not node.get(field):
                            report.error(f"VideoObject is missing required field {field}.", rel)
                    upload_date = node.get("uploadDate")
                    if upload_date:
                        try:
                            stamp = datetime.fromisoformat(upload_date.replace("Z", "+00:00"))
                            if "T" not in upload_date or stamp.tzinfo is None:
                                raise ValueError("Time and timezone required")
                        except (ValueError, TypeError, AttributeError):
                            report.error("VideoObject uploadDate must include a valid time and timezone.", rel)
                    if not parser.has_video_player:
                        report.error("VideoObject requires a playable video on the page; use CreativeWork for external interview links.", rel)

    for rel, parser in parsed.items():
        for anchor in parser.anchors:
            raw = anchor.get("href", "")
            split = urlsplit(raw)
            if not split.fragment or split.scheme not in {"", "http", "https"}:
                continue
            if split.netloc and split.hostname != SITE_HOST:
                continue
            if rel == TEMPLATE and "SLUG-DA-NOTA" in raw:
                continue
            fragment = unquote(split.fragment.split(":~:text=", 1)[0])
            if not fragment:
                continue
            target = rel if not split.path and not split.netloc else local_target(rel, raw)
            target_parser = parsed.get(target) if target is not None else None
            if target_parser is not None and fragment not in target_parser.ids:
                report.error(f"Broken internal fragment: {raw}", rel)
    report.passed("Unique search metadata, indexability, language, visible FAQ consistency, video markup and internal fragments")


def main() -> int:
    report = Report()
    parsed = check_html(report)
    check_discovery(report, parsed)
    check_sitemap(report)
    check_feed(report)
    check_text_files(report)
    check_cloudflare_infrastructure(report)
    return report.finish()


if __name__ == "__main__":
    sys.exit(main())
