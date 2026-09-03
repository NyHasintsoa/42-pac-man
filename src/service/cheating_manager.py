# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheating_manager.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/14 14:49:10 by nramalan        #+#    #+#               #
#  Updated: 2026/07/14 14:51:00 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.graphic.page.game import GamePage


class CheatingManager:
    """
    Manages all cheating features and behavior toggles without bloating game.py
    """

    def __init__(self) -> None:
        self.invincible: bool = False
        self.ghost_freeze: bool = False
        self.speed_boost: bool = False

    def add_extra_life(self, game_page: "GamePage") -> None:
        """Increments player life count directly."""
        game_page.lives += 1

    def skip_level(self, game_page: "GamePage") -> None:
        """Triggers level skip sequence on target GamePage."""
        game_page.is_cheating = False
        if game_page.current_level < len(game_page.levels):
            game_page.current_level += 1
            game_page.init(game_page.context)
        else:
            game_page.return_to_menu()
