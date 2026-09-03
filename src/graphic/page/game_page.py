# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 08:07:34 by nramalan        #+#    #+#               #
#  Updated: 2026/05/15 19:59:01 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import TYPE_CHECKING
from mazegenerator import MazeGenerator

from src.enums import PageState
from src.graphic.component import (
    Button, MazeComponent
)
from src.graphic.page.parent_page import ParentPage

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class GamePage(ParentPage):
    def __init__(self, window: "MainWindow") -> None:
        super().__init__(window)
        self.state = PageState.GAME_PAGE
        self.score = 0
        self.lives = 3
        self.time_elapsed = 0
        self.game_running = True
        maze_cols, maze_rows = 20, 10
        self.maze_gen = MazeGenerator(
            (maze_cols, maze_rows), False, (0, 0), (14, 14)
        )
        self.maze_gen.generate()

        ui_height = 160
        available_width = self.window.width * 0.95
        available_height = (self.window.height - ui_height) * 0.95
        cell_size_w = available_width // maze_cols
        cell_size_h = available_height // maze_rows
        self.scale = int(min(cell_size_w, cell_size_h))

        # Center the maze
        maze_pixel_width = maze_cols * self.scale
        maze_pixel_height = maze_rows * self.scale
        self.offset_x = (self.window.width - maze_pixel_width) // 2
        self.offset_y = (
            80 + ((self.window.height - 160) - maze_pixel_height) // 2
        )
        self.maze_view = MazeComponent(
            self.maze_gen.maze,
            x=self.offset_x,
            y=self.offset_y,
            scale=self.scale,
            wall_thickness=5.0,
            color=pr.Color(4, 4, 214, 255),
            logo_color=pr.Color(33, 208, 220, 255)
        )
        self.btn_back = Button(
            self.window.width - 240, 15, 220, 50, "Main Menu",
            color=pr.DARKPURPLE, hover_color=pr.VIOLET,
            clicked_color=pr.GOLD, text_color=pr.WHITE,
            font_size=20, border_radius=0.35
        )

    def _event_listener(self) -> None:
        if self.btn_back.is_clicked:
            self.next_state = PageState.MAIN_MENU

    def render(self) -> None:
        pr.clear_background(pr.BLACK)

        # Top bar (Relative to window width)
        pr.draw_rectangle(0, 0, self.window.width, 80, pr.DARKBLUE)
        pr.draw_rectangle_lines(0, 0, self.window.width, 80, pr.GOLD)
        pr.draw_text("PAC-MAN", 20, 20, 48, pr.YELLOW)
        self.btn_back.render()

        self.maze_view.render()

        # Bottom info bar (Relative to window height/width)
        b_y = self.window.height - 80
        pr.draw_rectangle(0, b_y, self.window.width, 80, pr.DARKBLUE)
        pr.draw_rectangle_lines(0, b_y, self.window.width, 80, pr.GOLD)

        pr.draw_text(f"Score: {self.score}", 20, b_y + 25, 28, pr.YELLOW)
        pr.draw_text(f"Lives: {self.lives}", self.window.width // 2 - 50, b_y + 25, 28, pr.LIME)
        pr.draw_text(f"Time: {int(self.time_elapsed)}", self.window.width - 200, b_y + 25, 28, pr.LIGHTGRAY)

        self._event_listener()
