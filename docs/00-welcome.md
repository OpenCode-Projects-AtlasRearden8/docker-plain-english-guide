# Welcome: Docker Like a Friend Would Explain It

*Part of The Massive AI Manual series. By Dylan Asdale — published by
Asdale Dynamics, LLC.*

## Who this is for

This manual is for you if any of these sound familiar:

- You have heard the word "Docker" and nodded politely while your stomach sank.
- You want to run a local AI tool (like Ollama or Open WebUI) but every tutorial
  assumes you already know things nobody ever explained to you.
- You want to try an open-source tool you found, without installing five
  mysterious things all over your laptop.

You do not need to be an engineer. You do not need to have used the command line
much (or at all). Every command in this manual is copy-and-paste ready, and every
one of them has been run and checked before it landed on this page.

## What Docker actually does (the 10-second version)

Docker lets you run a program in a tidy little bubble called a **container**.
Everything the program needs — its files, its settings, its own private copy of
Linux — lives inside that bubble. When the program ends, the bubble disappears
without leaving mess on your computer.

That is the whole trick. The rest of this manual is just learning to talk to
the bubble politely.

## How to use this manual

The chapters are short on purpose. Read them in order the first time:

1. **Images aren't magic** — what you download and what you run.
2. **Containers vs VMs** — why Docker feels light and fast.
3. **Volumes** — how to keep your files when a container disappears.
4. **Compose** — running several tools together from one file.
5. **Examples: a local AI stack** — Ollama and Open WebUI, step by step.
6. **Troubleshooting** — what to do when it misbehaves.
7. **Cleanup commands** — every "tidy up" command explained.
8. **Safe cleanup** — what you can remove without fear, and what to leave alone.

The last part is a **gentle glossary** — plain-English definitions you can skim
when a word sneaks up on you.

## A promise before we start

- Nothing here will touch your personal files unless you tell it to.
- Nothing here needs a secret, an API key, or an account.
- If a command can be copy-pasted, it is written exactly as you would type it.
- You cannot "break your computer" by following this manual. Worst case, you
  delete a container and run the same command again. That is it.

Take a breath. Open a terminal. Type this to prove Docker (or Docker Desktop)
is installed and awake:

```bash
docker --version
```

If you see something like `Docker version 27.x.x`, you are gold. If not, the
very next chapter starts gently and the troubleshooting chapter has a section
on "Docker isn't installed" panic.

## Where to get Docker if you don't have it

- **Windows or Mac:** download Docker Desktop from
  <https://www.docker.com/products/docker-desktop/>. It is a normal installer —
  click Next a few times and it appears in your menu or dock.
- **Linux:** follow the official install page
  <https://docs.docker.com/engine/install/> for your distribution, or your
  package manager's `docker` package.

The rest of the manual assumes `docker --version` answers politely.
