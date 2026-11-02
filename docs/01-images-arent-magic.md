# Chapter 1: Images Aren't Magic

The single most common confusion for beginners: **an image and a container are
two different things.** Once this clicks, most of Docker makes sense.

## The recipe and the cake

Think of it like this:

- An **image** is a recipe downloaded from the internet. It sits quietly on
  your computer, doing nothing. It is a frozen snapshot of a program plus
  everything that program needs.
- A **container** is the actual cake you bake *from* that recipe. It runs,
  it works, it takes up attention — and when it stops, it's gone.

You can bake many cakes from one recipe (run many containers from one image),
and they never get in each other's way.
The mental model in one line:

> **Image = the recipe. Container = the running thing. Volume = the Tupperware
> you keep after the cake is eaten.**

(Volumes come in Chapter 3. Patience.)

## See what images you already have

```bash
docker image ls
```

`ls` is old computer-speak for "list". You'll see a table with columns like
`REPOSITORY`, `TAG`, `IMAGE ID`, and `SIZE`. The repository is the recipe's
name, the tag is usually the version. Right after installing Docker this list
is probably empty. That's normal — you haven't downloaded any recipes yet.

## Download a recipe (a tiny, harmless one)

The classic first move in Docker-land is `hello-world` — a recipe that, when
baked, prints a friendly paragraph and quits. Download and run it in one go:

```bash
docker run hello-world
```

What happened, in order:

1. Docker noticed you don't have the `hello-world` image yet.
2. It downloaded it from Docker Hub (the big public library of images).
3. It baked one container from it, ran it, and — since the program finished —
   the container quietly went away.

You now have a new image and zero new containers. Prove it:

```bash
docker image ls
```

```bash
docker ps -a
```

`docker ps` lists containers (the `-a` means "all", including the ones that
already stopped). You'll see `hello-world` listed with status `Exited`. That
leftover line is normal and we clean it up in a later chapter.

## "But where did the image come from?"

From a **registry** — an app store for images. The default one is
**Docker Hub** at <https://hub.docker.com>. When you write
`docker run hello-world`, Docker quietly reads that as
`docker.io/library/hello-world`. You almost never need to think about that.

## The command that does 90% of your Docker life

```bash
docker run --name my-bubble -d nginx
```

Don't run that yet — read it first, in slow motion:

- `docker run` — bake a container from an image and start it.
- `--name my-bubble` — give it a friendly name so future-you can find it.
- `-d` — detached: it runs in the background so your terminal stays yours.
- `nginx` — the image name (a popular web server, used here as an example).

If you *do* run it, look around with `docker ps`, then tidy up:

```bash
docker ps
```

```bash
docker stop my-bubble
```

```bash
docker rm my-bubble
```

- `stop` asks it politely to quit.
- `rm` removes the stopped container (the cake). The image (the recipe) is
  still on your disk, untouched.

## Names with slashes and colons

You'll see images like `ollama/ollama` or `ghcr.io/open-webui/open-webui:main`
in the examples chapter. Nothing scary:

- A slash (`author/name`) just says who published the recipe.
- A colon (`:main` or `:1.17`) picks a specific version. No colon means
  "latest", which almost always does what you hope.

## One recipe, many cakes — worth saying twice

If you run the same image twice, you get two independent containers:

```bash
docker run --name cake-one -d alpine sleep 60
```

```bash
docker run --name cake-two -d alpine sleep 300
```

(`alpine` is the smallest, most popular "tiny Linux" image; `sleep` just makes
it sit there for a bit so it's "running" long enough to look at.)

Both will show up in `docker ps`. Neither affects the other. That
isolation-in-plain-English is Docker's entire superpower.
