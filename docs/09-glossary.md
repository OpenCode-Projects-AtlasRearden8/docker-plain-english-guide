# Appendix: A Gentle Glossary

Words you'll meet in Docker tutorials, explained the way a friend would.
Words in *italics* are defined elsewhere in this list.

**bind mount**
A folder from *your* computer, plugged into a *container* so both see the
same files. Contrast with a *volume*.

**CLI**
Command-line interface — typing commands in a terminal instead of clicking
buttons. You already use one; Docker's commands are its CLI.

**compose**
The part of Docker that reads one `compose.yaml` file and runs a whole
*flock* of *containers* together. Commands look like `docker compose up`.

**container**
A running instance of an *image* — the cake to the image's recipe. It has its
own private workspace and disappears cleanly when removed.

**daemon**
The quiet background process that actually does Docker's work. When something
says "cannot connect to the Docker daemon", it means this helper isn't
running — on Windows/Mac, open Docker Desktop; on Linux, `sudo systemctl
start docker`.

**detached mode (`-d`)**
Running a *container* so it keeps working in the background and your terminal
stays yours. The opposite of "attached" mode, where logs scroll in your face.

**Docker Desktop**
The free Windows/Mac app that runs Docker for you — installer, settings
panel, and the hidden Linux world behind the curtain all in one.

**Docker Hub**
The big public *registry* at hub.docker.com — the default place `docker run`
downloads images from.

**environment variable**
A named setting you hand a program when it starts, like
`OLLAMA_BASE_URL=http://ollama:11434`. Think of it as a sticky note passed in
at the door.

**exec**
Run a command inside an already-running *container*:
`docker exec ollama ollama pull llama3.2:1b`.

**image**
A frozen, downloadable recipe: a program plus everything it needs, ready to
become a *container*. Images sit quietly until used, can be re-downloaded any
time, and can never contain your personal data by surprise.

**kernel**
The deep core of an operating system that talks to hardware. *Containers* on
your machine share your Linux kernel; a *virtual machine* brings its own.

**named volume**
A *volume* with a label you chose (`ollama-models`) instead of a serial
number. Both survive *container* removal; the named kind is easy to
recognize in `docker volume ls`.

**port** / **port mapping**
A numbered doorway for network traffic (8080, 3000). A *mapping* like
`"3000:8080"` means traffic to port 3000 on *your* computer gets forwarded
to port 8080 *inside that container*. Always write it with quotes in
*compose* files.

**prune**
To trim off what's clearly unused. Docker's cleanup commands (`docker
container prune`, `docker image prune`, …) remove only unattached things.

**registry**
An app store for *images* — Docker Hub, GitHub's `ghcr.io`, or one your
company runs. A slash in an image name (`ollama/ollama`) names the author
within the registry.

**service**
One entry in a *compose* file: a named long-term role ("the ollama service")
that Docker keeps running as one or more *containers*.

**stack**
A related group of services managed together from one compose file — in this
manual, Ollama plus Open WebUI is "the local AI stack".

**tag**
A version label on an *image* (`:main`, `:1b`, `:latest`). No tag means
"latest".

**terminal**
The dark window where you type commands. On Mac it's called Terminal; on
Windows people often use PowerShell or the one inside Docker Desktop; on
Linux, whatever ships with your distribution.

**volume**
Docker-managed storage that lives *outside* any container and survives
container deletion. How models and chat history survive tool updates.

**virtual machine (VM)**
A full simulated computer, complete with its own operating system — heavier
and slower than a *container*, but useful for running entirely different
operating systems side by side.

**YAML**
The tidy, indentation-based file format of `compose.yaml`. Two spaces of
indent, colon after names, quotes around port mappings — that's 90% of what
you'll ever need.
