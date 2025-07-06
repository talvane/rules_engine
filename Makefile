PROJECT_NAME="rules-engine"

# @scf-region env-vars
export PYTHONDONTWRITEBYTECODE=1
export ENVIRONMENT=DEVELOPMENT
export PYTHONPATH=$(shell pwd)/
# @end-scf-region

.PHONY=help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean: ## Remove cache files
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf

###
# Dependencies section
###
_base_pip:
	@pip install -U pip wheel poetry

_base_poetry:
	@poetry install

dev-dependencies: _base_pip _base_poetry ## Install development dependencies

dependencies: _base_pip ## Install dependencies
	@poetry install --only main

outdated: ## Show outdated packages
	@poetry show --outdated

###
# Lint section
# @scf-region lint
###
_ruff:
	@poetry run ruff format --check .
	@poetry run ruff check .

_ruff-fix:
	@poetry run ruff format .
	@poetry run ruff check --fix .

_dead_fixtures:
	@poetry run pytest --dead-fixtures src/

_mypy:
	@poetry run mypy src/

pre-commit:
	@poetry run pre-commit run --all-files

lint: _ruff _mypy   ## Check code lint
format-code: _ruff-fix ## Format code
# @end-scf-region

###
# Tests section
###
test: clean ## Run tests
	@pytest src/ -m "not integration_test"

test-coverage: clean ## Run tests with coverage output
	@pytest src/ --cov src/ --cov-report term-missing --cov-report xml:coverage/pycoverage.xml -m "not integration_test"

test-debug: clean ## Run tests with active ipdb
	@poetry run pytest -s -x test/*

test-matching: clean ## Run tests by match ex: make test-matching k=name_of_test
	@poetry run pytest -s -k $(k) test/
