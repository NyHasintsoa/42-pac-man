"""Render a keyboard- and mouse-selectable menu item."""

import pyray as pr

from src.graphic.utils.text_helper import centered_text_position
from src.graphic.utils import ft_check_collision_point_rec


class MenuButton:
    """Represent a selectable button in a menu."""

    def __init__(
        self,
        pos_x: int,
        pos_y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = 24,
    ) -> None:
        """Initialize the MenuButton instance.

        Args:
            pos_x: The horizontal position or grid coordinate.
            pos_y: The vertical position or grid coordinate.
            width: The width in tiles or pixels.
            height: The height in tiles or pixels.
            text: The text to display or process.
            font_size: The font size in pixels.

        Returns:
            The requested result.
        """
        self.rect = pr.Rectangle(pos_x, pos_y, width, height)
        self.text = text
        self.font_size = font_size
        self.is_clicked = False
        self._is_unloaded = False
        self.initial_text_color = pr.Color(220, 235, 245, 255)
        self.active_text_color = pr.Color(255, 215, 45, 255)
        self.shadow_color = pr.Color(10, 50, 90, 200)

    def unload(self) -> None:
        """Release graphical resources owned by the component.

        Returns:
            The requested result.
        """
        if self._is_unloaded:
            return
        self._is_unloaded = True

    def render(self, is_focused: bool = False) -> None:
        """Render the component for the current frame.

        Args:
            is_focused: Whether the menu button is keyboard-focused.

        Returns:
            The requested result.
        """
        self.is_clicked = False

        mouse_pos = pr.get_mouse_position()
        is_hovered = ft_check_collision_point_rec(mouse_pos, self.rect)
        active = is_focused or is_hovered

        if active and pr.is_mouse_button_pressed(
            pr.MouseButton.MOUSE_BUTTON_LEFT
        ):
            self.is_clicked = True

        current_color = (
            self.active_text_color if active else self.initial_text_color
        )

        tx, ty = centered_text_position(
            self.text,
            self.rect.x + (self.rect.width / 2),
            self.rect.y,
            self.rect.height,
            self.font_size,
        )
        pr.draw_text(
            self.text,
            int(tx + 2),
            int(ty + 2),
            self.font_size,
            self.shadow_color,
        )
        pr.draw_text(
            self.text,
            int(tx),
            int(ty),
            self.font_size,
            current_color,
        )

        if active:
            arrow_size = int(self.font_size * 0.75)
            arrow_x = int(tx - arrow_size - 12)
            arrow_y = int(ty + (self.font_size - arrow_size) / 2)

            v1 = pr.Vector2(arrow_x, arrow_y)
            v2 = pr.Vector2(arrow_x, arrow_y + arrow_size)
            v3 = pr.Vector2(arrow_x + arrow_size, arrow_y + (arrow_size / 2))

            pr.draw_triangle(
                pr.Vector2(v1.x + 2, v1.y + 2),
                pr.Vector2(v2.x + 2, v2.y + 2),
                pr.Vector2(v3.x + 2, v3.y + 2),
                self.shadow_color,
            )
            pr.draw_triangle(v1, v2, v3, self.active_text_color)
