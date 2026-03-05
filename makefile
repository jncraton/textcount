SHELL := /bin/bash

.PHONY: all test serve lint clean

all: test

serve:
	python3 -m http.server 8000

test:
	uv run --with pytest-playwright==0.7.2 python -m playwright install chromium
	uv run --with pytest-playwright==0.7.2 python -m pytest --browser chromium

lint:
	npx prettier@3.6.2 --check .
	
format:
	npx prettier@3.6.2 --write .

clean:
	rm -f .pytest_cache
