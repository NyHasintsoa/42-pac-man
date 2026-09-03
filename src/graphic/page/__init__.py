# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:29:56 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 15:36:45 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.graphic.page.game import GamePage
from src.graphic.page.high_score import HighScorePage
from src.graphic.page.how_to_play import HowToPlayPage
from src.graphic.page.loading import LoadingPage
from src.graphic.page.menu import MenuPage
from src.graphic.page.parent import ParentPage
from src.graphic.page.player_name import PlayerNamePage

__all__ = [
    "ParentPage",
    "MenuPage",
    "HowToPlayPage",
    "GamePage",
    "PlayerNamePage",
    "LoadingPage",
    "HighScorePage",
]
