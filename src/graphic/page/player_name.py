# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  player_name.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/11 18:05:00 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 15:15:43 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.component import Button, Input
from src.graphic.page.parent import ParentPage
from src.model.enums import PageState
from src.model.game_context import GameContext

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class PlayerNamePage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.PLAYER_NAME_PAGE

        box_width = 300
        box_height = 50
        box_x = (self.window.width // 2) - (box_width // 2)
        self.box_y = (self.window.height // 2) - 40

        btn_width = 160
        btn_height = 45
        btn_x = (self.window.width // 2) - (btn_width // 2)
        btn_y = self.box_y + box_height + 30

        self.name_input = Input(
            pos_x=box_x,
            pos_y=self.box_y,
            width=box_width,
            height=box_height,
            max_chars=12,
        )

        self.submit_btn = Button(
            pos_x=btn_x,
            pos_y=btn_y,
            width=btn_width,
            height=btn_height,
            text="SUBMIT",
            font_size=20,
        )

    def init(self, context: GameContext) -> None:
        super().init(context)
        self.name_input.clear()

    def update(self) -> None:
        self.name_input.update()

        enter_pressed = pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER)

        if self.submit_btn.is_clicked or enter_pressed:
            self._handle_submit()

    def _handle_submit(self) -> None:
        cleaned_name = self.name_input.value.strip()

        if cleaned_name:
            print(f"[SUBMITTED PLAYER NAME]: {cleaned_name}")
        else:
            print("[SUBMITTED PLAYER NAME]: Anonymous Player")

    def render(self) -> None:
        self.update()

        title_text = "ENTER PLAYER NAME"
        title_size = 28
        title_width = pr.measure_text(title_text, title_size)
        pr.draw_text(
            title_text,
            (self.window.width // 2) - (title_width // 2),
            self.box_y - 60,
            title_size,
            pr.YELLOW,
        )

        self.name_input.render()
        self.submit_btn.render()
