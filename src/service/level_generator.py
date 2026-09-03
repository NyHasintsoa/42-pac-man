# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_generator.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 17:33:57 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 19:01:38 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List

from mazegenerator import MazeGenerator

from src.model import GameConfig
from src.model.game_context import LevelData


class LevelGenerator:
    def __init__(self, config: GameConfig) -> None:
        self.config = config

    def generate_levels(self) -> List[LevelData]:
        levels: List[LevelData] = []
        for _, lvl in enumerate(self.config.levels):
            print(f"level {lvl.model_dump_json()}")
            gen = MazeGenerator(
                size=(lvl.width, lvl.height), perfect=False,
                entry_cell=(0, 0),
                exit_cell=(lvl.width - 1, lvl.height - 1),
                seed=self.config.seed
            )
            gen.generate()
            levels.append(
                LevelData(
                    width=lvl.width,
                    height=lvl.height,
                    maze_data=gen.maze,
                )
            )
        return levels
