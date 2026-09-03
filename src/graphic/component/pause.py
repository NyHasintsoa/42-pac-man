# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pause.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/13 22:50:36 by nramalan        #+#    #+#               #
#  Updated: 2026/07/14 14:56:05 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING, Callable

import pyray as pr

from src.graphic.component import Button

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class PauseComponent:
    def __init__(self, window: MainWindow) -> None:
        self.window = window

        self.modal_w = 280
        self.modal_h = 320
        self.modal_x = (self.window.width - self.modal_w) // 2
        self.modal_y = (self.window.height - self.modal_h) // 2

        btn_w, btn_h = 200, 40
        btn_x = self.modal_x + (self.modal_w - btn_w) // 2
        start_y = self.modal_y + 80

        self.resume_btn = Button(
            btn_x,
            start_y,
            btn_w,
            btn_h,
            "RESUME",
            bg_color=pr.Color(0, 162, 255, 255),
            text_color=pr.WHITE,
        )
        self.restart_btn = Button(btn_x, start_y + 50, btn_w, btn_h, "RESTART")
        self.menu_btn = Button(btn_x, start_y + 100, btn_w, btn_h, "MAIN MENU")
        self.quit_btn = Button(
            btn_x,
            start_y + 150,
            btn_w,
            btn_h,
            "QUIT",
            bg_color=pr.RED,
        )

    def handle_input(
        self, on_resume: Callable, on_restart: Callable, on_menu: Callable
    ) -> None:

        if pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT):
            mouse_pos = pr.get_mouse_position()

            if pr.check_collision_point_rec(mouse_pos, self.resume_btn.rect):
                on_resume()
            elif pr.check_collision_point_rec(
                mouse_pos, self.restart_btn.rect
            ):
                on_restart()
            elif pr.check_collision_point_rec(mouse_pos, self.menu_btn.rect):
                on_menu()
            elif pr.check_collision_point_rec(mouse_pos, self.quit_btn.rect):
                pr.close_window()

    def render(self) -> None:
        pr.draw_rectangle(
            0,
            0,
            self.window.width,
            self.window.height,
            pr.fade(pr.BLACK, 0.65),
        )

        pr.draw_rectangle(
            self.modal_x,
            self.modal_y,
            self.modal_w,
            self.modal_h,
            pr.Color(15, 33, 48, 255),
        )
        pr.draw_rectangle_lines_ex(
            pr.Rectangle(
                self.modal_x, self.modal_y, self.modal_w, self.modal_h
            ),
            4,
            pr.Color(33, 208, 220, 255),
        )

        title = "PAUSED"
        font_size = 36
        title_w = pr.measure_text(title, font_size)
        pr.draw_text(
            title,
            self.modal_x + (self.modal_w - title_w) // 2,
            self.modal_y + 25,
            font_size,
            pr.Color(254, 222, 23, 255),
        )
        self.resume_btn.render()
        self.restart_btn.render()
        self.menu_btn.render()
        self.quit_btn.render()
