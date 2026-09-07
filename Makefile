# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: nramalan <nramalan@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/04 16:13:37 by nramalan          #+#    #+#              #
#    Updated: 2026/09/07 18:26:40 by nramalan         ###   ########.fr        #
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

FLAKE8_EXCLUDE_LINT := $(VENV),.cache,build,dist,assets

#----------------------------------------------
# Main Commands
#----------------------------------------------
.PHONY: install
install: $(VENV)
	echo "Installing project and its dependencies"
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
	echo "Cleaning project"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

.PHONY: lint
lint: $(VENV)
	echo "Check Project Types"
	$(FLAKE8) . --exclude $(FLAKE8_EXCLUDE_LINT)
	$(MYPY) . --warn-return-any --warn-unused-ignores \
			--ignore-missing-imports --disallow-untyped-defs \
			--check-untyped-defs

.PHONY: lint-strict
lint-strict: $(VENV)
	echo "Check Project Types Strict Mode"
	$(FLAKE8) . --exclude $(FLAKE8_EXCLUDE_LINT)
	$(MYPY) . --strict

.PHONY: package
package:
	echo "Syncing dependencies with uv..."
	$(UV) sync
	echo "Building standalone executable..."
	$(UV) run pyinstaller pac-man.spec --noconfirm --clean --distpath dist/pac-man
	echo "Adding minimal instructions..."
	echo "==================================================" > dist/pac-man/README.txt
	echo "                 PAC-MAN CONTROLS                 " >> dist/pac-man/README.txt
	echo "==================================================" >> dist/pac-man/README.txt
	echo "• Movement    : WASD / Arrow Keys" >> dist/pac-man/README.txt
	echo "• Options     : ESC" >> dist/pac-man/README.txt
	echo "• Select      : Enter / Space" >> dist/pac-man/README.txt
	echo "• Config      : Edit config.json in root directory" >> dist/pac-man/README.txt
	echo "Archiving package with tar..."
	tar -czvf pacman-desktop.tar.gz -C dist pac-man
	echo "Build complete: pacman-desktop.tar.gz"

#----------------------------------------------
# Dependencies
#----------------------------------------------
$(VENV): lib/mazegenerator-2.1.0-py3-none-any.whl
	echo "Creating virtual environment and installing dependencies"
	$(UV) venv
	UV_CACHE_DIR=$(FT_CACHE_DIR)/uv \
	$(UV) sync
