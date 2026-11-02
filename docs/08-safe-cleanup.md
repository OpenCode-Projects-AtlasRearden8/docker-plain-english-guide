# Chapter 8: Safe Cleanup — A Checklist You Can Trust

Docker rarely makes you choose under pressure, and yet: when your disk is
full or you're "just tidying", it's easy to delete the wrong thing. This
chapter is the pause, breathe, and check routine — what to do *before*
deleting, and a do-not-touch list.

## The before-you-delete checklist (60 seconds)

1. **Look first, delete second.** Nothing in this manual needs deleting on a
   schedule. Curiosity first, and four quick peeks — `docker system df`,
   `docker ps -a`, `docker image ls`, and `docker volume ls` — tell you
   everything Docker is keeping and how big it all is.

2. **Name things kindly.** Anything you're not sure about — is that
   `ollama-models`? `my-first-experiment`? — that's the sign to *stop*, not
   delete. Well-named things survive investigation.

3. **Check what's using an image before removing it.** See the containers
   that use it first: run `docker ps -a --filter ancestor=nginx` (adjust the
   image name). If a container uses it, you'll see the container, and
   `docker image rm` would refuse anyway. Safer to know first.

4. **Prefer prune sweeps to naming your own victims.** If you don't know what
   something is, you shouldn't be deleting it by name. The prune commands
   remove only clearly unused things — that's exactly their kindness.

5. **When in doubt, walk away for five minutes.** Cleanup desire is 90%
   anxiety, 10% disk space. The disk will still be full in five minutes; the
   wrong deletion is forever.

## Safe by almost any definition

These four are the habits of people who never lose data to Docker — every
one of them removes only clearly unused things:

```bash
docker container prune
```

```bash
docker network prune
```

```bash
docker image prune
```

```bash
docker system prune
```

(Stopped containers; unused networks; images nothing references; and the
combined sweep. None of them touch named volumes without the extra
`--volumes` flag from the last chapter.)

A sentence you'll want to remember about images specifically:
**images can always be re-pulled.** Deleting an image costs you a re-download
and never costs data.

## The do-not-touch list

- **`docker volume prune --all`** (or any volume deletion) while any real
  stack exists. Volumes are the data. That's the whole point.
- **`rm -rf /var/lib/docker` by hand.** Never, ever. It's the classic
  "delete my entire Docker life in one keystroke" move. If you want a full
  reset, uninstall Docker Desktop properly, or use its built-in reset; the
  official uninstallers are built to do that safely.
- **`docker system prune --volumes` on a machine running AI models.** The
  only way this chapter's commands delete real data. If you ever run it, stop
  first and check `docker volume ls` — everything in that list stays in that
  moment unless a container is running and using it.
- **Deleting by name anything you can't say a full sentence about.**
  ("`docker volume rm ollama-models` — that's where my downloaded Llama model
  lives.") If you can't finish the sentence, don't run the command.

## A tidy routine for "I'm done with this tool for now"

If it's a compose stack, run `docker compose down` (containers gone, data
kept), then `docker container prune` to sweep strays, then check the new
smaller number with `docker system df` — and optionally `docker image prune`
— and go back to your life.

For "I'm done with this tool forever": `docker compose down --volumes` from
the stack's folder, or `docker volume rm the-name` individually — after
reading the name three times and being able to say out loud what it holds.

## The one-sentence summary

**Images and stopped containers are always safe to clean. Networks are safe
to clean. Volumes are the data — look before you touch, and name things
kindly so future-you can tell what anything is.**
