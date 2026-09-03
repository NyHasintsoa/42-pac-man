from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.component import MenuButton, PageFrame
from src.graphic.page.parent import ParentPage
from src.model.enums import PageState

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class MenuPage(ParentPage):
    def __init__(self, window: "MainWindow") -> None:
        super().__init__(window)
        self.state = PageState.MAIN_MENU
        self.page_frame = PageFrame(window.width, window.height)
        self.selected_index = 0
        btn_width = 400
        btn_height = 50
        btn_x = (window.width - btn_width) // 2

        self.buttons = [
            MenuButton(
                btn_x,
                500,
                btn_width,
                btn_height,
                "Play Game",
                font_size=24,
            ),
            MenuButton(
                btn_x,
                570,
                btn_width,
                btn_height,
                "How To Play",
                font_size=24,
            ),
            MenuButton(
                btn_x,
                640,
                btn_width,
                btn_height,
                "High Scores",
                font_size=24,
            ),
            MenuButton(
                btn_x,
                710,
                btn_width,
                btn_height,
                "Quit Game",
                font_size=24,
            ),
        ]

    def unload(self) -> None:
        if self._is_unloaded:
            return
        for button in self.buttons:
            button.unload()
        super().unload()

    def _event_listener(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_UP) or pr.is_key_pressed(
            pr.KeyboardKey.KEY_W
        ):
            self.selected_index = (self.selected_index - 1) % len(self.buttons)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN) or pr.is_key_pressed(
            pr.KeyboardKey.KEY_S
        ):
            self.selected_index = (self.selected_index + 1) % len(self.buttons)

        enter_pressed = pr.is_key_pressed(
            pr.KeyboardKey.KEY_ENTER
        ) or pr.is_key_pressed(pr.KeyboardKey.KEY_KP_ENTER)

        if self.buttons[0].is_clicked or (
            self.selected_index == 0 and enter_pressed
        ):
            self.next_state = PageState.GAME_PAGE
        elif self.buttons[1].is_clicked or (
            self.selected_index == 1 and enter_pressed
        ):
            self.next_state = PageState.HELP_MENU
        if self.buttons[2].is_clicked or (
            self.selected_index == 2 and enter_pressed
        ):
            self.next_state = PageState.HIGH_SCORES_PAGE
        elif self.buttons[3].is_clicked or (
            self.selected_index == 3 and enter_pressed
        ):
            self.window.close()

    def render(self) -> None:
        self._event_listener()
        self.page_frame.render()
        pr.draw_text("PAC-MAN", 320, 180, 72, pr.YELLOW)

        mouse_pos = pr.get_mouse_position()
        for i, button in enumerate(self.buttons):
            if pr.check_collision_point_rec(mouse_pos, button.rect):
                self.selected_index = i

        for i, button in enumerate(self.buttons):
            button.render(is_focused=(i == self.selected_index))
