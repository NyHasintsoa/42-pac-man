# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_parser.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 13:26:44 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 19:17:07 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import re
from pathlib import Path

from pydantic import ValidationError

from src.exception import ConfigError
from src.model import GameConfig


class ConfigParser:
    @staticmethod
    def _strip_comments(json_str: str) -> str:
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
        try:
            path = Path(file_path)
            if not path.is_file():
                raise FileNotFoundError(
                    f"Configuration file target does not exist: '{file_path}'"
                )
            raw_data = path.read_text(encoding="utf-8")
            sanitized_json = ConfigParser._strip_comments(raw_data)
            return GameConfig.parse_json(sanitized_json)
        except FileNotFoundError:
            raise ConfigError(f"Configuration file '{file_path}' not found.")
        except PermissionError:
            raise ConfigError(f"Permission denied when trying \
to read '{file_path}'.")
        except ValidationError as e:
            raise ConfigError(e.errors())
        except Exception as e:
            raise ConfigError(e)
