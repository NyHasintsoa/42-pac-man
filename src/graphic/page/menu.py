"""Display the main menu and handle its navigation."""

from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.component import MenuButton, PageFrame
from src.graphic.page.parent import ParentPage
from src.graphic.utils.text_helper import centered_x
from src.model.enums import PageState
from src.graphic.utils import ft_check_collision_point_rec

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class MenuPage(ParentPage):
    """Display the main menu and route the selected action."""

    def __init__(self, window: "MainWindow") -> None:
        """Initialize the MenuPage instance.

        Args:
            window: The application window owning the component.

        Returns:
            The requested result.
        """
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
        """Release graphical resources owned by the component.

        Returns:
            The requested result.
        """
        if self._is_unloaded:
            return
        for button in self.buttons:
            button.unload()
        super().unload()

    def _event_listener(self) -> None:
        """Process keyboard and mouse events for the page.

        Returns:
            The requested result.
        """
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
            self.window.request_close()

    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        self._event_listener()
        self.page_frame.render()
        title = "PAC-MAN"
        title_font_size = 72
        pr.draw_text(
            title,
            centered_x(title, self.window.width / 2, title_font_size),
            int(self.window.height * 0.20),
            title_font_size,
            pr.YELLOW,
        )

        mouse_pos = pr.get_mouse_position()
        for i, button in enumerate(self.buttons):
            if ft_check_collision_point_rec(mouse_pos, button.rect):
                self.selected_index = i

        for i, button in enumerate(self.buttons):
            button.render(is_focused=(i == self.selected_index))
