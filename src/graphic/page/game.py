# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 08:07:34 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 22:07:15 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING, List

import pyray as pr

from src.graphic.component import (
    GhostCharacter,
    MazeComponent,
    PacgumComponent,
    PacmanCharacter,
    ScoreBoardComponent,
)
from src.graphic.page.parent import ParentPage
from src.model import GameContext, LevelConfig, MazeData
from src.model.enums import PageState

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class GamePage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.GAME_PAGE
        self.score: int = 0
        self.lives: int = 5
        self.levels: List[LevelConfig]
        self.current_level: int = 1
        self.maze_data: MazeData
        self.time_elapsed: float = 0
        self.game_running: bool = True

    def init(self, context: GameContext) -> None:
        super().init(context)
        self.lives = self.context.lives
        self.levels = self.context.config.levels
        self.time_elapsed = self.levels[self.current_level - 1].level_max_time
        self.maze_data = self.context.maze_levels[self.current_level - 1]
        pacgums = self.context.pacgums[self.current_level - 1]

        self.score_board = ScoreBoardComponent(
            self.window,
            high_score=120,
            padding_x=50,
        )
        self.maze_view = MazeComponent(
            self.maze_data,
            self.window,
            margin_top=100,
            margin_bottom=30,
            padding_x=20,
            color=pr.Color(4, 4, 214, 255),
            logo_color=pr.Color(33, 208, 220, 255),
        )
        center_y = round(len(self.maze_data) / 2)
        center_x = round(len(self.maze_data[0]) / 2) - 1
        self.pacman = PacmanCharacter(
            self.maze_data,
            center_x,
            center_y,
            5.0,
            0.15,
            self.window,
            100,
            30,
            20,
        )
        self.ghost = GhostCharacter(
            self.maze_data,
            1,
            1,
            2.0,
            0.15,
            self.window,
            100,
            30,
            20,
        )
        self.pacgums = PacgumComponent(
            self.maze_data, self.window, pacgums, 100, 30, 20
        )

    def _event_listener(self) -> None:
        pass

    def update(self) -> None:
        self._event_listener()
        if self.time_elapsed > 0:
            self.time_elapsed -= pr.get_frame_time()
        self.score_board.update(
            self.score, self.lives, self.current_level, int(self.time_elapsed)
        )
        screen_px = int(self.pacman.pixel_pos.x)
        screen_py = int(self.pacman.pixel_pos.y)
        gained_score = self.pacgums.collect_pacgums(screen_px, screen_py)
        self.score += gained_score
        self.pacman.update()
        self.ghost.update()

    def render(self) -> None:
        pr.clear_background(pr.BLACK)
        self.update()
        self.score_board.render()
        self.maze_view.render()
        self.pacgums.render()
        self.ghost.render()
        self.pacman.render()
