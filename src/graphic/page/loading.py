"""Generate levels while displaying the loading page."""

from threading import Thread
from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.page.parent import ParentPage
from src.graphic.utils.text_helper import centered_x
from src.model.enums import PageState
from src.service import LevelGenerator

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class LoadingPage(ParentPage):
    """Generate game levels asynchronously before showing the menu."""

    def __init__(self, window: "MainWindow") -> None:
        """Initialize the LoadingPage instance.

        Args:
            window: The application window owning the component.

        Returns:
            The requested result.
        """
        super().__init__(window)
        self.state = PageState.LOADING_PAGE
        self.next_state = PageState.LOADING_PAGE
        self.rotation_angle = 0.0
        self.is_generation_done = False
        self.loading_message = "GENERATING LEVELS..."
        self.progress_text = "Level generation progressing"

        if self.context and self.context.config:
            self.worker_thread = Thread(target=self._perform_heavy_generation)
            self.worker_thread.daemon = True
            self.worker_thread.start()
        else:
            self.is_generation_done = True

    def _perform_heavy_generation(self) -> None:
        """Generate configured levels on the loading worker thread.

        Returns:
            The requested result.
        """
        try:
            config = self.context.config
            if not config:
                self.is_generation_done = True
                return

            level_gen = LevelGenerator(config)
            maze, pacgums = level_gen.generate_levels()
            self.context.maze_levels = maze
            self.context.pacgums = pacgums
            self.context.current_level = 0
            self.context.lives = config.lives
        finally:
            self.is_generation_done = True

    def update(self) -> None:
        """Update component state from current input or timers.

        Returns:
            The requested result.
        """
        self.rotation_angle += 180.0 * pr.get_frame_time()
        if self.rotation_angle >= 360.0:
            self.rotation_angle -= 360.0

        if self.is_generation_done:
            self.next_state = PageState.MAIN_MENU

    def draw(self) -> None:
        """Draw the loading indicator and status text.

        Returns:
            The requested result.
        """
        center_x = self.window.width // 2
        center_y = self.window.height // 2

        pr.draw_circle_sector_lines(
            pr.Vector2(center_x, center_y - 20),
            45.0,
            self.rotation_angle,
            self.rotation_angle + 270.0,
            36,
            pr.YELLOW,
        )

        pr.draw_text(
            self.loading_message,
            centered_x(self.loading_message, center_x, 22),
            center_y + 65,
            22,
            pr.GOLD,
        )

        sub_txt = "Please wait while system matrices align"
        pr.draw_text(
            sub_txt,
            centered_x(sub_txt, center_x, 14),
            center_y + 105,
            14,
            pr.DARKGRAY,
        )

    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        self.update()
        self.draw()
