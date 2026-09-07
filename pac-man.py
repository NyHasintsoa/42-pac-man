"""Run the Pac-Man game from a configuration file."""

import sys

from src.exception import ArgsError
from src.graphic.main_window import MainWindow
from src.service import ConfigParser


def main() -> None:
    """Start the game using the configuration.

    Returns:
        The requested result.
    """
    if len(sys.argv) <= 1:
        raise ArgsError("Usage: python3 ./pac-man.py <config_file>")
    config = ConfigParser.parse_file(sys.argv[1])
    window = MainWindow(1177, 920, config, "pac-man")
    window.add_event()
    window.load_page()
    window.render()


if __name__ == "__main__":
    main()
