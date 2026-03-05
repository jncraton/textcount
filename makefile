SHELL := /bin/bash

.PHONY: all test serve lint clean

all: test

serve:
	python3 -m http.server 8000

test:
	python3 -m pytest -q

lint:
	echo "no linter configured"

clean:
	rm -f .pytest_cache
