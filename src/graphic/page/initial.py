from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.page.parent import ParentPage
from src.graphic.component import MenuButton, PageFrame
from src.model.enums import PageState

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class InitialPage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.INIT_MENU
        self.page_frame = PageFrame(window.width, window.height)
        self.selected_index = 0
        btn_width = 400
        btn_height = 50
        btn_x = (window.width - btn_width) // 2

        self.buttons = [
            MenuButton(
                btn_x,
                520,
                btn_width,
                btn_height,
                "START ADVENTURE",
                35,
            ),
            MenuButton(
                btn_x,
                590,
                btn_width,
                btn_height,
                "HOW TO PLAY",
                35,
            ),
        ]

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
            self.next_state = PageState.MAIN_MENU
        elif self.buttons[1].is_clicked or (
            self.selected_index == 1 and enter_pressed
        ):
            self.next_state = PageState.HELP_MENU

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
