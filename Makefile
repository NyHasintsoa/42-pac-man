# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: nramalan <nramalan@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/04 16:13:37 by nramalan          #+#    #+#              #
#    Updated: 2026/07/30 17:43:22 by nramalan         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

.SILENT:

VENV := .venv

FT_CACHE_DIR := $(PWD)/.cache

UV := uv
PYTHON := $(UV) run python
PDB := $(PYTHON) -m pdb
FLAKE8 := $(UV) run flake8
MYPY := $(UV) run mypy

.DEFAULT_GOAL := run

FLAKE8_EXCLUDE_LINT := $(VENV),.cache

#----------------------------------------------
# Main Commands
#----------------------------------------------
.PHONY: install
install: $(VENV)
	@echo "Installing project and its dependencies"
	UV_CACHE_DIR=$(FT_CACHE_DIR)/uv \
	$(UV) sync

.PHONY: run
run: $(VENV)
	$(PYTHON) pac-man.py config.json

.PHONY: debug
debug: $(VENV)
	$(PDB) pac-man.py config.json

.PHONY: clean
clean:
	@echo "Cleaning project"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name "*.egg-info" -exec rm -rf {} +

.PHONY: lint
lint: $(VENV)
	@echo "Check Project Types"
	$(FLAKE8) . --exclude $(FLAKE8_EXCLUDE_LINT)
	$(MYPY) . --warn-return-any --warn-unused-ignores \
			--ignore-missing-imports --disallow-untyped-defs \
			--check-untyped-defs

.PHONY: lint-strict
lint-strict: $(VENV)
	@echo "Check Project Types Strict Mode"
	$(FLAKE8) . --exclude $(FLAKE8_EXCLUDE_LINT)
	$(MYPY) . --strict

#----------------------------------------------
# Dependencies
#----------------------------------------------
$(VENV): lib/mazegenerator-2.1.0-py3-none-any.whl
	@echo "Creating virtual environment and installing dependencies"
	$(UV) venv
	UV_CACHE_DIR=$(FT_CACHE_DIR)/uv \
	$(UV) sync
