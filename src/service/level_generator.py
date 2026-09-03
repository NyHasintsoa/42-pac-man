# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_generator.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 17:33:57 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 17:56:17 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.model import GameConfig


class LevelGenerator:
    def __init__(self, config: GameConfig) -> None:
        self.config = config
