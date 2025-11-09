.DEFAULT_GOAL := run

.PHONY: all format check fix typecheck test run

all: format check typecheck test

format:
	uv run ruff format .

check:
	uv run ruff check .

fix:
	uv run ruff check --fix .

typecheck:
	uv run ty check

test:
	uv run pytest

run:
	uv run strenpy
