"""Run the Pac-Man game from a configuration file."""

import sys

from src.graphic.main_window import MainWindow
from src.service import ConfigParser


def main() -> None:
    """Start the game using the configuration.

    Returns:
        The requested result.
    """
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"

    config = ConfigParser.parse_file(config_file)
    window = MainWindow(1177, 920, config, "pac-man")
    window.add_event()
    window.load_page()
    window.render()


if __name__ == "__main__":
    main()
