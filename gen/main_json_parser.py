import sys
import re
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field


# --- 1. Comment Stripping Logic ---
def strip_comments(json_str: str) -> str:
    """
    Removes shell-style (#), single-line C-style (//), and multi-line C-style (/* */)
    comments from a raw string configuration.
    """
    # Remove multi-line comments: /* content */
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)

    clean_lines = []
    for line in json_str.splitlines():
        stripped = line.strip()
        # Ignore lines entirely dedicated to comments
        if stripped.startswith('#') or stripped.startswith('//'):
            continue

        # Inline comment removal (strips trailing comments if they aren't inside a string protocol)
        line = re.sub(r'(?<!:)\s*(?://|#).*$', '', line)
        clean_lines.append(line)

    return '\n'.join(clean_lines)


# --- 2. Pydantic Game Configurations Models ---
class LevelConfig(BaseModel):
    """Configuration schema for individual map levels."""
    width: int = 28
    height: int = 36


class GameConfig(BaseModel):
    """Root structure containing game configuration parameters and fallback states."""
    highscore_filename: str = "highscore.txt"
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90

    # Defaults to a basic list containing one standard configuration level if omitted
    levels: List[LevelConfig] = Field(default_factory=lambda: [LevelConfig()])


# --- 3. Parsing and Argument Execution Flow ---
def load_config_from_file(file_path: str) -> GameConfig:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file target does not exist: '{file_path}'")

    raw_data = path.read_text(encoding="utf-8")
    sanitized_json = strip_comments(raw_data)

    return GameConfig.model_validate_json(sanitized_json)


def main() -> None:
    # Enforce file input through argument parameters
    if len(sys.argv) < 2:
        print("Usage: python config_parser.py <path_to_config.json>", file=sys.stderr)
        sys.exit(1)

    config_file_input = sys.argv[1]

    try:
        config = load_config_from_file(config_file_input)
        print("--- Configuration Parsed Successfully ---")
        print(f"Highscore Storage File: {config.highscore_filename}")
        print(f"Player Lives: {config.lives}")
        print(f"Default Target Packgums: {config.pacgum}")
        print(f"Point Scale (Ghost / Super / Regular): {config.points_per_ghost} / {config.points_per_super_pacgum} / {config.points_per_pacgum}")
        print(f"Random Engine Seed: {config.seed}")
        print(f"Maximum Level Delta-Time: {config.level_max_time}s")
        print(f"Total Registered Levels: {len(config.levels)}")
        for idx, lvl in enumerate(config.levels, start=1):
            print(f"  -> Level {idx}: Dimensions = {lvl.width}x{lvl.height}")

    except Exception as error:
        print(f"Error loading configuration: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
