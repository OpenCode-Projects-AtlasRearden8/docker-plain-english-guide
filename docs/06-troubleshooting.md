# Chapter 6: Troubleshooting — When It Misbehaves

Docker misbehaving is almost always one of a short list of simple causes.
This chapter is the list. Read it top to bottom; the fix is usually one
command away.

## First: the health check

Put your stethoscope on:

```bash
docker ps -a
```

Read the table like a friend would:

- `Up` — running and healthy. (The trailing time is how long it's been up.)
- `Exited (0)` — it ran, finished, and quit normally. Nothing is broken.
- `Exited (1)` or other non-zero numbers — it tried, hit a problem, quit. →
  next step: logs.
- `Created` or `Restarting` — it never quite got going. → also logs.

## The logs — always the logs

You'd be amazed how many mysteries end at:

```bash
docker logs my-container
```

Add `-f` ("follow") to watch it live like a movie; Ctrl+C stops watching
(the container keeps running):

```bash
docker logs -f my-container
```

Last 50 lines only, for chatty programs:

```bash
docker logs --tail 50 my-container
```

For compose stacks: same things work via `docker compose logs`.

## Approved grief list: common errors and their kindly fixes

### "Cannot connect to the Docker daemon"

Docker Desktop isn't running, or on Linux the daemon isn't started.

- Windows/Mac: open Docker Desktop and wait until it says running.
- Linux:

```bash
sudo systemctl start docker
```

### "permission denied … /var/run/docker.sock" (Linux)

Your user isn't in the `docker` group. Fix for real:

```bash
sudo usermod -aG docker $USER
```

Then log out and back in (or reboot) — genuinely required. Until then,
`sudo docker …` works.

### "port is already allocated" / "bind: address already in use"

Something else on your computer owns the port. Two options:

1. Stop/quit the other program (with a browser tab still holding 3000 open,
   quit and re-open the browser; it's usually that simple).
2. Use a different "outside" port, e.g. change `"3000:8080"` to
   `"3001:8080"` in `compose.yaml`, then `docker compose up -d` again. The
   right side of the colon never changes; only your side does.

### Container "Exited (1)" right after starting

Read the logs — truly, read the logs — but three usual suspects:

- a typo in a port or volume flag,
- the command inside the image needs different arguments,
- a bind-mounted folder doesn't exist or isn't readable — create the folder
  first; Docker only mounts what's there.

### "no space left on device"

Your disk is full, and it's almost certainly old images and stopped
containers. Do the gentle clean-up in the cleanup chapter; start with:

```bash
docker system df
```

then, if you like what it says you'd reclaim:

```bash
docker container prune
```

### Image pulls failing / timeouts

Wi-Fi wobbles, VPNs, and rare Docker Hub outages. Retry once; then check
<https://status.docker.com> if it keeps failing.

### "exec: container not running"

You tried `docker exec` on something that isn't running. `docker ps -a`
first, start it if it stopped:

```bash
docker start my-container
```

### Ctrl+C "stopped my whole stack" surprise

If you ran `docker compose up` *without* `-d`, the terminal is attached:
Ctrl+C stops the stack. Not a disaster — either

```bash
docker compose start
```

to bring the flock back, or use `docker compose up -d` next time for the
docile background version.

### The one-liner reset (polite version)

For compose stacks, when in doubt:

```bash
docker compose down
```

```bash
docker compose up -d
```

Rebooting the stack fixes a surprising range of ills, and costs you nothing
that volumes were there to protect.

## When to just ask a person

If a log mentions something unique (a crash, a specific model error), copy
the exact lines and search them — you are almost never the first person to
hit a given error message, and project GitHub issue pages are full of other
people asking the same question, usually with a kind answer nearby.
