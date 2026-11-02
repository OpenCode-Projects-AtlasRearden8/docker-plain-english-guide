PY ?= python3

.PHONY: build serve test check clean

build:
	$(PY) build.py

serve: build
	$(PY) -m http.server 8787 --directory site

test:
	$(PY) -m pytest tests/ -q

check: test
	$(PY) -m pytest tests/ -q && echo "ALL CHECKS PASSED"

clean:
	rm -rf site .pytest_cache
