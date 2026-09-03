# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:29:56 by nramalan        #+#    #+#               #
#  Updated: 2026/05/25 17:13:30 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List

from src.graphic.page.parent_page import ParentPage
from src.graphic.page.init_page import InitPage
from src.graphic.page.menu_page import MenuPage
from src.graphic.page.help_page import HelpPage
from src.graphic.page.game_page import GamePage

__all__: List[str] = [
    "ParentPage",
    "InitPage",
    "MenuPage",
    "HelpPage",
    "GamePage",
]
