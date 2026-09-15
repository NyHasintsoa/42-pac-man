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

PACKAGE_NAME := pacman-desktop.tar.gz
SPEC_NAME := pac-man.spec

FLAKE8_EXCLUDE_LINT := $(VENV),.cache,build,dist,assets

##----------------------------------------------
## Main Commands
##----------------------------------------------
.PHONY: install
install: $(VENV) ## Create the venv and install project dependencies
	echo "Installing project and its dependencies"
	$(UV) sync

.PHONY: run
run: $(VENV) ## Launch the game with the default config
	$(PYTHON) pac-man.py config.json

.PHONY: debug
debug: $(VENV) ## Start the game in pdb for debugging
	$(PDB) pac-man.py config.json

.PHONY: clean
clean: ## Remove Python caches and generated build folders
	echo "Cleaning project"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build dist

.PHONY: fclean
fclean: clean ## Remove temporary build artifacts and the packaged archive
	echo "Cleaning build and dist folders ... 🗑️"
	rm -f $(PACKAGE_NAME)

.PHONY: lint
lint: $(VENV) ## Run flake8 and mypy checks on the project
	echo "Check Project Types"
	$(FLAKE8) . --exclude $(FLAKE8_EXCLUDE_LINT)
	$(MYPY) . --warn-return-any --warn-unused-ignores \
			--ignore-missing-imports --disallow-untyped-defs \
			--check-untyped-defs

.PHONY: lint-strict
lint-strict: $(VENV) ## Run strict linting with mypy in strict mode
	echo "Check Project Types Strict Mode"
	$(FLAKE8) . --exclude $(FLAKE8_EXCLUDE_LINT)
	$(MYPY) . --strict

.PHONY: build
build: $(VENV) ## Build the distributable package with PyInstaller
	echo "Syncing dependencies with uv..."
	$(UV) sync
	echo "Building standalone executable..."
	rm -rf build dist
	$(UV) run pyinstaller $(SPEC_NAME) --noconfirm --clean --distpath dist
	echo "Copying external configuration files beside executable..."
	cp config.json dist/pac-man/config.json
	echo "Adding minimal instructions..."
	echo "==================================================" > dist/pac-man/README.txt
	echo "                 PAC-MAN CONTROLS                 " >> dist/pac-man/README.txt
	echo "==================================================" >> dist/pac-man/README.txt
	echo  "Movement    : WASD / Arrow Keys" >> dist/pac-man/README.txt
	echo  "Select      : Enter / Space" >> dist/pac-man/README.txt
	echo  "Pause/Menu  : ESC" >> dist/pac-man/README.txt
	echo  "" >> dist/pac-man/README.txt
	echo  "==================================================" >> dist/pac-man/README.txt
	echo  "                   CONFIGURATION                  " >> dist/pac-man/README.txt
	echo  "==================================================" >> dist/pac-man/README.txt
	echo  "- Game settings, speeds, and level seeds can be modified " >> dist/pac-man/README.txt
	echo  "by editing 'config.json' located in this directory." >> dist/pac-man/README.txt
	echo  "- High scores are saved automatically to 'highscores.json'." >> dist/pac-man/README.txt
	echo "Archiving package with tar..."
	tar -czvf $(PACKAGE_NAME) -C dist pac-man
	echo "Build complete: $(PACKAGE_NAME)"

##----------------------------------------------
## Other Commands
##----------------------------------------------
.PHONY: help
help: ## List usefull commands
	@grep -E '(^[a-zA-Z0-9_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}{printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'


#----------------------------------------------
# Dependencies
#----------------------------------------------
$(VENV): lib/mazegenerator-2.1.0-py3-none-any.whl
	echo "Creating virtual environment and installing dependencies"
	$(UV) venv
	$(UV) sync
