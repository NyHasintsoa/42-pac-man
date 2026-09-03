# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  page_state.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 16:44:52 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 15:38:15 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import StrEnum


class PageState(StrEnum):
    LOADING_PAGE = "LOADING_PAGE"
    MAIN_MENU = "MAIN_MENU"
    HELP_MENU = "HELP_MENU"
    GAME_PAGE = "GAME_PAGE"
    PLAYER_NAME_PAGE = "PLAYER_NAME_PAGE"
    HIGH_SCORES_PAGE = "HIGH_SCORES_PAGE"
