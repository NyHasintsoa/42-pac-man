"""Run the Pac-Man game from a configuration file."""

import sys
from typing import Optional, Sequence

from src.exception import ApplicationError, ArgsError, PacmanError
from src.graphic.main_window import MainWindow
from src.service import ConfigParser


def _run(arguments: Sequence[str]) -> None:
    """Run the game and convert unexpected failures to project errors.

    Args:
        arguments: Command-line arguments excluding the executable name.

    Raises:
        ArgsError: If more than one configuration path is provided.
        PacmanError: If the game cannot be started or run.
    """
    if len(arguments) > 1:
        raise ArgsError("Usage: uv run python pac-man.py [config-file]")

    config_file = arguments[0] if arguments else "config.json"
    window = None
    try:
        config = ConfigParser.parse_file(config_file)
        window = MainWindow(1177, 920, config, "pac-man")
        window.add_event()
        window.load_page()
        window.render()
    except PacmanError:
        raise
    except Exception as error:
        raise ApplicationError("The game could not be started.") from error
    finally:
        if window is not None:
            window.close()


def main(arguments: Optional[Sequence[str]] = None) -> int:
    """Start the game using the configuration.

    Returns:
        The requested result.
    """
    command_arguments = sys.argv[1:] if arguments is None else arguments
    try:
        _run(command_arguments)
    except KeyboardInterrupt:
        print("Game interrupted.", file=sys.stderr)
        return 130
    except PacmanError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
