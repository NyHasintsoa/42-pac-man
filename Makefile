.SILENT:

VENV := .venv

FT_CACHE_DIR := $(PWD)/.cache

export UV_CACHE_DIR := $(FT_CACHE_DIR)/uv
export PYINSTALLER_CONFIG_DIR := $(FT_CACHE_DIR)/pyinstaller

UV := uv
PYTHON := $(UV) run python
PDB := $(PYTHON) -m pdb
FLAKE8 := $(UV) run flake8
MYPY := $(UV) run mypy

.DEFAULT_GOAL := run

PACKAGE_NAME := pacman-desktop.zip

FLAKE8_EXCLUDE_LINT := $(VENV),.cache,build,dist,assets

#----------------------------------------------
# Main Commands
#----------------------------------------------
.PHONY: install
install: $(VENV)
	echo "Installing project and its dependencies"
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
	rm -rf build dist

.PHONY: fclean
fclean: clean
	echo "Cleaning build and dist folders ... 🗑️"
	rm -f $(PACKAGE_NAME) pac-man.spec

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
	rm -rf build dist
	$(UV) run pyinstaller --noconfirm --clean --distpath dist \
		--onedir \
		--windowed \
		--name pac-man \
		--add-data "assets:assets" \
		--add-data "lib:lib" \
		pac-man.py
	rm -f pac-man.spec
	echo "Copying external configuration files beside executable..."
	cp config.json dist/pac-man/config.json
	echo "Adding minimal instructions..."
	echo "==================================================" > dist/pac-man/README.txt
	echo "                 PAC-MAN CONTROLS                 " >> dist/pac-man/README.txt
	echo "==================================================" >> dist/pac-man/README.txt
	echo "Movement    : WASD / Arrow Keys" >> dist/pac-man/README.txt
	echo "Options     : ESC" >> dist/pac-man/README.txt
	echo "Select      : Enter / Space" >> dist/pac-man/README.txt
	echo "Config      : Edit config.json beside the executable" >> dist/pac-man/README.txt
	echo "Archiving package with zip..."
	cd dist && zip -r ../$(PACKAGE_NAME) pac-man
	echo "Build complete: $(PACKAGE_NAME)"

#----------------------------------------------
# Dependencies
#----------------------------------------------
$(VENV): lib/mazegenerator-2.1.0-py3-none-any.whl
	echo "Creating virtual environment and installing dependencies"
	$(UV) venv
	$(UV) sync