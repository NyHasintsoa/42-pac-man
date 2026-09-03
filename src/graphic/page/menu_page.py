# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  menu_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:00:58 by nramalan        #+#    #+#               #
#  Updated: 2026/05/10 21:49:17 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr

from src.enums import PageState
from src.graphic.component import Button
from src.graphic.page.parent_page import ParentPage


class MenuPage(ParentPage):
    def __init__(self) -> None:
        super().__init__()
        self.state = PageState.MAIN_MENU
        self.next_state = PageState.MAIN_MENU
        self.btn_first = Button(50, 50, 100, 40, "Go to Help")
        self.btn_second = Button(300, 250, 200, 50, "Back to Init")

    def _event_listener(self) -> None:
        if (self.btn_first.is_clicked):
            self.next_state = PageState.HELP_MENU
            print("Menu page -> transitioning to Help Menu")
        if (self.btn_second.is_clicked):
            self.next_state = PageState.INIT_MENU
            print("Menu page -> transitioning to Init Menu")

    def render(self) -> None:
        pr.draw_text("Menu Page", 220, 100, 40, pr.YELLOW)
        self.btn_first.render()
        self.btn_second.render()
        self._event_listener()
