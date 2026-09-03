# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_page.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 07:54:19 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 08:15:04 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import TYPE_CHECKING

from src.enums import PageState
from src.graphic.component import Button
from src.graphic.page.parent_page import ParentPage
if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class LevelPage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.LEVEL_MENU
        self.btn_first = Button(50, 50, 100, 40, "Start Game")
        self.btn_second = Button(300, 250, 200, 50, "Go to Main Menu")

    def _event_listener(self) -> None:
        if (self.btn_first.is_clicked):
            self.next_state = PageState.GAME_PAGE
        if (self.btn_second.is_clicked):
            self.next_state = PageState.MAIN_MENU

    def render(self) -> None:
        pr.draw_text("Level Page", 220, 100, 40, pr.YELLOW)
        self.btn_first.render()
        self.btn_second.render()
        self._event_listener()
