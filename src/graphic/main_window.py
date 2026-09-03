from typing import Dict, Optional

import pyray as pr

from src.graphic.page import (
    GamePage,
    HighScorePage,
    HowToPlayPage,
    LoadingPage,
    MenuPage,
    ParentPage,
    PlayerNamePage,
)
from src.model import GameConfig, GameContext
from src.model.enums import PageState


class MainWindow:
    def __init__(
        self, width: int, height: int, config: GameConfig, title: str
    ) -> None:
        self.width = width
        self.height = height
        self.title = title
        self.current_state: PageState
        self.current_page: Optional[ParentPage] = None
        self.windows: Dict[PageState, ParentPage] = {}
        self.context = GameContext(
            config=config,
            lives=config.lives,
        )

        pr.set_trace_log_level(pr.TraceLogLevel.LOG_NONE)
        pr.init_window(self.width, self.height, self.title)
        pr.set_target_fps(60)

    def add_event(self) -> None:
        pr.set_exit_key(pr.KeyboardKey.KEY_NULL)

    def load_page(self) -> None:
        self.windows = {
            PageState.LOADING_PAGE: LoadingPage(self),
            PageState.MAIN_MENU: MenuPage(self),
            PageState.HELP_MENU: HowToPlayPage(self),
            PageState.GAME_PAGE: GamePage(self),
            PageState.PLAYER_NAME_PAGE: PlayerNamePage(self),
            PageState.HIGH_SCORES_PAGE: HighScorePage(self),
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
