# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  init_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:21:14 by nramalan        #+#    #+#               #
#  Updated: 2026/05/10 21:13:45 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr

from src.enums import PageState
from src.graphic.component import Button
from src.graphic.page.parent_page import ParentPage


class InitPage(ParentPage):
    def __init__(self) -> None:
        super().__init__()
        self.state = PageState.INIT_MENU
        self.btn_first = Button(50, 50, 100, 40, "First")
        self.btn_second = Button(300, 250, 200, 50, "Second")

    def _event_listener(self) -> None:
        if (self.btn_first.is_clicked):
            print("Init page -> btn first")
        if (self.btn_second.is_clicked):
            self.next_state = PageState.MAIN_MENU
            print("Init page -> btn second")

    def render(self) -> None:
        pr.draw_text("Init Page", 220, 100, 40, pr.YELLOW)
        self.btn_first.render()
        self.btn_second.render()
        self._event_listener()
