# Chapter 4: Compose — Several Tools, One File, One Command

`docker run` is wonderful for one container. But real tools often want a
small flock of containers working together — say, an AI brain and its chat
screen. Typing a long `docker run` line every time, remembering six flags in
order, is exactly the kind of chore that makes people quit.

**Compose** fixes that: you write the whole flock down once, in one little
`compose.yaml` file, and then control all of it with a couple of short
commands.

The old name people use is "docker-compose"; the modern spelling — the one
that works on any up-to-date install — is `docker compose` (with a space).

## Your first compose file

Make a new folder anywhere you like — for instance `dockerplay` — `cd` into
it in your terminal, and create a file named exactly:

```text
compose.yaml
```

(Depending on your editor this may be shown as `compose.yaml.txt` — turn the
`.txt` off. The ending must be `.yaml`.)

Paste this into the file:

```yaml
services:
  alpine:
    image: alpine
    command: sleep infinity
```

Then, in your terminal, from that same folder:

```bash
docker compose up -d
```

- `up` — create and start whatever the file describes.
- `-d` — detached: keep your terminal.

Check on it:

```bash
docker compose ps
```

You'll see `alpine` running. Look at its recent activity:

```bash
docker compose logs --tail 20
```

(`--tail 20` means "just the last 20 lines," in case of chatter.)

When you're done playing:

```bash
docker compose down
```

`down` stops and removes the containers — the flock is gone in one word.
The images (recipes) stay on your disk, and named volumes also stay, which
leads nicely to the next point.

## Compose is careful with your data

By default, `down` removes containers but **keeps named volumes**. Your data
is safer than your fear. To explicitly remove volumes too (only when you
mean it):

```bash
docker compose down --volumes
```

## A compose file that would actually be useful

Here is the shape of a real compose file — the one we'll build in the next
chapter. For now just absorb how tidy it is; you don't need to run it yet.

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama-models:/root/.ollama
    ports:
      - "11434:11434"

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "8080:8080"
    depends_on:
      - ollama

volumes:
  ollama-models:
```

Reading it like a friend would translate it to you:

- **services** — the flock. Each entry is one container.
- **image** — which recipe to use.
- **volumes** — which folders to plug in (the named volume `ollama-models` is
  declared at the bottom, under the top-level `volumes:` heading).
- **ports** — `"11434:11434"` means "official port 11434 of the container,
  reachable at port 11434 on *my* computer." Left side: your machine. Right
  side: inside the container. The quotes matter; always include them.
- **depends_on** — start the helper first.

## The compose commands you'll actually use

There are only a handful. All run from the folder that contains the
`compose.yaml`:

```bash
docker compose up -d
```

```bash
docker compose ps
```

```bash
docker compose logs --tail 30
```

```bash
docker compose restart
```

```bash
docker compose stop
```

```bash
docker compose down
```

```bash
docker compose pull
```

(`pull` re-downloads the recipes' latest listed versions — a common step
before `up -d` when you want to catch a tool up.)

## Tiny etiquette notes

- Indentation matters in YAML. Two spaces, everywhere, no tabs. If compose
  complains about a mysterious error, nine times out of ten it's an
  indentation slip or a missing colon.
- File name: exactly `compose.yaml`. Compose also accepts `docker-compose.yml`
  (the older spelling works fine), but pick one and stay with it.
- One folder, one stack. Giving each project its own folder with its own
  `compose.yaml` keeps everything easy to reason about.

You now know enough to run a whole local AI stack. Honestly. Next chapter.
