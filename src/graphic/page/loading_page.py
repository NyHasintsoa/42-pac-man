# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  loading_page.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/25 17:26:20 by nramalan        #+#    #+#               #
#  Updated: 2026/05/25 17:34:05 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
import threading
from typing import TYPE_CHECKING
from mazegenerator import MazeGenerator
from src.enums import PageState
from src.graphic.page.parent_page import ParentPage

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class LoadingPage(ParentPage):
    def __init__(self, window: "MainWindow") -> None:
        super().__init__(window)
        self.state = PageState.LOADING_PAGE
        self.next_state = PageState.LOADING_PAGE
        
        # Retro loading configs
        self.rotation_angle = 0.0
        self.is_generation_done = False
        self.loading_message = "GENERATING MAZE CONFIGURATIONS..."

        # Offload structural math to a background thread
        self.worker_thread = threading.Thread(target=self._perform_heavy_generation)
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def _perform_heavy_generation(self) -> None:
        """Executes concurrently behind the main graphics thread context."""
        maze_cols, maze_rows = 20, 20
        # Use exact layout parameter calls to mirror game requirements
        maze_gen = MazeGenerator(
            (maze_cols, maze_rows), False,
            (0, 0), (maze_cols - 1, maze_rows - 1)
        )
        maze_gen.generate()
        
        # Save array output directly to global memory storage
        self.window.cached_maze = maze_gen.maze
        self.is_generation_done = True

    def update(self) -> None:
        # Spin arc dynamically at 180 degrees per second
        self.rotation_angle += 180.0 * pr.get_frame_time()
        if self.rotation_angle >= 360.0:
            self.rotation_angle -= 360.0

        # When worker thread wraps matrix processing, forward application to Init Menu
        if self.is_generation_done:
            self.next_state = PageState.INIT_MENU

    def render(self) -> None:
        self.update()
        
        center_x = self.window.width // 2
        center_y = self.window.height // 2

        # Draw Arcade Loader Ring
        pr.draw_circle_sector_lines(
            pr.Vector2(center_x, center_y - 20),
            45.0,
            self.rotation_angle,
            self.rotation_angle + 270.0,
            36,
            pr.YELLOW
        )

        # Status HUD texts
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