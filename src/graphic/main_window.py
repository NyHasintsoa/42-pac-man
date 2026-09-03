# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_window.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/06 18:44:46 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 17:03:25 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Dict, Optional
import pyray as pr

from src.data import GameContext
from src.graphic.page import HelpPage, InitPage, MenuPage, ParentPage
from src.graphic.page import GamePage
from src.graphic.page.loading_page import LoadingPage
from src.enums import PageState


class MainWindow:
    def __init__(self, width: int, height: int, title: str) -> None:
        self.width = width
        self.height = height
        self.title = title
        self.current_state: PageState
        self.current_page: Optional[ParentPage] = None
        self.windows: Dict[PageState, ParentPage] = {}
        self.cached_maze: Optional[list] = None
        self.context = GameContext()

        pr.set_trace_log_level(pr.TraceLogLevel.LOG_NONE)
        pr.init_window(self.width, self.height, self.title)
        pr.set_target_fps(60)

    def add_event(self) -> None:
        pr.set_exit_key(pr.KeyboardKey.KEY_NULL)

    def load_page(self) -> None:
        loading_page = LoadingPage(self)
        init_page = InitPage(self)
        menu_page = MenuPage(self)
        help_page = HelpPage(self)
        game_page = GamePage(self)

        self.windows = {
            PageState.LOADING_PAGE: loading_page,
            PageState.INIT_MENU: init_page,
            PageState.MAIN_MENU: menu_page,
            PageState.HELP_MENU: help_page,
            PageState.GAME_PAGE: game_page
        }

        self.current_state = PageState.LOADING_PAGE
        self.current_page = self.windows.get(self.current_state)
        if self.current_page:
            self.current_page.init(self.context)

    def render(self) -> None:
        while not pr.window_should_close():
            pr.clear_background(pr.BLACK)
            pr.begin_drawing()

            if not self.current_page:
                pr.end_drawing()
                break

            self.current_page.render()

            if self.current_page.next_state != self.current_state:
                self.context = self.current_page.context
                self.current_state = self.current_page.next_state
                self.current_page = self.windows.get(self.current_state)
                if self.current_page:
                    self.current_page.next_state = self.current_state
                    self.current_page.init(self.context)
            pr.end_drawing()
        pr.close_window()
