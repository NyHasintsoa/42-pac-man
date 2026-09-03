# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  help_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:00:48 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 14:16:10 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.component import Button
from src.graphic.page.parent_page import ParentPage
from src.model.enums import PageState

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class HelpPage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.HELP_MENU
        self.btn_back = Button(
            360,
            760,
            280,
            70,
            "Back to Menu",
            font_size=24,
        )
        self.btn_quit = Button(
            360,
            840,
            280,
            70,
            "Quit Game",
            font_size=24,
        )

    def _event_listener(self) -> None:
        if self.btn_back.is_clicked:
            self.next_state = PageState.MAIN_MENU
        if self.btn_quit.is_clicked:
            pr.close_window()

    def render(self) -> None:
        panel = pr.Rectangle(100, 140, 800, 760)
        pr.draw_rectangle_rounded(panel, 0.3, 16, pr.DARKBLUE)
        pr.draw_rectangle_rounded_lines(panel, 0.3, 16, pr.GOLD)

        pr.draw_text("HELP & CONTROLS", 240, 180, 58, pr.YELLOW)
        pr.draw_text(
            "Keep your finger on the mouse and click the buttons to navigate.",
            140,
            240,
            22,
            pr.LIGHTGRAY,
        )
        pr.draw_text(
            "- Use the menu to start the game or choose a level.",
            140,
            320,
            22,
            pr.LIGHTGRAY,
        )
        pr.draw_text(
            "- Explore the maze and enjoy the arcade-style UI.",
            140,
            360,
            22,
            pr.LIGHTGRAY,
        )
        pr.draw_text(
            "- Return any time with the main menu button.",
            140,
            400,
            22,
            pr.LIGHTGRAY,
        )

        pr.draw_text("Tip:", 140, 470, 28, pr.GOLD)
        pr.draw_text(
            "A glowing golden path guides your way through the maze.",
            190,
            470,
            22,
            pr.LIGHTGRAY,
        )

        pr.draw_circle(840, 200, 18, pr.GOLD)
        pr.draw_circle(820, 260, 14, pr.SKYBLUE)
        pr.draw_circle(840, 320, 10, pr.LIGHTGRAY)

        self.btn_back.render()
        self.btn_quit.render()
        self._event_listener()
