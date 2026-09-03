from typing import TYPE_CHECKING, Callable, Dict

import pyray as pr

from src.graphic.component import Button

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow
    from src.service import CheatingManager


class CheatComponent:
    def __init__(self, window: MainWindow, manager: CheatingManager) -> None:
        self.window = window
        self.manager = manager

        self.modal_w = 340
        self.modal_h = 420
        self.modal_x = (self.window.width - self.modal_w) // 2
        self.modal_y = (self.window.height - self.modal_h) // 2

        btn_w, btn_h = 120, 35
        btn_x_left = self.modal_x + 30
        btn_x_right = self.modal_x + self.modal_w - btn_w - 30

        self.lives_btn = Button(
            btn_x_left,
            self.modal_y + 300,
            btn_w,
            btn_h,
            "+1 LIFE",
            bg_color=pr.Color(0, 162, 255, 255),
        )
        self.skip_btn = Button(
            btn_x_right,
            self.modal_y + 300,
            btn_w,
            btn_h,
            "SKIP LEVEL",
            bg_color=pr.Color(0, 180, 100, 255),
        )

        self.close_btn = Button(
            self.modal_x + (self.modal_w - 200) // 2,
            self.modal_y + 360,
            200,
            35,
            "RESUME GAME",
            bg_color=pr.GRAY,
        )

        checkbox_start_y = self.modal_y + 90
        self.checkboxes: Dict[str, pr.Rectangle] = {
            "invincible": pr.Rectangle(
                self.modal_x + 40, checkbox_start_y, 24, 24
            ),
            "freeze": pr.Rectangle(
                self.modal_x + 40, checkbox_start_y + 50, 24, 24
            ),
            "speed": pr.Rectangle(
                self.modal_x + 40, checkbox_start_y + 100, 24, 24
            ),
        }

    def handle_input(
        self,
        on_add_life: Callable[[], None],
        on_skip_level: Callable[[], None],
        on_close: Callable[[], None],
    ) -> None:
        if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
            mouse_pos = pr.get_mouse_position()

            if pr.check_collision_point_rec(mouse_pos, self.lives_btn.rect):
                on_add_life()
            elif pr.check_collision_point_rec(mouse_pos, self.skip_btn.rect):
                on_skip_level()
            elif pr.check_collision_point_rec(mouse_pos, self.close_btn.rect):
                on_close()

            for key, rect in self.checkboxes.items():
                if pr.check_collision_point_rec(mouse_pos, rect):
                    if key == "invincible":
                        self.manager.invincible = not self.manager.invincible
                    elif key == "freeze":
                        self.manager.ghost_freeze = (
                            not self.manager.ghost_freeze
                        )
                    elif key == "speed":
                        self.manager.speed_boost = not self.manager.speed_boost

    def _draw_checkbox(
        self, rect: pr.Rectangle, checked: bool, label: str
    ) -> None:
        pr.draw_rectangle_lines_ex(rect, 2, pr.Color(33, 208, 220, 255))

        if checked:
            inner_padding = 4
            pr.draw_rectangle(
                int(rect.x + inner_padding),
                int(rect.y + inner_padding),
                int(rect.width - (inner_padding * 2)),
                int(rect.height - (inner_padding * 2)),
                pr.Color(254, 222, 23, 255),
            )

        pr.draw_text(
            label,
            int(rect.x + rect.width + 15),
            int(rect.y + (rect.height - 18) // 2),
            18,
            pr.WHITE,
        )

    def render(self) -> None:
        pr.draw_rectangle(
            0, 0, self.window.width, self.window.height, pr.fade(pr.BLACK, 0.7)
        )

        pr.draw_rectangle(
            self.modal_x,
            self.modal_y,
            self.modal_w,
            self.modal_h,
            pr.Color(18, 18, 28, 255),
        )
        pr.draw_rectangle_lines_ex(
            pr.Rectangle(
                self.modal_x, self.modal_y, self.modal_w, self.modal_h
            ),
            4,
            pr.Color(255, 0, 128, 255),
        )

        title = "CHEAT PANEL"
        font_size = 28
        title_w = pr.measure_text(title, font_size)
        pr.draw_text(
            title,
            self.modal_x + (self.modal_w - title_w) // 2,
            self.modal_y + 25,
            font_size,
            pr.Color(255, 0, 128, 255),
        )

        self._draw_checkbox(
            self.checkboxes["invincible"],
            self.manager.invincible,
            "Invincibility",
        )
        self._draw_checkbox(
            self.checkboxes["freeze"],
            self.manager.ghost_freeze,
            "Freeze Ghosts",
        )
        self._draw_checkbox(
            self.checkboxes["speed"],
            self.manager.speed_boost,
            "Double Speed x2",
        )

        pr.draw_line(
            self.modal_x + 20,
            self.modal_y + 265,
            self.modal_x + self.modal_w - 20,
            self.modal_y + 265,
            pr.GRAY,
        )

        self.lives_btn.render()
        self.skip_btn.render()
        self.close_btn.render()
