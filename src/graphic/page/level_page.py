# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_page.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 07:54:19 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 08:34:24 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import TYPE_CHECKING

from src.enums import PageState
from src.graphic.component import Button
from src.graphic.page.parent_page import ParentPage
if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class LevelPage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.LEVEL_MENU
        self.btn_level_one = Button(
            220, 420, 180, 70, "Level 1",
            color=pr.DARKBLUE, hover_color=pr.SKYBLUE,
            clicked_color=pr.GOLD, font_size=24, border_radius=0.35
        )
        self.btn_level_two = Button(
            410, 420, 180, 70, "Level 2",
            color=pr.DARKPURPLE, hover_color=pr.VIOLET,
            clicked_color=pr.GOLD, font_size=24, border_radius=0.35
        )
        self.btn_level_three = Button(
            600, 420, 180, 70, "Level 3",
            color=pr.DARKGREEN, hover_color=pr.LIME,
            clicked_color=pr.GOLD, font_size=24, border_radius=0.35
        )
        self.btn_back = Button(
            360, 660, 280, 70, "Return to Menu",
            color=pr.DARKGRAY, hover_color=pr.SKYBLUE,
            clicked_color=pr.GOLD, font_size=24, border_radius=0.35
        )

    def _event_listener(self) -> None:
        if self.btn_level_one.is_clicked:
            self.next_state = PageState.GAME_PAGE
        if self.btn_level_two.is_clicked:
            self.next_state = PageState.GAME_PAGE
        if self.btn_level_three.is_clicked:
            self.next_state = PageState.GAME_PAGE
        if self.btn_back.is_clicked:
            self.next_state = PageState.MAIN_MENU

    def render(self) -> None:
        panel = pr.Rectangle(100, 140, 800, 760)
        pr.draw_rectangle_rounded(panel, 0.3, 16, pr.DARKBLUE)
        pr.draw_rectangle_rounded_lines(panel, 0.3, 16, pr.GOLD)

        pr.draw_text("LEVEL SELECT", 280, 180, 58, pr.YELLOW)
        pr.draw_text(
            "Choose the maze difficulty and begin your adventure.",
            180, 260, 22, pr.LIGHTGRAY
        )

        pr.draw_circle(160, 220, 24, pr.GOLD)
        pr.draw_circle(820, 240, 20, pr.SKYBLUE)

        self.btn_level_one.render()
        self.btn_level_two.render()
        self.btn_level_three.render()
        self.btn_back.render()
        self._event_listener()
