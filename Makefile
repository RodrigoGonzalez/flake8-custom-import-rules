# =============================================================================
# MAKEFILE FOR CUSTOM IMPORT RULES
# =============================================================================
#
# Partially inspired by https://github.com/johschmidt42/python-project-johannes
#
# To do stuff with make, you type `make` in a directory that has a file called
# "Makefile". You can also type `make -f <makefile>` to use a different filename.
#
# A Makefile is a collection of rules. Each rule is a recipe to do a specific
# thing, sort of like a grunt task or an npm package.json script.
#
# A rule looks like this:
#
# <target>: <prerequisites...>
# 	<commands>
#
# The "target" is required. The prerequisites are optional, and the commands
# are also optional, but you have to have one or the other.
#
# Type `make` to show the available targets and a description of each.
#

# =============================================================================
# GLOBAL VARIABLES
# =============================================================================

PROJECTNAME := $(shell basename "$(PWD)")
PYTHON_INTERPRETER := python3.10

.SILENT: ;               # no need for @

# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

##@ Environment

setup: poetry-install pre-commit-install  ## Setup Virtual Environment

    poetry-install:  ## Install dependencies using Poetry
		poetry env use $(PYTHON_INTERPRETER)
		poetry install
		# pip install -e .

    pre-commit-install:  ## Install pre-commit hooks
		poetry run pre-commit install

update-deps: pip-upgrade poetry-update pre-commit-autoupdate  ## Update dependencies

    pip-upgrade:  ## Upgrade pip
		poetry run pip install --upgrade pip

    poetry-update:  ## Update Poetry dependencies
		poetry update
		poetry lock

    pre-commit-autoupdate:  ## Update pre-commit hooks
		poetry run pre-commit autoupdate -c .pre-commit-config.yaml

local: setup update-deps  ## Locally install the package
	custom-imports --help

.PHONY: setup update-deps local

# =============================================================================
# DEVELOPMENT
# =============================================================================

##@ Development

# Get the list of changed files
changed_files = $(shell git diff --name-only --diff-filter=d $$(git merge-base HEAD origin/main))

# Filter only Python files
changed_py_files = $(filter %.py, $(changed_files))

pre-commit:  ## Manually run all pre-commit hooks
	# not added to `pre-commit-tool` in order to prevent unwanted behavior when running in workflows
	git add -A
	poetry run pre-commit run -c .pre-commit-config.yaml
	#poetry run pre-commit run --all-files -c .pre-commit-config.yaml

pre-commit-tool:  ## Manually run a single pre-commit hook (e.g. `make pre-commit-tool TOOL=black`)
	poetry run pre-commit run --hook-stage manual $(TOOL) -c .pre-commit-config.yaml
	#poetry run pre-commit run $(TOOL) --all-files -c .pre-commit-config.yaml

# https://commitizen-tools.github.io/commitizen/bump/
commit: pre-commit tests clean  ## Commit changes
	./scripts/commit.sh

bump:  ## Bump version and update changelog
	poetry run cz bump --changelog --check-consistency --annotated-tag
	git push --follow-tags

.PHONY: pre-commit pre-commit-tool commit bump

# =============================================================================
# FORMATTING
# =============================================================================

##@ Formatting

format: format-black format-isort format-autoflake format-pyupgrade  ## Run all formatters

format-black: ## Run black (code formatter)
	$(MAKE) pre-commit-tool TOOL=black

format-isort: ## Run isort (import formatter)
	$(MAKE) pre-commit-tool TOOL=isort

format-autoflake: ## Run autoflake (remove unused imports)
	$(MAKE) pre-commit-tool TOOL=autoflake

format-pyupgrade: ## Run pyupgrade (upgrade python syntax)
	$(MAKE) pre-commit-tool TOOL=pyupgrade

.PHONY: format format-black format-isort format-autoflake format-pyupgrade

# =============================================================================
# LINTING
# =============================================================================

##@ Linting

lint: lint-black lint-isort lint-flake8 lint-mypy ## Run all linters

.PHONY: lint lint-black lint-isort lint-flake8 lint-mypy

lint-black: ## Run black in linting mode
	$(MAKE) pre-commit-tool TOOL=black-check

lint-isort: ## Run isort in linting mode
	$(MAKE) pre-commit-tool TOOL=isort-check

lint-flake8: ## Run flake8 (linter)
	$(MAKE) pre-commit-tool TOOL=flake8

lint-mypy: ## Run mypy (static-type checker)
	$(MAKE) pre-commit-tool TOOL=mypy

lint-mypy-report: ## Run mypy & create report
	poetry run mypy --install-types --non-interactive --verbose --html-report ./.mypy_html_report src
	#$(MAKE) pre-commit-tool TOOL=mypy ARGS="--html-report ./mypy_html"

lint-mypy-changed:  ## Run mypy on changed Python files & create report
	$(if $(changed_py_files), poetry run mypy --install-types --non-interactive --verbose --html-report ./.mypy_html_report $(changed_py_files), echo "No changed Python files to lint.")

.PHONY: lint-mypy-report

# =============================================================================
# TESTING
# =============================================================================

##@ Testing

tox: ## run tox tests
	poetry run tox
	make clean

tests: unit-tests  ## run all tests

unit-tests: ## run unit-tests with pytest
	poetry run pytest  -vvvvsra --doctest-modules

unit-tests-cov: ## run unit-tests with pytest and show coverage (terminal + html)
	poetry run pytest  -vvvvsra --doctest-modules --cov=src --cov-report term-missing --cov-report=html

unit-tests-cov-fail: ## run unit tests with pytest and show coverage (terminal + html) & fail if coverage too low & create files for CI
	poetry run pytest  -vvvvsra --doctest-modules --cov=src --cov-report term-missing --cov-report=html --cov-fail-under=80 --junitxml=pytest.xml | tee pytest-coverage.txt

clean-cov: ## remove output files from pytest & coverage
	@rm -rf .coverage
	@rm -rf coverage.xml
	@rm -rf htmlcov
	@rm -rf pytest.xml
	@rm -rf pytest-coverage.txt
	@rm -rf dist

.PHONY: tox tests unit-tests unit-tests-cov unit-tests-cov-fail clean-cov

# =============================================================================
# DOCUMENTATION
# =============================================================================

##@ Documentation

docs-serve: ## serve documentation locally
	mkdocs serve

docs-build: ## build documentation locally
	mkdocs build

docs-deploy: ## build & deploy documentation to "gh-pages" branch
	mkdocs gh-deploy -m "docs: update documentation" -v --force

clean-docs: ## remove output files from mkdocs
	rm -rf site

.PHONY: docs-serve docs-build docs-deploy clean-docs

# =============================================================================
# BUILD & RELEASE
# =============================================================================

##@ Build & Release

clean: clean-docs  clean-cov  ## Clean package
	find . -type d -name '__pycache__' | xargs rm -rf
	find . -type d -name '.temp' | xargs rm -rf
	find . -type f -name '.coverage' | xargs rm -rf
	rm -rf build dist

build:  pre-commit tests clean ## Build the project
	poetry build

deploy:  ## Deploy to PyPI
	poetry publish --build

.PHONY: build deploy clean


# -----------------------------------------------------------------------------
# GIT
# -----------------------------------------------------------------------------

##@ Git Shortcuts

git-commit-num:
	@echo "+ $@"
	@echo $(shell git rev-list --all --count)

.PHONY: git-commit-num

current_branch := $(shell git symbolic-ref --short HEAD)

checkout-main:  ## Switch to main branch
	@echo "+ $@"
	if [ "$(current_branch)" != "main" ]; then \
		git checkout main; \
	fi
	git pull --all
	git fetch --tags

.PHONY: checkout-main

commit_count := $(shell git rev-list --all --count)

check-branch-name:
ifeq ($(BRANCH),)
	$(error BRANCH variable is not set. Please provide a branch name with BRANCH=mybranch)
endif

new-branch: check-branch-name  ## Create a new branch
	git checkout -b $(BRANCH)_$(commit_count)

new-feat-branch: check-branch-name  ## Create a new feature branch
	git checkout -b feat/$(BRANCH)_$(commit_count)

.PHONY: check-branch-name new-branch new-feat-branch

# =============================================================================
# ADDITIONAL
# =============================================================================

##@ Additional

# =============================================================================
# SELF DOCUMENTATION
# =============================================================================

.DEFAULT_GOAL := help
.PHONY: help
help:  ## Display this help
	echo
	echo " The following commands can be run for "$(PROJECTNAME)":"
	echo
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
