# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  init_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:21:14 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 18:07:44 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import TYPE_CHECKING

from src.model.enums import PageState
from src.graphic.component import Button
from src.graphic.page.parent_page import ParentPage
if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class InitPage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.INIT_MENU
        self.btn_start = Button(
            360, 590, 280, 70, "Start Adventure",
            color=pr.DARKBLUE, hover_color=pr.SKYBLUE,
            clicked_color=pr.GOLD, text_color=pr.WHITE,
            font_size=26, border_radius=0.35
        )
        self.btn_help = Button(
            360, 690, 280, 70, "How to Play",
            color=pr.DARKPURPLE, hover_color=pr.VIOLET,
            clicked_color=pr.GOLD, text_color=pr.WHITE,
            font_size=26, border_radius=0.35
        )

    def _event_listener(self) -> None:
        if self.btn_start.is_clicked:
            self.next_state = PageState.MAIN_MENU
        if self.btn_help.is_clicked:
            self.next_state = PageState.HELP_MENU

    def render(self) -> None:
        background_panel = pr.Rectangle(120, 120, 760, 680)
        pr.draw_rectangle_rounded(background_panel, 0.3, 16, pr.DARKBLUE)
        pr.draw_rectangle_rounded_lines(background_panel, 0.3, 16, pr.GOLD)

        pr.draw_text("PAC-MAN", 320, 180, 72, pr.YELLOW)
        pr.draw_text("A bold maze adventure with a 42 twist", 236, 260, 22, pr.LIGHTGRAY)
        pr.draw_text(
            "Choose your path, explore the maze, and enjoy arcade style fun.",
            190, 300, 20, pr.LIGHTGRAY
        )

        pr.draw_circle(190, 220, 26, pr.GOLD)
        pr.draw_circle(860, 220, 20, pr.SKYBLUE)
        pr.draw_circle(760, 330, 14, pr.LIGHTGRAY)
        pr.draw_circle(210, 330, 12, pr.LIGHTGRAY)

        self.btn_start.render()
        self.btn_help.render()
        self._event_listener()
