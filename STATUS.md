# STATUS.md

Project: **Docker in Plain English** — a beginner manual (Markdown) mirrored
as a static HTML site, with verified copyable commands and a gentle glossary.
Part of The Massive AI Manual series, published by Asdale Dynamics, LLC.

Date: 2026-11-02

## What was built

- **docs/** — 10 Markdown chapters, written in plain, warm, step-by-step style:
  - `00-welcome.md` — who it's for, how to use it
  - `01-images-arent-magic.md` — the image/container distinction
  - `02-containers-vs-vms.md` — why Docker feels light and fast
  - `03-volumes.md` — surviving containers, with a hands-on demo
  - `04-compose.md` — one file, one command, whole stacks
  - `05-examples-local-ai-stack.md` — Ollama + Open WebUI, fully local,
    no accounts, no API keys
  - `06-troubleshooting.md` — common failures and their kindly fixes
  - `07-cleanup-commands.md` — every prune command explained
  - `08-safe-cleanup.md` — a trustworthy before-you-delete checklist
  - `09-glossary.md` — ~25 gentle, plain-English definitions
- **site/** — static HTML generated from docs/ by `build.py` (no external
  dependencies): shared stylesheet, chapter nav, one-click Copy buttons under
  every command block, mobile-friendly, credits the LLC in every footer.
- **examples/ollama-compose/compose.yaml** — the ready-to-use local AI stack
  file from Chapter 5 (annotated, secrets-free).
- **build.py** — Markdown → HTML renderer (stdlib only).
- **tests/test_guide.py** — 28 pytest checks (see Verification below).
- **Makefile** — optional `make build / serve / test` shorthands.
- **LICENSE** — MIT, copyright line exactly: `Copyright (c) 2026 Asdale Dynamics, LLC`.
- **README.md** — chapter map, run/test instructions, credit to
  Asdale Dynamics, LLC and a link to dylanasdale.github.io.

## How to run it

```bash
python3 build.py                                # build site/ from docs/
python3 -m http.server 8787 --directory site    # serve at http://localhost:8787
python3 -m pytest tests/ -q                     # run the test suite
```

(`make build`, `make serve`, `make test` also work where `make` exists.)
Or simply open `site/index.html` in a browser — it's fully static.

## Verification results

- `python3 -m pytest tests/ -q` → **28 passed**. The suite verifies:
  - the site builds (10 pages) and each has DOCTYPE, nav, credits;
  - every code-block div has exactly one Copy button;
  - internal site links resolve; external links are https (except localhost);
  - **every `bash` block in docs/ passes `bash -n`** (shell syntax-checked);
  - every documented `docker` command is a real Docker subcommand;
  - every `yaml` block parses; compose examples have numeric port pairs,
    declared named volumes, and images on every service;
  - no secret-shaped strings in any doc; chapters are substantive.
- `markdownlint docs/` → **0 errors**.
- Python HTMLParser tag-balance check over all 10 generated pages → **0 errors**.
- `python3 -m http.server` + curl smoke test → index and chapter pages return **200**.
- `examples/ollama-compose/compose.yaml` parses as valid YAML with the two
  expected services.

## Known gaps

1. **Docker was not installed in this writing environment**, so no command
   was *executed* against a live Docker daemon here. Mitigation: every command
   is syntax-checked (`bash -n`) and cross-checked against real Docker
   subcommands by the tests; the Ollama/Open WebUI stack matches the projects'
   official documented configurations (ports 11434 / 8080→3000, volumes
   `/root/.ollama` and `/app/backend/data`, `OLLAMA_BASE_URL`). If run on a
   machine with Docker, Chapter 5 is designed to be followed start-to-finish.
2. The HTML renderer supports the subset of Markdown used in docs/
   (headings, lists, fenced code, blockquotes, inline styles, links) — enough
   for this manual, not a general-purpose Markdown parser.
3. No semantic search, print stylesheet, or dark mode — nice future polish.
4. Only the local-AI stack example is included; other stacks (e.g. a binding
   mount "my documents" reader) are described in prose but not shipped as
   ready-made files.
5. The site link for http://localhost:3000 is the one intentional non-https
   link (it refers to the reader's own machine) — this is by design.

## Integrity notes

- No secrets, API keys, or personal data in any file (enforced by test).
- Single commit authored as the existing git identity
  (Dylan Asdale <dylanasdale@users.noreply.github.com>), plain message, no
  co-author trailers; nothing pushed or published anywhere.
