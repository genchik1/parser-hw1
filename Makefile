# Makefile
.PHONY: lint test test-cov
fmt:
	ruff format
	ruff check --fix

lint:
	pre-commit run --all-files

test:
	pytest tests
