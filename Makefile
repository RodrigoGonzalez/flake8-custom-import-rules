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

PROJECT_NAME := $(shell basename "$(PWD)")
PYTHON_INTERPRETER := python3.10
UV_TEST_RUN ?= uv run --locked --group test

.SILENT: ;               # no need for @

# =============================================================================
# ENVIRONMENT SETUP
# =============================================================================

##@ Environment

setup: uv-sync pre-commit-install  ## Setup Virtual Environment

uv-sync:  ## Install dependencies using uv
	uv sync --python $(PYTHON_INTERPRETER) --all-groups

pre-commit-install:  ## Install pre-commit hooks
	uv run --locked pre-commit install

update-deps: uv-update pre-commit-autoupdate  ## Update dependencies

uv-update:  ## Update locked package versions within declared constraints
	uv lock --upgrade
	uv sync --all-groups

pre-commit-autoupdate:  ## Update pre-commit hooks
	uv run --locked pre-commit autoupdate -c .pre-commit-config.yaml

local: setup update-deps  ## Locally install the package
	uv run --locked import-rules --help

.PHONY: setup uv-sync pre-commit-install update-deps uv-update pre-commit-autoupdate local

# =============================================================================
# DEVELOPMENT
# =============================================================================

##@ Development

# Get the list of changed files
changed_files = $(shell git diff --name-only --diff-filter=d $$(git merge-base HEAD origin/main))

# Filter only Python files
changed_py_files = $(filter %.py, $(changed_files))

pre-commit:  check-readme ## Manually run all pre-commit hooks
	# not added to `pre-commit-tool` in order to prevent unwanted behavior when running in workflows
	git add -A
	uv run --locked pre-commit run -c .pre-commit-config.yaml

# https://commitizen-tools.github.io/commitizen/bump/
commit: pre-commit tests clean  ## Commit changes
	./scripts/commit.sh

bump:  ## Bump version and update changelog
	uv run --locked cz bump --changelog --check-consistency --annotated-tag --retry
	git push -u origin HEAD --follow-tags

dry-run-bump:  ## Generate the changes that would be made by bumping the version
	uv run --locked cz bump --dry-run

.PHONY: pre-commit commit bump dry-run-bump

# =============================================================================
# TESTING
# =============================================================================

##@ Testing

tox: ## tox.ini remains deferred to the compatibility migration
	echo "tox.ini remains coupled to the previous package manager and is intentionally deferred to the tox/Python compatibility migration."
	echo "Use the pytest targets for the current test suite."
	exit 2

tests: unit-tests  ## run all tests

unit-tests: ## run unit-tests with pytest
	$(UV_TEST_RUN) pytest  -vvvvsra --doctest-modules

unit-tests-cov: ## run unit-tests with pytest and show coverage (terminal + html)
	$(UV_TEST_RUN) pytest  -vvvvsra --doctest-modules --cov=src --cov-report term-missing --cov-report=html

unit-tests-cov-fail: ## run unit tests w/ pytest and coverage (terminal + html) & create files for CI
	$(UV_TEST_RUN) pytest  -vvvvsra --doctest-modules --cov=src --cov-report term-missing \
	--cov-report=xml --cov-fail-under=80 --junitxml=pytest.xml | tee pytest-coverage.txt

clean-cov: ## remove output files from pytest & coverage
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf htmlcov
	rm -rf pytest.xml
	rm -rf pytest-coverage.txt
	rm -rf dist

.PHONY: tox tests unit-tests unit-tests-cov unit-tests-cov-fail clean-cov

# =============================================================================
# DOCUMENTATION
# =============================================================================

##@ Documentation

check-readme: ## check README.rst rendering
	echo "Checking README.rst is rendering correctly."
	rst2html.py --halt=2 README.rst > /dev/null

docs-serve: ## serve documentation locally
	uv run --locked --group docs mkdocs serve

docs-build: ## build documentation locally
	uv run --locked --group docs mkdocs build

docs-deploy: ## build & deploy documentation to "gh-pages" branch
	uv run --locked --group docs mkdocs gh-deploy -m "docs: update documentation" -v --force

clean-docs: ## remove output files from mkdocs
	rm -rf site

.PHONY: check-readme docs-serve docs-build docs-deploy clean-docs

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
	uv build --no-sources

deploy: build  ## Deploy to PyPI
	uv publish

.PHONY: build deploy clean


# -----------------------------------------------------------------------------
# GIT
# -----------------------------------------------------------------------------

##@ Git Shortcuts

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

new-version-branch:  ## Create a new version branch
	NEW_VERSION=$(shell uv run --locked cz bump --dry-run | grep 'bump: version' | awk -F ' ' '{print $$NF}'); \
	git checkout -b v$$NEW_VERSION

.PHONY: check-branch-name new-branch new-feat-branch new-version-branch

# =============================================================================
# SELF DOCUMENTATION
# =============================================================================

.DEFAULT_GOAL := help
.PHONY: help
help:  ## Display this help
	echo
	echo " The following commands can be run for "$(PROJECT_NAME)":"
	echo
	awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ \
	{ printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' \
	$(MAKEFILE_LIST)
