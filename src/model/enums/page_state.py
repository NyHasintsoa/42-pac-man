# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  page_state.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 16:44:52 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 15:02:16 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import IntEnum


class PageState(IntEnum):
    LOADING_PAGE = 0
    INIT_MENU = 1
    MAIN_MENU = 2
    HELP_MENU = 3
    GAME_PAGE = 4
    PLAYER_NAME_PAGE = 5
    HIGH_SCORES_PAGE = 6
