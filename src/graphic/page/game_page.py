# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 08:07:34 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 08:33:04 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import TYPE_CHECKING

from mazegenerator import MazeGenerator

from src.enums import PageState
from src.graphic.component import Button, MazeComponent
from src.graphic.page.parent_page import ParentPage

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class GamePage(ParentPage):
    def __init__(self, window: "MainWindow") -> None:
        super().__init__(window)
        self.state = PageState.GAME_PAGE

        self.maze_gen = MazeGenerator(size=(18, 11), perfect=True)
        self.maze_view = MazeComponent(
            self.maze_gen.maze,
            x=40,
            y=180,
            cell_size=40,
            wall_width=4.0,
            color=pr.BLUE,
            logo_color=pr.GOLD
        )

        self.btn_back = Button(
            740, 40, 220, 60, "Main Menu",
            color=pr.DARKPURPLE, hover_color=pr.VIOLET,
            clicked_color=pr.GOLD, text_color=pr.WHITE,
            font_size=24, border_radius=0.35
        )

    def _event_listener(self) -> None:
        if self.btn_back.is_clicked:
            self.next_state = PageState.MAIN_MENU

    def render(self) -> None:
        header_bar = pr.Rectangle(20, 20, 960, 120)
        pr.draw_rectangle_rounded(header_bar, 0.3, 16, pr.DARKBLUE)
        pr.draw_rectangle_rounded_lines(header_bar, 0.3, 16, pr.GOLD)

        pr.draw_text("PAC-MAN ADVENTURE", 40, 40, 40, pr.GOLD)
        pr.draw_text("Score: 0000", 40, 90, 22, pr.LIGHTGRAY)
        pr.draw_text("Lives: 3", 320, 90, 22, pr.LIGHTGRAY)
        pr.draw_text("Maze Explorer", 520, 90, 22, pr.SKYBLUE)

        pr.draw_circle(880, 70, 22, pr.GOLD)
        pr.draw_circle(910, 90, 14, pr.SKYBLUE)

        border = pr.Rectangle(30, 140, 940, 760)
        pr.draw_rectangle_rounded(border, 0.2, 16, pr.DARKGRAY)
        pr.draw_rectangle_rounded_lines(border, 0.2, 16, pr.GRAY)

        self.maze_view.render()
        self.btn_back.render()
        self._event_listener()