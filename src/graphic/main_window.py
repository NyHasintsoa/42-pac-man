# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_window.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/06 18:44:46 by nramalan        #+#    #+#               #
#  Updated: 2026/05/10 21:12:52 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Dict, Optional
import pyray as pr

from src.graphic.page import ParentPage, InitPage, HelpPage, MenuPage
from src.enums import PageState


class MainWindow:
    def __init__(self, width: int, height: int, title: str) -> None:
        self.width = width
        self.height = height
        self.title = title
        self.current_state: PageState
        self.current_page: Optional[ParentPage]
        self.windows: Dict[PageState, ParentPage]
        pr.set_trace_log_level(pr.TraceLogLevel.LOG_NONE)
        pr.init_window(self.width, self.height, self.title)
        pr.set_target_fps(30)

    def add_event(self) -> None:
        pr.set_exit_key(pr.KeyboardKey.KEY_NULL)

    def load_page(self) -> None:
        init_page = InitPage()
        menu_page = MenuPage()
        help_page = HelpPage()
        self.windows = {
            PageState.INIT_MENU: init_page,
            PageState.MAIN_MENU: menu_page,
            PageState.HELP_MENU: help_page,
        }
        self.current_state = PageState.INIT_MENU
        self.current_page = self.windows.get(self.current_state)

    def render(self) -> None:
        while not pr.window_should_close():
            pr.clear_background(pr.BLACK)
            pr.begin_drawing()
            if not self.current_page:
                break
            self.current_page.render()
            self.current_state = self.current_page.next_state
            pr.end_drawing()
        pr.close_window()
