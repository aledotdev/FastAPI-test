.DEFAULT_GOAL := help

.PHONY: help all run shell test checks

ARCH = $(shell uname -m)

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

all: install hooks-check run  ## Setup and run the project

requirements_flag: poetry.lock
	pip install poetry
	poetry install --with dev
	pre-commit install

run: requirements_flag ## Run flask project in debug mode
	uvicorn event_provider.main:app --reload

init_test_db: ## Init (and drop the old DB) a local database with a test provider
	python -m commands.init_db --dropall
	python -m commands.create_test_provider

sync_events: ## Start Providers Events task
	python -m commands.start_providers_event_sync

cmd: requirements_flag ## Run flask project in debug mode
	python -m commands.$(args)

test: requirements_flag ## Run tests
	ENV=test python -m pytest tests/ $(args)

hooks-check: ## Run all hooks against all files
	@pre-commit run --all-files

style: ## Run code styles (black, isort)
	black .
	isort ./tests/ ./event_provider/ ./commands/
