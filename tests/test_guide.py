#!/usr/bin/env python3
"""Test suite for the Docker plain-English guide.

Verifies:
  1. The build script runs and produces the expected HTML pages.
  2. Generated HTML has nav, copy buttons on every code block, and credits.
  3. Internal links in the site resolve.
  4. Every bash code block in docs/ is syntactically valid (bash -n).
  5. Every docker command documented is a real Docker command.
  6. Every yaml code block parses, and compose examples are well-shaped
     (ports numeric, volumes numeric-and-declared, services have images).
  7. No secrets or accidental oddities in the docs.

Run:  python3 -m pytest tests/ -q      (or make test)
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT))

import build  # noqa: E402

CODE_BLOCK = re.compile(r"^```(\w*)\s*$\n(.*?)^```", re.M | re.S)


def md_blocks(md: str):
    return [(m.group(1), m.group(2)) for m in CODE_BLOCK.finditer(md)]


def all_docs():
    paths = sorted(DOCS.glob("*.md"))
    assert paths, "no docs found"
    return paths


# ---------------------------------------------------------------- build

def test_build_runs_and_creates_pages():
    outs = build.build()
    assert len(outs) == len(build.PAGES)
    for out in outs:
        p = build.SITE / out
        assert p.exists(), f"missing {p}"
        assert p.read_text(encoding="utf-8").startswith("<!DOCTYPE html>")


def test_html_pages_have_nav_copy_and_footer():
    build.build()
    for out in build.build():
        page = (build.SITE / out).read_text(encoding="utf-8")
        assert '<nav class="chapters">' in page
        assert "Asdale Dynamics, LLC" in page
        n_copy = page.count('class="copy"')
        n_code = page.count('<div class="code">')
        assert n_copy == n_code, f"{out}: {n_copy} buttons vs {n_code} code blocks"


def test_html_internal_links_resolve():
    build.build()
    names = {p.name for p in build.SITE.glob("*.html")}
    for page in build.SITE.glob("*.html"):
        text = page.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"#]+)"', text):
            if href.startswith("http"):
                assert href.startswith("https://") or href == "http://localhost:3000", href
            else:
                assert href in names, f"{page.name} links to missing {href}"


# ------------------------------------------------- bash command blocks

DOC_HEADS = (
    "docker --version",
    "docker run",
    "docker ps",
    "docker stop",
    "docker start",
    "docker rm",
    "docker rmi",
    "docker exec",
    "docker logs",
    "docker image",
    "docker container",
    "docker volume",
    "docker network",
    "docker system",
    "docker compose",
)


@pytest.mark.parametrize("md_path", all_docs(), ids=lambda p: p.name)
def test_bash_blocks_are_valid_shell(md_path):
    md = md_path.read_text(encoding="utf-8")
    bad = []
    for lang, code in md_blocks(md):
        if lang != "bash":
            continue
        r = subprocess.run(["bash", "-n"], input=code, text=True, capture_output=True)
        if r.returncode != 0:
            bad.append((code, r.stderr.strip()))
    assert not bad, f"{md_path.name}: invalid bash blocks:\n{bad}"


def test_docker_commands_are_real():
    problems = []
    for md in all_docs():
        text = md.read_text(encoding="utf-8")
        for lang, code in md_blocks(text):
            if lang != "bash":
                continue
            for line in code.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                words = line.split()
                if words[0] != "docker":
                    continue
                args = " ".join(words[1:])
                matched = False
                for head in DOC_HEADS:
                    suffix = head[len("docker"):].strip()
                    if args == suffix or (suffix and args.startswith(suffix + " ")):
                        matched = True
                        break
                if not matched:
                    problems.append((md.name, line))
    assert not problems, f"unrecognized docker commands: {problems}"


# ------------------------------------------------- yaml blocks

@pytest.mark.parametrize("md_path", all_docs(), ids=lambda p: p.name)
def test_yaml_blocks_parse(md_path):
    md = md_path.read_text(encoding="utf-8")
    bad = []
    for lang, code in md_blocks(md):
        if lang != "yaml":
            continue
        try:
            parsed = yaml.safe_load(code)
            assert isinstance(parsed, dict)
        except Exception as e:  # noqa: BLE001
            bad.append((code[:80], str(e)))
    assert not bad, f"{md_path.name}: bad yaml blocks:\n{bad}"


def test_compose_examples_are_well_shaped():
    comps = []
    for md in all_docs():
        text = md.read_text(encoding="utf-8")
        for lang, code in md_blocks(text):
            if lang != "yaml":
                continue
            parsed = yaml.safe_load(code)
            if isinstance(parsed, dict) and "services" in parsed:
                comps.append((md.name, parsed))
    assert comps, "expected at least one compose example"

    for src, comp in comps:
        for name, svc in comp["services"].items():
            assert isinstance(name, str)
            assert "image" in svc, f"{src}: service {name} has no image"
            for p in svc.get("ports", []):
                sp = str(p).strip('"')
                host, _, inner = sp.partition(":")
                assert host.isdigit() and inner.isdigit(), f"{src}: bad port {sp!r}"
            for v in svc.get("volumes", []):
                assert isinstance(v, str) and len(v.split(":")) == 2, f"{src}: bad volume {v!r}"
        declared = set(comp.get("volumes", {}))
        for svc in comp["services"].values():
            for v in svc.get("volumes", []):
                left = v.split(":")[0]
                assert left in declared or left.startswith(("/", "./", "~")), \
                    f"{src}: volume {left} used but not declared"
        for key in comp.get("volumes", {}):
            assert isinstance(comp["volumes"][key], (dict, type(None)))


# ------------------------------------------------- docs hygiene

def test_no_secrets_in_docs():
    patterns = ("api_key", "apikey", "sk-", "ghp_", "begin rsa", "begin openssh",
                "openssh private")
    for md in all_docs():
        text = md.read_text(encoding="utf-8").lower()
        for blob in patterns:
            assert blob not in text, f"{md.name} contains {blob!r}"


def test_chapters_are_substantive():
    for md in all_docs():
        assert len(md.read_text(encoding="utf-8").split()) > 300, f"{md.name} reads thin"


def test_docs_match_site_pages():
    slug_md = {s for s, _, _ in build.PAGES}
    on_disk = {p.name for p in DOCS.glob("*.md")}
    assert slug_md == on_disk, f"site/docs mismatch: {slug_md ^ on_disk}"
