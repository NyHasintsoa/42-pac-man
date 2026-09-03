# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_context.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 16:10:07 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 17:26:44 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pydantic import BaseModel
from typing import List


class LevelData(BaseModel):
    width: int
    height: int
    maze_data: List[List[int]]
    pacgums: List[List[int]]


class GameContext(BaseModel):
    maze_level: List[List[int]] = [[]]
