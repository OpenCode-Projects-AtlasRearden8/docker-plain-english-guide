# Chapter 3: Volumes — Keeping Your Stuff When Containers Vanish

Here is the part nobody warns beginners about, and it causes quiet heartbreak:

> **When a container is removed, everything inside it is gone. Forever.**

If you chat with an AI inside a container and there's no volume, your chat
history lives in the container. Delete the container (maybe just to upgrade to
a newer version — a very normal thing to do) and your history evaporates.

**Volumes fix this.** A volume is a folder that Docker manages *outside* the
container's little world. You plug it in when the container starts, like
plugging an external drive into a laptop: the laptop can die, the drive keeps
its contents.

## The three kinds of "plugging in a folder"

### 1. Named volumes — Docker's managed storage (usually the right choice)

Docker creates and maintains a folder in its own storage area, and you refer
to it by a short name. Best for databases, models, chat histories — anything
a tool owns and you mostly don't want to touch by hand.

```bash
docker volume create my-notes
```

```bash
docker run -d --name notes-test -v my-notes:/data alpine sleep 300
```

Read that second command out loud: "Run a container named `notes-test`,
and plug my named volume `my-notes` in at the folder `/data` inside it."

(The colon can look like magic. Just remember: `-v` then
`external-name:inside-the-container`.)

### 2. Bind mounts — plugging in *your* real folders

A bind mount plugs one of your actual folders (with a path you already know
and love) into the container. The container sees your files live. Great when
*you* want to own the files — for example, a folder of your own documents.

```bash
docker run --rm -v "$PWD"/shared:/data alpine ls /data
```

In plain English: "Run a temporary container (`--rm` says remove it when done)
with my current folder's `shared` sub-folder visible inside the container at
`/data`, then list what's in there."

- `$PWD` means "my present working directory" — the folder your terminal is
  sitting in right now.
- Create a `shared` folder (with anything in it) where your terminal is when
  you try this, or the list comes back empty (which is also fine and harmless).

### 3. Anonymous volumes — the accidental ones

If an image's author declared "this image should have storage" and you didn't
plug anything in, Docker quietly makes an *anonymous* volume — a volume with
no nice name, just a long serial number. These pile up. The safe-cleanup
chapter shows how to sweep them.

## Watch a volume survive its container

This is worth doing once, because it cements the idea:

```bash
docker exec notes-test sh -c "echo hello > /data/notes.txt"
```

`exec` means "run a command inside the running container." Here we're writing
one small file, `hello`, into `/data/notes.txt`.

Now delete the container — the scary part:

```bash
docker stop notes-test
```

```bash
docker rm notes-test
```

The cake is gone. Now bake a new one from the same recipe, plugged into the
same volume:

```bash
docker run -d --name notes-test-2 -v my-notes:/data alpine sleep 300
```

```bash
docker exec notes-test-2 cat /data/notes.txt
```

`notes.txt`, still there, still saying hello. **That's volumes.** Your data
survived the death and rebirth of its container.

In real AI tools this is exactly how you keep your downloaded models and your
chat history between updates — you'll see it twice in the examples chapter.

## Looking after volumes

List them (`ls` means list, always):

```bash
docker volume ls
```

Peek at where one physically lives and how big it is:

```bash
docker volume inspect my-notes
```

Say goodbye forever, only if ready:

```bash
docker volume rm my-notes
```

(Do that only when you're done experimenting — it really does delete the
data. Try it with `my-notes`, it was just a hello.)

## Naming habit from this chapter forward

Volume names like `ollama-models` and `open-webui-data` appear in the
examples chapter. Names without slashes, lowercase, with dashes if needed.
Same habit for containers. Future-you, moving through `docker ps` and
`docker volume ls`, will send you a thank-you note.
