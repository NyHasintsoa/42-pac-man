# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  help_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:00:48 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 08:03:22 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import TYPE_CHECKING

from src.enums import PageState
from src.graphic.component import Button
from src.graphic.page.parent_page import ParentPage
if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class HelpPage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.HELP_MENU
        self.btn_first = Button(50, 50, 100, 40, "Back to Menu")
        self.btn_second = Button(300, 250, 200, 50, "Close")

    def _event_listener(self) -> None:
        if (self.btn_first.is_clicked):
            self.next_state = PageState.MAIN_MENU
        if (self.btn_second.is_clicked):
            print("Help page -> closing application")

    def render(self) -> None:
        pr.draw_text("Help Page", 220, 100, 40, pr.YELLOW)
        self.btn_first.render()
        self.btn_second.render()
        self._event_listener()
