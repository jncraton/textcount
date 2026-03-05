SHELL := /bin/bash

.PHONY: all test serve lint clean

all: test

serve:
	python3 -m http.server 8000

test:
	uv run --with pytest-playwright==0.7.2 python -m playwright install chromium
	uv run --with pytest-playwright==0.7.2 python -m pytest --browser chromium

lint:
	echo "no linter configured"

clean:
	rm -f .pytest_cache
