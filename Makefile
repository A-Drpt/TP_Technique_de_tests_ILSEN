.PHONY: test unit_test perf_test coverage lint doc

test:
	pytest -q

unit_test:
	pytest -m "not perf" -q

perf_test:
	pytest -m perf -q

coverage:
	coverage run -m pytest
	coverage report -m

lint:
	ruff check .

doc:
	pdoc3 --html --output-dir docs triangulator
