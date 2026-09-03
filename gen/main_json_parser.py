import sys
import re
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field, ValidationError


def strip_comments(json_str: str) -> str:
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)

    clean_lines = []
    for line in json_str.splitlines():
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith('//'):
            continue
        line = re.sub(r'(?<!:)\s*(?://|#).*$', '', line)
        clean_lines.append(line)
    return '\n'.join(clean_lines)


class LevelConfig(BaseModel):
    width: int = 28
    height: int = 36


class GameConfig(BaseModel):
    highscore_filename: str = "highscores.json"
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90
    levels: List[LevelConfig] = Field(default_factory=lambda: [LevelConfig()])


def load_config_from_file(file_path: str) -> GameConfig:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(
            f"Configuration file target does not exist: '{file_path}'"
        )
    raw_data = path.read_text(encoding="utf-8")
    sanitized_json = strip_comments(raw_data)
    return GameConfig.model_validate_json(sanitized_json, strict=True)


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: python config_parser.py <path_to_config.json>",
            file=sys.stderr
        )
        sys.exit(1)
    config_file_input = sys.argv[1]
    try:
        config = load_config_from_file(config_file_input)
        print("--- Configuration Parsed Successfully ---")
        print(f"Highscore Storage File: {config.highscore_filename}")
        print(f"Player Lives: {config.lives}")
        print(f"Default Target Packgums: {config.pacgum}")
        print("Point Scale (Ghost / Super / Regular):", end=" ")
        print(f"{config.points_per_ghost}", end=" / ")
        print(f"{config.points_per_super_pacgum}", end=" / ")
        print(f"{config.points_per_pacgum}")
        print(f"Random Engine Seed: {config.seed}")
        print(f"Maximum Level Delta-Time: {config.level_max_time}s")
        print(f"Total Registered Levels: {len(config.levels)}")
        for idx, lvl in enumerate(config.levels, start=1):
            print(f"  -> Level {idx}: Dimensions = {lvl.width}x{lvl.height}")

    except ValidationError as error:
        print(f"Validation Error: {error.errors()}", file=sys.stderr)
        sys.exit(1)
    except Exception as error:
        print(f"Error loading configuration: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
