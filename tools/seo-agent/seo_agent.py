#!/usr/bin/env python3
"""
SEO / indexing diagnostic agent.

"Why isn't my site on Google?" is a chain of yes/no gates. The agent walks them
in order and stops at the first one that fails:

    reachable -> not blocked by robots.txt -> not noindex -> canonical points here
    -> in sitemap -> sitemap URL actually resolves -> content is in the HTML
    -> unique title/description -> internally linked

NOTE THE IMPORT BELOW: AgentLoop is unchanged from agent.py. Same five
ingredients, same control flow. Only the tool registry is different. That is
the lesson -- the loop is invariant, the tools are the product.

    python3 seo_agent.py --offline --local /home/user/vibesafe   # no key needed
    python3 seo_agent.py --local . --live https://www.vibesafe.info
"""
from __future__ import annotations

import argparse
import gzip
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request
import urllib.robotparser
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from agent import AgentLoop, Sandbox, Tool, ToolRegistry, _Block, _Resp  # the loop is reused as-is

UA_GOOGLEBOT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
TIMEOUT = 20

# --- HTML field extraction (regex is fine for static sites) ------------------

RX = {
    "title": re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S),
    "description": re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', re.I | re.S),
    "canonical": re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\'](.*?)["\']', re.I),
    "robots": re.compile(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'](.*?)["\']', re.I),
    "h1": re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S),
    "jsonld": re.compile(r'<script[^>]+application/ld\+json[^>]*>', re.I),
}
STRIP_TAGS = re.compile(r"<(script|style)[^>]*>.*?</\1>|<[^>]+>", re.I | re.S)


def seo_fields(html: str) -> dict[str, Any]:
    def one(key: str) -> str:
        m = RX[key].search(html)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    body_text = STRIP_TAGS.sub(" ", html)
    return {
        "title": one("title"),
        "description": one("description"),
        "canonical": one("canonical"),
        "meta_robots": one("robots"),
        "h1": [re.sub(r"\s+", " ", h).strip() for h in RX["h1"].findall(html)],
        "words": len(body_text.split()),
        "has_schema": bool(RX["jsonld"].search(html)),
    }


def verdict(fields: dict[str, Any], url: str = "") -> list[str]:
    """The gates, in the order Google applies them."""
    out = []
    mr = fields["meta_robots"].lower()
    if "noindex" in mr:
        out.append("BLOCKED: meta robots noindex -- this page will never rank")
    if not fields["title"]:
        out.append("ERROR: no <title>")
    elif len(fields["title"]) > 60:
        out.append(f"WARN: title {len(fields['title'])} chars (truncates in SERP ~60)")
    if not fields["description"]:
        out.append("WARN: no meta description (Google writes its own snippet)")
    elif len(fields["description"]) > 160:
        out.append(f"WARN: description {len(fields['description'])} chars (>160 truncates)")
    if not fields["h1"]:
        out.append("WARN: no <h1>")
    elif len(fields["h1"]) > 1:
        out.append(f"WARN: {len(fields['h1'])} <h1> tags")
    if fields["words"] < 150:
        out.append(f"WARN: only {fields['words']} words of text -- thin content")
    if url and fields["canonical"]:
        if fields["canonical"].rstrip("/") != url.rstrip("/"):
            out.append(f"NOTE: canonical points elsewhere -> {fields['canonical']}")
    return out or ["ok"]


# --- LIVE tools --------------------------------------------------------------

def _get(url: str, ua: str = UA_GOOGLEBOT) -> tuple[int, dict[str, str], str, list[str], float]:
    """Returns (status, headers, body, redirect_chain, ttfb)."""
    chain: list[str] = []

    class Tracker(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
            chain.append(f"{code} -> {newurl}")
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    opener = urllib.request.build_opener(Tracker)
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    t0 = time.time()
    try:
        with opener.open(req, timeout=TIMEOUT) as r:
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return r.status, dict(r.headers), raw.decode("utf-8", "replace"), chain, time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8", "replace"), chain, time.time() - t0


def build_live_tools(reg: ToolRegistry) -> None:
    def fetch_url(url: str) -> str:
        status, headers, body, chain, ttfb = _get(url)
        xr = headers.get("X-Robots-Tag", "")
        lines = [f"HTTP {status}  ttfb={ttfb:.2f}s  {len(body)}b  type={headers.get('Content-Type','?')}"]
        if chain:
            lines.append("redirects: " + " | ".join(chain))
        if xr:
            lines.append(f"X-Robots-Tag: {xr}" + ("   <-- BLOCKS INDEXING" if "noindex" in xr.lower() else ""))
        if status >= 400:
            lines.append(f"ERROR: Googlebot sees {status} -- cannot index")
        return "\n".join(lines)

    def check_robots(site_url: str, path: str = "/") -> str:
        base = re.match(r"(https?://[^/]+)", site_url).group(1)
        rp = urllib.robotparser.RobotFileParser()
        status, _, body, _, _ = _get(f"{base}/robots.txt")
        if status != 200:
            return f"robots.txt returned {status} (Google treats 4xx as allow-all, 5xx as disallow-all)"
        rp.parse(body.splitlines())
        allowed = rp.can_fetch("Googlebot", base + path)
        sitemaps = re.findall(r"(?im)^\s*Sitemap:\s*(\S+)", body)
        return (f"robots.txt OK\nGooglebot may crawl {path}: {allowed}"
                + ("" if allowed else "   <-- BLOCKED, this is why it is not indexed")
                + f"\nsitemaps declared: {sitemaps or 'NONE -- add one'}\n---\n{body[:600]}")

    def page_seo(url: str) -> str:
        status, headers, body, chain, _ = _get(url)
        if status != 200:
            return f"HTTP {status} -- no SEO data"
        f = seo_fields(body)
        lines = [f"title: {f['title']!r}", f"description: {f['description'][:110]!r}",
                 f"canonical: {f['canonical'] or '(none)'}", f"meta robots: {f['meta_robots'] or '(none)'}",
                 f"h1: {f['h1'] or '(none)'}", f"words: {f['words']}  schema: {f['has_schema']}"]
        if headers.get("X-Robots-Tag"):
            lines.append(f"X-Robots-Tag: {headers['X-Robots-Tag']}")
        return "\n".join(lines) + "\n\nverdict:\n  " + "\n  ".join(verdict(f, url))

    def sitemap_audit(sitemap_url: str, sample: int = 15) -> str:
        status, _, body, _, _ = _get(sitemap_url)
        if status != 200:
            return f"sitemap returned {status} -- Search Console will report 'Couldn't fetch'"
        try:
            root = ElementTree.fromstring(body)
        except ElementTree.ParseError as e:
            return f"sitemap is not valid XML: {e}"
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locs = [e.text.strip() for e in root.iter(f"{ns}loc") if e.text]
        out = [f"{len(locs)} URLs in sitemap; checking first {min(sample, len(locs))}"]
        for loc in locs[:sample]:
            st, hd, bd, ch, _ = _get(loc)
            note = ""
            if st != 200:
                note = f"   <-- {st} IN SITEMAP = Search Console error"
            elif "noindex" in (seo_fields(bd)["meta_robots"] + hd.get("X-Robots-Tag", "")).lower():
                note = "   <-- noindex page submitted in sitemap = conflict"
            elif ch:
                note = f"   <-- redirects ({len(ch)} hops)"
            out.append(f"  {st} {loc}{note}")
        return "\n".join(out)

    reg.register(Tool("fetch_url", "Fetch a URL as Googlebot. Shows status, redirect chain, X-Robots-Tag, TTFB.",
                      {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}, fetch_url))
    reg.register(Tool("check_robots", "Fetch robots.txt and test whether Googlebot may crawl a path.",
                      {"type": "object", "properties": {"site_url": {"type": "string"}, "path": {"type": "string"}},
                       "required": ["site_url"]}, check_robots))
    reg.register(Tool("page_seo", "Extract title, description, canonical, meta robots, h1, word count from a live URL.",
                      {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}, page_seo))
    reg.register(Tool("sitemap_audit", "Fetch a sitemap and check that its URLs actually return 200 and are indexable.",
                      {"type": "object", "properties": {"sitemap_url": {"type": "string"},
                                                        "sample": {"type": "integer"}},
                       "required": ["sitemap_url"]}, sitemap_audit))


# --- LOCAL tools (work with no network) -------------------------------------

SKIP = {".git", "node_modules", "dist", "build", "drafts", "__pycache__"}


def build_local_tools(reg: ToolRegistry, sandbox: Sandbox) -> None:
    def _pages() -> dict[str, dict[str, Any]]:
        # rglob, not glob: subdirectories (blog/, docs/) hold real pages too.
        # Keys are paths relative to the root, so 'blog/post.html' matches the
        # slug a clean URL like /blog/post resolves to.
        return {str(p.relative_to(sandbox.root)): seo_fields(p.read_text(errors="replace"))
                for p in sorted(sandbox.root.rglob("*.html"))
                if not any(part in SKIP for part in p.parts)}

    def audit_pages() -> str:
        rows = []
        for name, f in _pages().items():
            v = verdict(f)
            if v != ["ok"]:
                rows.append(f"{name}\n    " + "\n    ".join(v))
        return "\n".join(rows) if rows else "all pages pass the per-page checks"

    def find_duplicates() -> str:
        titles: dict[str, list[str]] = {}
        descs: dict[str, list[str]] = {}
        for name, f in _pages().items():
            if "noindex" in f["meta_robots"].lower():
                continue
            if f["title"]:
                titles.setdefault(f["title"], []).append(name)
            if f["description"]:
                descs.setdefault(f["description"], []).append(name)
        out = []
        for label, table in (("title", titles), ("description", descs)):
            for value, pages in table.items():
                if len(pages) > 1:
                    out.append(f"duplicate {label} on {len(pages)} pages: {pages}\n    {value[:100]!r}")
        return "\n".join(out) if out else "no duplicate titles or descriptions among indexable pages"

    # A sitemap URL is not a file path. Before claiming a page is missing or
    # noindex, resolve the URL the way the HOST resolves it. Three layers, in
    # priority order: an explicit server route, a static-host rewrite, then the
    # plain file guess. Skipping the first layer is what produced a false
    # "HARD BLOCKER" on a site whose Express app serves a different file at /.
    # The gap between the path and sendFile is "tempered": it may not contain
    # another app.get/app.all, or the match bridges two separate routes and
    # pairs the wrong file with the wrong URL.
    ROOT_ROUTE = re.compile(
        r"""app\.(?:get|all)\(\s*["']([^"']+)["']"""
        r"""(?:(?!app\.(?:get|all)\()[\s\S]){0,300}?"""
        r"""sendFile\([^)]*?["']([\w./-]+\.html)["']"""
    )

    def _server_routes() -> tuple[dict[str, str], bool]:
        """(slug -> html file, server_detected). A detected server means file
        layout alone cannot prove what a URL serves."""
        routes: dict[str, str] = {}
        detected = False
        for base in (sandbox.root, sandbox.root.parent):
            for pattern in ("*.js", "lib/*.js", "api/*.js", "src/*.js", "server/*.js"):
                for js in base.glob(pattern):
                    try:
                        text = js.read_text(errors="replace")
                    except OSError:
                        continue
                    if "express.static" in text or "app.get(" in text:
                        detected = True
                    for m in ROOT_ROUTE.finditer(text):
                        routes[m.group(1).strip("/")] = m.group(2).lstrip("./")
        return routes, detected

    def _rewrites() -> dict[str, str]:
        """Exact-match rewrites from vercel.json, so '/' -> '/landing.html' is
        understood. A sitemap audit that ignores routing reports blockers the
        host has already solved."""
        import json
        for cfg in (sandbox.root / "vercel.json", sandbox.root.parent / "vercel.json"):
            if not cfg.is_file():
                continue
            try:
                data = json.loads(cfg.read_text())
            except json.JSONDecodeError:
                return {}
            return {r["source"].strip("/"): r["destination"].strip("/")
                    for r in data.get("rewrites", [])
                    if "source" in r and "destination" in r and "(" not in r["source"]}
        return {}

    def audit_sitemap(sitemap: str = "") -> str:
        files = sorted(sandbox.root.glob("sitemap*.xml"))
        path = sandbox.resolve(sitemap) if sitemap else (files[0] if files else None)
        if path is None:
            return "NO SITEMAP FILE FOUND -- Google has no URL list to crawl"
        root = ElementTree.fromstring(path.read_text())
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locs = [e.text.strip() for e in root.iter(f"{ns}loc") if e.text]
        pages = _pages()
        rewrites = _rewrites()
        routes, server = _server_routes()
        problems, listed = [], set()
        for loc in locs:
            slug = re.sub(r"^https?://[^/]+/?", "", loc).strip("/")
            routed = slug in routes or slug in rewrites
            slug = routes.get(slug) or rewrites.get(slug, slug)
            # A sitemap URL may be a clean URL (/how-it-works), an explicit file
            # (/how-it-works.html), or a directory (/blog/). Try each shape --
            # guessing only one is how this tool produced 21 false positives.
            candidates = ["index.html"] if slug == "" else [
                slug if slug.endswith(".html") else f"{slug}.html",
                f"{slug}/index.html",
            ]
            hit = next((c for c in candidates if c in pages), None)
            listed.update(candidates)
            # Only assert a blocker when we know what the URL serves. With a
            # server present and no route we could read, the file guess is a
            # guess -- say so and name the check instead of crying wolf.
            unproven = server and not routed
            if hit is None:
                problems.append(
                    f"  {'UNVERIFIED' if unproven else '404 RISK'}: {loc} -> no file matching {candidates}"
                    + ("; a server routes this host, so check with:"
                       f" curl -sI {loc}" if unproven else ""))
            elif "noindex" in pages[hit]["meta_robots"].lower():
                if unproven:
                    problems.append(
                        f"  UNVERIFIED: {loc} would map to {hit}, which is noindex -- but a server "
                        f"routes this host, so it may serve something else. Confirm with:"
                        f" curl -s {loc} | grep -i robots")
                else:
                    problems.append(f"  HARD BLOCKER: {loc} is in the sitemap but {hit} is noindex "
                                    f"-- Search Console reports \"Submitted URL marked 'noindex'\"")
        orphans = [n for n, f in pages.items()
                   if n not in listed and "noindex" not in f["meta_robots"].lower()]
        out = [f"sitemap {path.name}: {len(locs)} URLs, {len(pages)} html files on disk"]
        out += problems or ["  every sitemap URL maps to a real file, none are noindex"]
        if orphans:
            out.append(f"  NOT IN SITEMAP ({len(orphans)} indexable pages Google may never find):")
            out += [f"    {o}" for o in sorted(orphans)]
        return "\n".join(out)

    def read_robots() -> str:
        p = sandbox.root / "robots.txt"
        if not p.exists():
            return "no robots.txt (Google allows everything -- not fatal, but no sitemap hint either)"
        body = p.read_text()
        sm = re.findall(r"(?im)^\s*Sitemap:\s*(\S+)", body)
        dis = re.findall(r"(?im)^\s*Disallow:\s*(\S*)", body)
        return (f"{body}\n---\nsitemaps declared: {sm or 'NONE'}\n"
                f"disallow rules: {[d for d in dis if d] or 'none'}")

    reg.register(Tool("audit_pages", "Check every local HTML page for title/description/h1/noindex/thin-content problems.",
                      {"type": "object", "properties": {}, "required": []}, audit_pages))
    reg.register(Tool("find_duplicates", "Find duplicate titles or meta descriptions across indexable pages.",
                      {"type": "object", "properties": {}, "required": []}, find_duplicates))
    reg.register(Tool("audit_sitemap", "Cross-check the sitemap against files on disk: 404 risks, noindex conflicts, orphan pages.",
                      {"type": "object", "properties": {"sitemap": {"type": "string"}}, "required": []}, audit_sitemap))
    reg.register(Tool("read_robots", "Read robots.txt and report Disallow rules and declared sitemaps.",
                      {"type": "object", "properties": {}, "required": []}, read_robots))


SYSTEM = """You are an SEO indexing diagnostician. The user's site is not showing
up on Google. Work the gates in order and stop at the first hard blocker:

1. CRAWLABLE  - does the URL return 200 to Googlebot? robots.txt allow it?
2. INDEXABLE  - meta robots / X-Robots-Tag noindex? canonical pointing away?
3. DISCOVERABLE - in the sitemap? sitemap declared in robots.txt? internally linked?
4. QUALITY    - unique title and description, real h1, enough content?

Distinguish hard blockers (noindex, robots Disallow, 404, canonical to another
URL) from soft issues (long title, thin content). A hard blocker means the page
CANNOT rank. A soft issue means it ranks worse.

Two things you must say plainly if they apply:
- A brand-new domain simply takes days to weeks to get indexed. No amount of
  technical fixing makes that faster; Search Console URL Inspection is the fix.
- Being indexed and ranking are different. "Not in Google at all" and "on page
  4" have completely different causes. Say which one the evidence supports.

Report findings with the specific file or URL. Do not invent problems."""


# --- offline scripted model --------------------------------------------------

class OfflineSEOModel:
    def __init__(self) -> None:
        self.step = 0
        self._m = type("M", (), {"create": self._create})()

    @property
    def messages(self):
        return self._m

    def _create(self, **kw: Any) -> _Resp:
        self.step += 1
        have = {t["name"] for t in kw["tools"]}
        plan = [("read_robots", {}), ("audit_sitemap", {}), ("audit_pages", {}), ("find_duplicates", {})]
        for i, (name, args) in enumerate(plan, 1):
            if self.step == i and name in have:
                return _Resp([_Block(type="tool_use", id=f"t{i}", name=name, input=args)], "tool_use")
        return _Resp([_Block(type="text", text="Gate walk complete -- see findings above.")], "end_turn")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", help="path to the static site directory")
    ap.add_argument("--live", help="https://your-site.com to check over the network")
    ap.add_argument("--offline", action="store_true", help="scripted model, no API key")
    args = ap.parse_args()

    if not args.local and not args.live:
        ap.error("give --local <dir> and/or --live <url>")

    reg = ToolRegistry()
    if args.local:
        build_local_tools(reg, Sandbox(Path(args.local)))
    if args.live:
        build_live_tools(reg)

    if args.offline:
        client: Any = OfflineSEOModel()
    elif not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set; use --offline", file=sys.stderr)
        return 1
    else:
        import anthropic
        client = anthropic.Anthropic()

    target = args.live or args.local
    print(f"\033[1mdiagnosing {target}\033[0m")
    print(f"tools: {sorted(t['name'] for t in reg.specs())}\n")

    loop = AgentLoop(client=client, tools=reg, confirm=False)
    loop.run.__globals__["SYSTEM"] = SYSTEM  # reuse the loop, swap the brief
    answer = loop.run(
        f"My site {target} is not appearing on Google. Diagnose it: work the "
        f"crawl -> index -> discover -> quality gates and tell me what is blocking it."
    )
    print(f"\n\033[1m{answer}\033[0m")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
