# Chapter 5: Examples — Running a Local AI Stack

This chapter is the reason many people picked up this manual: get **Ollama**
(a local AI engine) and **Open WebUI** (a friendly chat screen for it) running
on your own computer, entirely local, entirely free, no accounts, no API keys.

Everything here follows the same calm pattern you already know: image →
container → volume.

## Step 0: know what you're plugging in

- **Ollama** downloads and runs open models like Llama, Gemma, and Qwen on
  your machine. It talks on port **11434**.
- **Open WebUI** is the website you'll open in your browser: a proper chat
  interface with history, model picking, and markdown rendering. It talks on
  port **8080** (inside its container) and we'll show it as port **3000** on
  your machine.

## Step 1: a home folder

Anywhere you like — documents, wherever — make a folder, say `ai-stack`, and
sit your terminal in it. This folder will hold one file and remember which
stack you started from where. (Bind mounts come later for your own files;
today's stack keeps everything in Docker volumes.)

## Step 2: the compose file

Create `compose.yaml` in that folder with exactly this:

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama-models:/root/.ollama
    ports:
      - "11434:11434"
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    volumes:
      - open-webui-data:/app/backend/data
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama-models:
  open-webui-data:
```

Breathe. Read it once through. It's two services, two volumes, two port
mappings, and one line of instructions ("find Ollama at `ollama:11434`" —
compose lets containers address each other by their service names).

Both `restart: unless-stopped` lines mean: if the container crashes or your
computer reboots, bring it back — unless you stopped it on purpose.

## Step 3: start the stack

From inside the `ai-stack` folder:

```bash
docker compose up -d
```

The first run downloads both images, which can take a few minutes on slow
internet. That's a one-time cost.

## Step 4: watch it settle

```bash
docker compose ps
```

You want both services to say `running`. Then peek at whatever either has
said so far:

```bash
docker compose logs --tail 20
```

## Step 5: open your chat screen

In a browser, go to **<http://localhost:3000>**. On the very first visit,
Open WebUI asks you to create the first account — this lives entirely inside
your own container (in your `open-webui-data` volume); nothing is sent
anywhere. Pick any username and password you like. This is your private,
local chat app.

## Step 6: get a model

The model needs to be pulled by Ollama once, and then any chat in the web UI
can use it. While you're at the terminal (or from inside Open WebUI's admin
models page if you prefer clicking):

```bash
docker exec ollama ollama pull llama3.2:1b
```

- `docker exec ollama` — run a command inside the running `ollama` container.
- `ollama pull llama3.2:1b` — Ollama's own command: download the Llama 3.2
  model with the `1b` (one-billion parameter) tag — a small, quick model that
  runs comfortably on ordinary laptops.

Feeling brave? A slightly larger, noticeably smarter model:

```bash
docker exec ollama ollama pull llama3.2:3b
```

(`1b` ~1–2 GB, `3b` ~2–3 GB of download roughly; both are fine for laptop use.)

## Step 7: talk to it

Back in the browser: pick the model from the dropdown at the top of the chat
box, type something ordinary — "explain photosynthesis like I'm ten" — and
watch it respond, from your own machine, with no internet after setup.

Note: chat history is stored in the `open-webui-data` volume, and model files
in `ollama-models`. **That's the whole reason those volumes are in the compose
file.** Upgrade the images next month, run `docker compose up -d`, and your
models and chats stay.

## Everyday upkeep, when you want it

Update the recipes and rebuild the flock (chats and models kept):

```bash
docker compose pull
```

```bash
docker compose up -d
```

Take a peek at what the stack has said recently:

```bash
docker compose logs --tail 30
```

Stop everything without deleting anything:

```bash
docker compose stop
```

Start it again later:

```bash
docker compose start
```

Remove the containers (volumes/chat/models survive):

```bash
docker compose down
```

## CPU-only? GPU? The short version

- **Works on any modern computer** with the compose above — it uses CPU.
- If you have an NVIDIA GPU *and* drivers working, faster inference is a
  one-line change: under `ollama:` in the compose file, add:

```yaml
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

Only attempt this if `docker run --gpus all --rm ubuntu nvidia-smi` works. If
that command trips you up, the CPU setup above already works pleasantly —
you lose nothing by waiting.

## What you just did, honestly

You installed nothing. You configured nothing scary. You described a
two-container stack in one tidy file, pressed `docker compose up -d`, and got
a working, private, local AI chat setup. That is beginner-level Docker doing
real, useful work — and it's the exact pattern you'll reuse for a hundred
other open-source tools.
