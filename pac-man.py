"""Module entrypoint for Pac-Man with granular error handling.

Provides top-level CLI execution and distinct handling for domain-specific
Pac-Man exceptions, terminal interrupts, and unexpected errors.
"""

import sys
from typing import Sequence

from src.exception import (
    ConfigError,
    PacmanError,
    ScoreError,
)
from src.graphic.main_window import MainWindow
from src.service import ConfigParser

COLOR_RED = "\033[31m"
COLOR_YELLOW = "\033[33m"
COLOR_RESET = "\033[0m"


def print_cli_error(
    category: str, details: object, color: str = COLOR_RED
) -> None:
    """Print styled, categorized error messages to standard error.

    Args:
        category: Descriptive category label for the intercepted error.
        details: Exception details, message, or printable object.
        color: ANSI escape sequence used for terminal styling. Defaults to
          COLOR_RED.
    """
    sys.stderr.write(f"{color}[{category}]{COLOR_RESET} {details}\n")


def _run(arguments: Sequence[str]) -> None:
    """Execute game setup and rendering.

    Args:
        arguments: Command-line arguments excluding executable name.

    Raises:
        ArgsError: If invalid arguments are provided.
    """
    config_file = arguments[0] if arguments else "config.json"
    window = None
    try:
        config = ConfigParser.parse_file(config_file)
        window = MainWindow(1177, 920, config, "Pac-Man")
        window.add_event()
        window.load_page()
        window.render()
    finally:
        if window is not None:
            window.close()


def main() -> None:
    """Start the Pac-Man application with granular error handling.

    Catches individual subclass exceptions to print distinct category tags
    and status messages before exiting.
    """
    try:
        _run(sys.argv[1:])
    except ConfigError as err:
        print_cli_error("Configuration Error", err)
        sys.exit(1)
    except ScoreError as err:
        print_cli_error("Score Error", err)
        sys.exit(1)
    except PacmanError as err:
        print_cli_error("Pac-Man Application Error", err)
        sys.exit(1)
    except KeyboardInterrupt:
        print_cli_error(
            "Interrupt", "Operation cancelled by user.", color=COLOR_YELLOW
        )
        sys.exit(130)
    except Exception as err:
        print_cli_error(
            "Unexpected Fatal Exception", f"{type(err).__name__}: {err}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
