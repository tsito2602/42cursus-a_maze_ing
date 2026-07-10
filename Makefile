UV		:= uv
PYTHON	:= $(UV) run python
CONFIG	?= config.txt

install:
	$(UV) sync

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +

lint:
	$(UV) run flake8 .
	$(UV) run mypy . --warn-return-any --warn-unused-ignores \
			--ignore-missing-imports --disallow-untyped-defs \
			--check-untyped-defs

lint-strict:
	$(UV) run flake8 .
	$(UV) run mypy . --strict

test:
	$(UV) run pytest

build:
	$(UV) build --out-dir .

.PHONY: install run debug clean lint lint-strict test build
