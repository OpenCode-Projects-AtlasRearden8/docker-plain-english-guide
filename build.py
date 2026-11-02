#!/usr/bin/env python3
"""Build the static HTML site from docs/.

Reads docs/*.md, renders each into site/<slug>.html with a shared warm,
accessible stylesheet, a copy button under every fenced code block, and
cross-page nav. No third-party dependencies.

Copyright (c) 2026 Asdale Dynamics, LLC
"""

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

PAGES = [
    ("00-welcome.md", "index.html", "Welcome"),
    ("01-images-arent-magic.md", "01-images.html", "Images aren't magic"),
    ("02-containers-vs-vms.md", "02-vms.html", "Containers vs VMs"),
    ("03-volumes.md", "03-volumes.html", "Volumes"),
    ("04-compose.md", "04-compose.html", "Compose"),
    ("05-examples-local-ai-stack.md", "05-examples.html", "Local AI stack"),
    ("06-troubleshooting.md", "06-troubleshooting.html", "Troubleshooting"),
    ("07-cleanup-commands.md", "07-cleanup.html", "Cleanup commands"),
    ("08-safe-cleanup.md", "08-safe-cleanup.html", "Safe cleanup"),
    ("09-glossary.md", "09-glossary.html", "Glossary"),
]

def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"<(https?://[^>]+)>", r'<a href="\1">\1</a>', out)
    out = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', out)
    return out


def render_markdown(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    in_code = False
    code_lang = ""
    code_buf: list[str] = []
    i = 0
    list_stack: list[str] = []  # "ul" | "ol"

    def close_list():
        while list_stack:
            out.append(f"</{list_stack.pop()}>")

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        m = re.match(r"^```(\w*)\s*$", stripped)
        if m:
            if not in_code:
                in_code = True
                code_lang = m.group(1)
                code_buf = []
            else:
                in_code = False
                lang = html.escape(code_lang or "text")
                code = html.escape("\n".join(code_buf))
                label = f'<span class="lang">{lang}</span>' if code_lang else ""
                out.append(
                    f'<div class="code">{label}'
                    f'<button class="copy" type="button" aria-label="Copy command">Copy</button>'
                    f'<pre><code>{code}</code></pre></div>'
                )
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if not stripped:
            close_list()
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            close_list()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        m = re.match(r"^>\s?(.*)$", stripped)
        if m:
            close_list()
            out.append(f"<blockquote><p>{inline(m.group(1))}</p></blockquote>")
            i += 1
            continue

        m = re.match(r"^([-*])\s+(.*)$", stripped)
        if m:
            if not list_stack or list_stack[-1] != "ul":
                close_list()
                list_stack.append("ul")
                out.append("<ul>")
            out.append(f"<li>{inline(m.group(2))}</li>")
            i += 1
            continue

        m = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m:
            if not list_stack or list_stack[-1] != "ol":
                close_list()
                list_stack.append("ol")
                out.append("<ol>")
            out.append(f"<li>{inline(m.group(2))}</li>")
            i += 1
            continue

        close_list()
        out.append(f"<p>{inline(stripped)}</p>")
        i += 1

    close_list()
    return "\n".join(out)


CSS = """
:root{--bg:#faf6f1;--fg:#2b2622;--accent:#7a4a2b;--card:#fff;
--border:#e4dcd2;--codebg:#2d2a26;--codefg:#f3efe8;--link:#9a5b2d}
*{box-sizing:border-box}
body{margin:0;font-family:Georgia,'Times New Roman',serif;
background:var(--bg);color:var(--fg);line-height:1.65}
header.site{background:var(--accent);color:#fff;padding:1rem 1.5rem;
display:flex;flex-wrap:wrap;gap:.75rem;align-items:baseline;justify-content:space-between}
header.site .brand{font-size:1.05rem;font-weight:bold;text-decoration:none;color:#fff}
header.site .tag{font-size:.8rem;opacity:.85}
nav.chapters{background:var(--card);border-bottom:1px solid var(--border);
padding:.6rem 1.5rem;display:flex;flex-wrap:wrap;gap:.35rem 1rem}
nav.chapters a{font-size:.8rem;color:var(--link);text-decoration:none}
nav.chapters a.cur{font-weight:bold;color:var(--fg)}
main{max-width:46rem;margin:0 auto;padding:1.5rem 1.25rem 4rem}
h1{font-size:1.7rem;margin:.6rem 0 1rem}
h2{font-size:1.25rem;margin-top:2rem;border-bottom:1px solid var(--border);padding-bottom:.25rem}
h3{font-size:1.05rem;margin-top:1.5rem}
p,li{font-size:1rem}
a{color:var(--link)}
code{font-family:'SFMono-Regular',Consolas,Menlo,monospace;font-size:.86em;
background:#efe7db;padding:.1em .35em;border-radius:4px}
blockquote{margin:1rem 0;padding:.6rem 1rem;border-left:4px solid var(--accent);
background:var(--card);border-radius:0 6px 6px 0}
blockquote p{margin:.2rem 0}
div.code{position:relative;background:var(--codebg);color:var(--codefg);
border-radius:8px;margin:1rem 0;border:1px solid var(--border)}
div.code pre{margin:0;padding:1rem 1rem 1rem 1rem;overflow-x:auto}
div.code code{background:none;color:var(--codefg);padding:0;font-size:.87rem}
div.code .lang{position:absolute;top:.45rem;left:1rem;font-size:.66rem;
letter-spacing:.12em;text-transform:uppercase;color:#b3a99c;font-family:sans-serif}
button.copy{position:absolute;top:.35rem;right:.35rem;background:#4a4238;
color:#f3efe8;border:1px solid #6b6152;border-radius:6px;font-size:.7rem;
padding:.3rem .65rem;cursor:pointer;font-family:sans-serif}
button.copy:hover{background:#5c5245}
footer{max-width:46rem;margin:0 auto;padding:1rem 1.25rem 3rem;font-size:.85rem;color:#8d8175}
footer a{color:var(--link)}
@media(max-width:600px){nav.chapters{padding:.5rem .75rem}}
"""

JS = """
document.addEventListener('click',function(e){
  if(!e.target.classList.contains('copy'))return;
  var btn=e.target,pre=btn.parentElement.querySelector('pre');
  navigator.clipboard.writeText(pre.textContent.trim()).then(function(){
    btn.textContent='Copied!';setTimeout(function(){btn.textContent='Copy';},1400);
  });
});
"""


def page_html(title: str, body: str, cur_slug: str) -> str:
    nav_items = []
    for slug, fname, label in PAGES:
        cls = ' class="cur"' if slug == cur_slug else ""
        nav_items.append(f'<a href="{fname}"{cls}>{html.escape(label)}</a>')
    nav = "\n".join(nav_items)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Docker, explained in plain English for non-engineers. By Dylan Asdale, published by Asdale Dynamics, LLC.">
<title>{html.escape(title)} — Docker in Plain English</title>
<style>{CSS}</style>
</head>
<body>
<header class="site">
  <a class="brand" href="index.html">Docker in Plain English</a>
  <span class="tag">The Massive AI Manual · Asdale Dynamics, LLC</span>
</header>
<nav class="chapters">
{nav}
</nav>
<main>
{body}
</main>
<footer>
  Written in plain English by Dylan Asdale · <em>The Massive AI Manual</em> series<br>
  © 2026 Asdale Dynamics, LLC · MIT licensed · local-first, friendly, tested.
</footer>
<script>{JS}</script>
</body>
</html>
"""


def build() -> list[str]:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    built = []
    for slug_md, out_name, label in PAGES:
        md = (DOCS / slug_md).read_text(encoding="utf-8")
        body = render_markdown(md)
        page = page_html(label, body, slug_md)
        (SITE / out_name).write_text(page, encoding="utf-8")
        built.append(out_name)
    return built


if __name__ == "__main__":
    outs = build()
    for o in outs:
        print(f"built site/{o}")
    print(f"{len(outs)} pages built.")
