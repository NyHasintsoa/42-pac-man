from threading import Thread
from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.page.parent import ParentPage
from src.model.enums import PageState
from src.service import LevelGenerator

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class LoadingPage(ParentPage):
    def __init__(self, window: "MainWindow") -> None:
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
        self.rotation_angle += 180.0 * pr.get_frame_time()
        if self.rotation_angle >= 360.0:
            self.rotation_angle -= 360.0

        if self.is_generation_done:
            self.next_state = PageState.MAIN_MENU

    def draw(self) -> None:
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

        txt_size = pr.measure_text(self.loading_message, 22)
        pr.draw_text(
            self.loading_message,
            center_x - (txt_size // 2),
            center_y + 65,
            22,
            pr.GOLD,
        )

        sub_txt = "Please wait while system matrices align"
        sub_size = pr.measure_text(sub_txt, 14)
        pr.draw_text(
            sub_txt,
            center_x - (sub_size // 2),
            center_y + 105,
            14,
            pr.DARKGRAY,
        )

    def render(self) -> None:
        self.update()
        self.draw()
