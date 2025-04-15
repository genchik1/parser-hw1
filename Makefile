# Makefile
.PHONY: lint test test-cov
fmt:
	ruff format
	ruff check --fix

lint:
	pre-commit run --all-files

test:
	pytest tests

build:
	docker build -t app .

run:
	docker run -v ./:/app/ app

run_with_config:
	docker run -v ./:/app/ app --config config.ini
