# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  menu_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:00:58 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 14:16:17 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.component import Button
from src.graphic.page.parent_page import ParentPage
from src.model.enums import PageState

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class MenuPage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.MAIN_MENU
        self.btn_play = Button(
            360,
            340,
            280,
            70,
            "Play Game",
            font_size=24,
        )
        self.btn_level = Button(
            360,
            440,
            280,
            70,
            "Level Select",
            font_size=24,
        )
        self.btn_help = Button(
            360,
            540,
            280,
            70,
            "Help & Controls",
            font_size=24,
        )
        self.btn_exit = Button(
            360,
            640,
            280,
            70,
            "Quit Game",
            font_size=24,
        )

    def _event_listener(self) -> None:
        if self.btn_play.is_clicked:
            self.next_state = PageState.GAME_PAGE
        if self.btn_help.is_clicked:
            self.next_state = PageState.HELP_MENU
        if self.btn_exit.is_clicked:
            pr.close_window()

    def render(self) -> None:
        panel = pr.Rectangle(120, 120, 760, 720)
        pr.draw_rectangle_rounded(panel, 0.3, 16, pr.DARKBLUE)
        pr.draw_rectangle_rounded_lines(panel, 0.3, 16, pr.GOLD)

        pr.draw_text("MAIN MENU", 320, 180, 60, pr.YELLOW)
        pr.draw_text(
            "Select your next challenge and jump back into the maze.",
            210,
            250,
            22,
            pr.LIGHTGRAY,
        )

        pr.draw_circle(180, 220, 24, pr.GOLD)
        pr.draw_circle(820, 220, 20, pr.SKYBLUE)
        pr.draw_text("Ready?", 720, 300, 32, pr.SKYBLUE)

        self.btn_play.render()
        self.btn_level.render()
        self.btn_help.render()
        self.btn_exit.render()
        self._event_listener()
