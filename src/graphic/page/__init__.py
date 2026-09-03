# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:29:56 by nramalan        #+#    #+#               #
#  Updated: 2026/05/10 18:36:34 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List

from src.graphic.page.parent_page import ParentPage
from src.graphic.page.init_page import InitPage
from src.graphic.page.menu_page import MenuPage
from src.graphic.page.help_page import HelpPage

__all__: List[str] = [
    "ParentPage",
    "InitPage",
    "MenuPage",
    "HelpPage",
]
