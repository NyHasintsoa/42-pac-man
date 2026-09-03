# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  loading_page.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/25 17:26:20 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 17:15:14 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from threading import Thread
from typing import TYPE_CHECKING
from mazegenerator import MazeGenerator
from src.enums import PageState
from src.graphic.page.parent_page import ParentPage

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class LoadingPage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.LOADING_PAGE
        self.next_state = PageState.LOADING_PAGE
        self.rotation_angle = 0.0
        self.is_generation_done = False
        self.loading_message = "GENERATING MAZE CONFIGURATIONS..."
        self.worker_thread = Thread(target=self._perform_heavy_generation)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def _perform_heavy_generation(self) -> None:
        maze_cols, maze_rows = 20, 10
        maze_gen = MazeGenerator(
            (maze_cols, maze_rows), False,
            (0, 0), (maze_cols - 1, maze_rows - 1)
        )
        maze_gen.generate()
        self.context.maze_level = maze_gen.maze
        self.is_generation_done = True

    def update(self) -> None:
        self.rotation_angle += 180.0 * pr.get_frame_time()
        if self.rotation_angle >= 360.0:
            self.rotation_angle -= 360.0

        if self.is_generation_done:
            self.next_state = PageState.INIT_MENU

    def draw(self) -> None:
        center_x = self.window.width // 2
        center_y = self.window.height // 2

        pr.draw_circle_sector_lines(
            pr.Vector2(center_x, center_y - 20),
            45.0,
            self.rotation_angle,
            self.rotation_angle + 270.0,
            36,
            pr.YELLOW
        )

        txt_size = pr.measure_text(self.loading_message, 22)
        pr.draw_text(
            self.loading_message,
            center_x - (txt_size // 2),
            center_y + 65,
            22,
            pr.GOLD
        )

        sub_txt = "Please wait while system matrices align"
        sub_size = pr.measure_text(sub_txt, 14)
        pr.draw_text(
            sub_txt,
            center_x - (sub_size // 2),
            center_y + 105,
            14,
            pr.DARKGRAY
        )

    def render(self) -> None:
        self.update()
        self.draw()
