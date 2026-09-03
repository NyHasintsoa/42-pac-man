# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_context.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 16:10:07 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 21:50:29 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

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
    is_paused: bool = False
    game_running: bool = True
