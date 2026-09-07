"""Load game configuration files with comments removed."""

import re
from pathlib import Path

from pydantic import ValidationError

from src.exception import ConfigError
from src.model import GameConfig


class ConfigParser:
    """Parse configuration files into validated game settings."""

    @staticmethod
    def _strip_comments(json_str: str) -> str:
        """Remove line and block comments from JSON-like configuration text.

        Args:
            json_str: The JSON configuration text to parse.

        Returns:
            The configuration text without comments.
        """
        json_str = re.sub(r"/\*.*?\*/", "", json_str, flags=re.DOTALL)

        clean_lines = []
        for line in json_str.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            line = re.sub(r"(?<!:)\s*(?://|#).*$", "", line)
            clean_lines.append(line)
        return "\n".join(clean_lines)

    @staticmethod
    def parse_file(file_path: str) -> GameConfig:
        """Load and validate a game configuration from a file.

        Args:
            file_path: The configuration file path to read.

        Returns:
            A validated GameConfig instance.
        """
        try:
            path = Path(file_path)
            if not path.is_file():
                raise ConfigError(
                    f"Configuration file '{file_path}' not found."
                )
            raw_data = path.read_text(encoding="utf-8")
            sanitized_json = ConfigParser._strip_comments(raw_data)
            return GameConfig.parse_json(sanitized_json)
        except PermissionError as error:
            raise ConfigError(
                f"Permission denied when trying to read '{file_path}'."
            ) from error
        except OSError as error:
            raise ConfigError(
                f"Unable to read configuration file '{file_path}'."
            ) from error
        except ValidationError as error:
            raise ConfigError(
                f"Invalid configuration in '{file_path}': {error}"
            ) from error
