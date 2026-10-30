.PHONY: test demo run dashboard lint fmt typecheck clean

PYTHON ?= python3

test:
	$(PYTHON) -m unittest discover -s tests -t . -v

run:
	$(PYTHON) -m solaris.cli --prompt "Propón una política de cuidado del agua" --trace out.json

demo:
	bash scripts/run_demo.sh

dashboard:
	@echo "Abre http://localhost:8000/apps/dashboard/ y carga data/traces/demo.json"
	$(PYTHON) -m http.server 8000

lint:
	ruff check .

fmt:
	ruff format .

typecheck:
	mypy solaris

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
