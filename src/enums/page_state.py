# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  page_state.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 16:44:52 by nramalan        #+#    #+#               #
#  Updated: 2026/05/10 18:37:24 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import IntEnum


class PageState(IntEnum):
    INIT_MENU = 0
    MAIN_MENU = 1
    HELP_MENU = 2
