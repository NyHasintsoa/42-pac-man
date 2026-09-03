# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: nramalan <nramalan@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/04 16:13:37 by nramalan          #+#    #+#              #
#    Updated: 2026/05/04 16:54:54 by nramalan         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

VENV := .venv

UV := @uv
PYTHON := $(UV) run python
PDB := $(UV) run python -m pdb
FLAKE8 := $(UV) run flake8
MYPY := $(UV) run mypy

.DEFAULT_GOAL := run

#----------------------------------------------
# Main Commands
#----------------------------------------------
.PHONY: install
install: $(VENV)
	@echo "Installing project and its dependencies"
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

.PHONY: lint
lint: $(VENV)
	@echo "Check Project Types"
	$(FLAKE8) . --exclude $(VENV)
	$(MYPY) . --warn-return-any --warn-unused-ignores \
			--ignore-missing-imports --disallow-untyped-defs \
			--check-untyped-defs --exclude $(VENV)

.PHONY: lint-strict
lint-strict: $(VENV)
	@echo "Check Project Types Strict Mode"
	$(FLAKE8) . --exclude $(VENV)
	$(MYPY) . --strict --exclude $(VENV)

#----------------------------------------------
# Dependencies
#----------------------------------------------
$(VENV):
	@echo "Creating virtual environment and installing dependencies"
	$(UV) venv
	$(UV) sync
