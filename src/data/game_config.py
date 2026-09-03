# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_config.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 15:24:39 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 17:32:39 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel, Field
from typing import List


class LevelConfig(BaseModel):
    width: int = 20
    height: int = 10


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
