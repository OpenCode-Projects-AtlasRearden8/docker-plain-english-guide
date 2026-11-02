# Chapter 7: Cleanup Commands — Every Tidy-Up Tool, Explained

Docker's cleanup commands have friendly, memorable names (they nearly all end
in `prune`, which means "trim"). This chapter walks through all of them, from
"definitely safe" to "only if you mean it."

Before anything: see how much space Docker is using, and where:

```bash
docker system df
```

(`df` is old computer-speak for "disk usage".) A `docker system df` that says
you only use 300 MB is a permission slip to relax and stop reading.

## Containers: stop, remove, sweep

Look before you touch:

```bash
docker ps -a
```

Stop one politely:

```bash
docker stop my-container
```

Remove one (must not be running):

```bash
docker rm my-container
```

Force-stop-and-remove in one step (only when sure):

```bash
docker rm -f my-container
```

**Sweep all stopped containers.** This is the most universally safe cleanup:
a stopped container is, almost always, a leftover from something you finished
(or `hello-world`). It removes containers, not images and not volumes:

```bash
docker container prune
```

Docker asks "Are you sure you want to continue? [y/N]" — type `y` and Enter.

## Images: the recipes

List them with sizes:

```bash
docker image ls
```

Remove one specific image:

```bash
docker rmi nginx
```

(`rmi` = remove image. If some container still uses it, Docker says no, and
that's the safety net working.)

**Sweep images nothing is using.** This removes images not referenced by any
container — including ones you pulled an hour ago for "later". Safe, but can
mean a re-download later:

```bash
docker image prune
```

Also-nice variant, remove images that haven't been used in the last 7 days:

```bash
docker image prune --filter "until=168h"
```

(`168h` = 168 hours = 7 days. Adjust to taste.)

## Volumes: the Tupperware

Volumes hold data that survived containers on purpose — models and chat
history are volume-sized commitments. Two rules:

1. **Named volumes you recognize** (like `ollama-models`) — keep them until
   you're truly done with that tool.
2. **Anonymous volumes** with no name you recognize — usually accident
   leftovers. Sweep them:

```bash
docker volume prune
```

Note (recent Docker versions): by default this keeps volumes that are used by
*any* container, and removes only the wholly-orphaned ones — which is exactly
the friendly behavior you want. If you want the more aggressive older style
(remove even volumes attached to stopped containers), there's an
`--all`/`-a` flag; leave it alone until you're comfortable.

## Networks: the invisible leftovers

Every compose stack quietly creates a small private network; `compose down`
usually removes it, but strays happen (often from experiments you half-remember):

```bash
docker network ls
```

If the list has names that are clearly from old experiments, `docker network
rm their-name` removes one, and the gentle sweep gets all unused ones:

```bash
docker network prune
```

This one is essentially always safe to run.

## The big soft brush and the big hard brush

`docker system prune` is everything above in one polite command: stopped
containers, unused networks, dangling images (untagged leftovers), and
unused cache. It **does not** touch named volumes:

```bash
docker system prune
```

Add `--volumes` only if you're ready for data loss of anything not attached
to a running container:

```bash
docker system prune --volumes
```

Read that again. `--volumes` is the only flag in this chapter that can delete
a downloaded model or chat history. It is the one to think about twice.

## Evergreen habit

If you do nothing else: run `docker system df` occasionally, and
`docker container prune` after finishing experiments. That alone keeps
Docker healthy basically forever.

The next chapter turns all of this into one short, calm checklist — what to
do before deleting anything named, and what to leave well alone.
