# Docker in Plain English

*A guide to Docker for non-engineers — part of The Massive AI Manual series.*

Docker explained the way a friend would: warm, step by step, never
condescending. Every command in these chapters is copy-paste ready and has
been syntax-checked before landing here.

## What's inside

| Chapter (Markdown) | Site page | What it covers |
|---|---|---|
| [Welcome](docs/00-welcome.md) | [index.html](site/index.html) | Who this is for, how to read it |
| [Images aren't magic](docs/01-images-arent-magic.md) | [01-images.html](site/01-images.html) | The image/container distinction |
| [Containers vs VMs](docs/02-containers-vs-vms.md) | [02-vms.html](site/02-vms.html) | Why Docker feels light and fast |
| [Volumes](docs/03-volumes.md) | [03-volumes.html](site/03-volumes.html) | Keeping data when containers vanish |
| [Compose](docs/04-compose.md) | [04-compose.html](site/04-compose.html) | Several tools, one file, one command |
| [Examples: local AI stack](docs/05-examples-local-ai-stack.md) | [05-examples.html](site/05-examples.html) | Ollama + Open WebUI, fully local |
| [Troubleshooting](docs/06-troubleshooting.md) | [06-troubleshooting.html](site/06-troubleshooting.html) | The common failures and kind fixes |
| [Cleanup commands](docs/07-cleanup-commands.md) | [07-cleanup.html](site/07-cleanup.html) | Every prune, explained |
| [Safe cleanup](docs/08-safe-cleanup.md) | [08-safe-cleanup.html](site/08-safe-cleanup.html) | A checklist for deleting without fear |
| [Glossary](docs/09-glossary.md) | [09-glossary.html](site/09-glossary.html) | Gentle, plain-English definitions |

Also included: `examples/ollama-compose/compose.yaml` — a ready-made compose
file for the local AI stack (Ollama + Open WebUI), direct from Chapter 5.

## Run it

No dependencies beyond Python 3.8+ — the standard library only, plus
`pytest` and `pyyaml` for tests (`pip install pytest pyyaml`).

```bash
python3 build.py    # renders docs/ -> site/ (10 static HTML pages)
```

Read the site two ways:

- Open `site/index.html` directly in any browser — it's a static file with
  copy buttons under every command.
- Or serve it locally if you prefer a URL:

```bash
python3 -m http.server 8787 --directory site    # http://localhost:8787
```

(A `Makefile` with `make build` / `make serve` / `make test` shorthands is
included, in case `make` is available.)

## Test it

```bash
python3 -m pytest tests/ -q
```

The test suite verifies that:

- the site builds and every page carries nav, copy buttons, and credits,
- internal links resolve,
- **every `bash` code block in docs/ passes `bash -n`** (syntax-checked, not
  merely copy-pasted),
- every documented `docker` subcommand is a real one,
- every `yaml` block parses and compose examples are well-shaped
  (numeric port pairs, declared volumes),
- nothing resembling a secret appears anywhere.

Chapters that include destructive-looking-but-safe commands (prunes) were
reviewed line-by-line against the [Docker documentation](https://docs.docker.com/).
Troubleshooting, cleanup, and safe-cleanup chapters were proofread for the
"delete the wrong thing" traps and give clearer guidance instead.

## Notes

- Docker itself is not installed in this writing environment, so runtime
  smoke tests (e.g. actually running `docker compose up`) were done by
  hand-matching each command against official docs and against the widely
  used Ollama/Open WebUI Docker configurations. See [STATUS.md](STATUS.md).
- No secrets, API keys, or personal data are in any file — by design and by
  test.

## Credits

Written by Dylan Asdale (*The Massive AI Manual*).
Published by **Asdale Dynamics, LLC** — beginner-friendly AI education,
books, and practical tools. Learn more at
[dylanasdale.github.io](https://dylanasdale.github.io).

Licensed under the MIT License — see [LICENSE](LICENSE).
