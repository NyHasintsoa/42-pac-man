# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_context.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 16:10:07 by nramalan        #+#    #+#               #
#  Updated: 2026/07/10 18:59:03 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List, Optional, Tuple

from pydantic import BaseModel, ConfigDict, Field

from src.model.game_config import GameConfig
from src.model.pacgum import SimplePacgum, SuperPacgum


class LevelData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    width: int = Field()
    height: int = Field()
    maze_data: List[List[int]] = Field()
    pacgums: Tuple[List[SuperPacgum], List[SimplePacgum]] = Field(
        default_factory=lambda: ([], [])
    )


class GameContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config: Optional[GameConfig] = None
    levels: List[LevelData] = Field(default_factory=list)
    current_level: int = 0
    maze_level: List[List[int]] = Field(default_factory=list)
    pacgums: Tuple[List[SuperPacgum], List[SimplePacgum]] = Field(
        default_factory=lambda: ([], [])
    )
    score: int = 0
    lives: int = 3
    time_elapsed: int = 0
    is_paused: bool = False
    game_running: bool = True
