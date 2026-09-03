# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_context.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 16:10:07 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 18:54:09 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field
from typing import List, Optional

from src.model.game_config import GameConfig


class LevelData(BaseModel):
    width: int
    height: int
    maze_data: List[List[int]]
    # simple_pacgum: List[SimplePacgum] = Field(default_factory=list)
    # super_pacgum: List[SuperPacgum] = Field(default_factory=list)


class GameContext(BaseModel):
    config: Optional[GameConfig] = None
    levels: List[LevelData] = Field(default_factory=list)
    current_level_index: int = 0
    maze_level: List[List[int]] = Field(default_factory=lambda: [[]])
    score: int = 0
    lives: int = 3
    time_elapsed: int = 0
    is_paused: bool = False
    game_running: bool = True
