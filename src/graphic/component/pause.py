"""Render and operate the pause dialog."""

from typing import TYPE_CHECKING, Callable

import pyray as pr

from src.graphic.component import Button
from src.graphic.utils.text_helper import centered_x

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class PauseComponent:
    """Represent the modal pause menu."""

    def __init__(self, window: "MainWindow") -> None:
        """Initialize the PauseComponent instance.

        Args:
            window: The application window owning the component.

        Returns:
            The requested result.
        """
        self.window = window

        self.modal_w = 280
        self.modal_h = 320
        self.modal_x = (self.window.width - self.modal_w) // 2
        self.modal_y = (self.window.height - self.modal_h) // 2

        btn_w, btn_h = 200, 40
        btn_x = self.modal_x + (self.modal_w - btn_w) // 2
        start_y = self.modal_y + 120
        margin_top = 60

        self.resume_btn = Button(
            btn_x,
            start_y,
            btn_w,
            btn_h,
            "RESUME",
            bg_color=pr.Color(0, 162, 255, 255),
            text_color=pr.WHITE,
        )
        self.restart_btn = Button(
            btn_x, start_y + margin_top, btn_w, btn_h, "RESTART"
        )
        self.menu_btn = Button(
            btn_x, start_y + (margin_top * 2), btn_w, btn_h, "MAIN MENU"
        )

    def handle_input(
        self,
        on_resume: Callable[[], None],
        on_restart: Callable[[], None],
        on_menu: Callable[[], None],
    ) -> None:
        """Process mouse input and invoke the selected callback.

        Args:
            on_resume: Callback invoked when the player resumes.
            on_restart: Callback invoked when the player restarts.
            on_menu: Callback invoked when the player returns to the menu.

        Returns:
            The requested result.
        """
        if self.resume_btn.is_clicked:
            on_resume()
            self.resume_btn.is_clicked = False
        elif self.restart_btn.is_clicked:
            on_restart()
            self.restart_btn.is_clicked = False
        elif self.menu_btn.is_clicked:
            on_menu()
            self.menu_btn.is_clicked = False

    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
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
        pr.draw_text(
            title,
            centered_x(title, self.modal_x + (self.modal_w / 2), font_size),
            self.modal_y + 25,
            font_size,
            pr.Color(254, 222, 23, 255),
        )
        self.resume_btn.render()
        self.restart_btn.render()
        self.menu_btn.render()
