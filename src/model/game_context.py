from typing import List, TypeAlias

from pydantic import BaseModel, ConfigDict, Field

from src.model.game_config import GameConfig
from src.model.pacgum import Pacgums

MazeData: TypeAlias = List[List[int]]


class GameContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: GameConfig
    current_level: int = 0
    maze_levels: List[MazeData] = Field(default_factory=list)
    pacgums: List[Pacgums] = Field(default_factory=list)
    score: int = 0
    lives: int = 3
    time_elapsed: int = 0
    is_winner: bool = False
