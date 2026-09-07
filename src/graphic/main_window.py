"""Manage the Raylib window and page transitions."""

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
    """Manage the game window, pages, and shared context."""

    def __init__(
        self, width: int, height: int, config: GameConfig, title: str
    ) -> None:
        """Initialize the MainWindow instance.

        Args:
            width: The width in tiles or pixels.
            height: The height in tiles or pixels.
            config: The validated game configuration.
            title: The title value.

        Returns:
            The requested result.
        """
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
        """Configure window input so the game handles exit events itself.

        Returns:
            The requested result.
        """
        pr.set_exit_key(pr.KeyboardKey.KEY_NULL)

    def close(self) -> None:
        """Release page resources and close the Raylib window.

        Returns:
            The requested result.
        """
        for page in self.windows.values():
            if not getattr(page, "_is_unloaded", False):
                page.unload()
        pr.close_window()

    def load_page(self) -> None:
        """Create all pages and initialize the loading page.

        Returns:
            The requested result.
        """
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
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
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
        self.close()
