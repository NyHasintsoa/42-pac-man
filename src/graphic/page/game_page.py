# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 08:07:34 by nramalan        #+#    #+#               #
#  Updated: 2026/07/10 16:32:15 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import TYPE_CHECKING

from src.model.game_context import GameContext
from src.model.enums import PageState
from src.graphic.component import MazeComponent, ScoreBoardComponent
from src.graphic.page.parent_page import ParentPage

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class GamePage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.GAME_PAGE
        self.score = 0
        self.lives = 5
        self.level = 1
        self.time_elapsed = 0
        self.game_running = True
        self.score_board = ScoreBoardComponent(
            self.window,
            padding_x=50,
        )

    def init(self, context: GameContext) -> None:
        super().init(context)
        self.maze_data = self.context.maze_level
        maze_cols, maze_rows = 20, 10

        ui_height = 160
        available_width = self.window.width * 0.95
        available_height = (self.window.height - ui_height) * 0.95
        cell_size_w = available_width // maze_cols
        cell_size_h = available_height // maze_rows
        self.scale = int(min(cell_size_w, cell_size_h))

        maze_pixel_width = maze_cols * self.scale
        maze_pixel_height = maze_rows * self.scale
        self.offset_x = (self.window.width - maze_pixel_width) // 2
        self.offset_y = (
            80 + ((self.window.height - 160) - maze_pixel_height) // 2
        )
        self.maze_view = MazeComponent(
            self.maze_data,
            self.window,
            margin_top=100,
            margin_bottom=30,
            color=pr.Color(4, 4, 214, 255),
            logo_color=pr.Color(33, 208, 220, 255),
        )

    def _event_listener(self) -> None:
        pass

    def update(self) -> None:
        self._event_listener()
        self.score_board.update(
            self.score, self.lives, self.level, self.time_elapsed
        )

    def render(self) -> None:
        pr.clear_background(pr.BLACK)
        self.update()
        self.score_board.render()
        self.maze_view.render()
