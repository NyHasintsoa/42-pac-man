"""Render a clickable rectangular button."""

import pyray as pr

from src.graphic.utils.text_helper import centered_text_position
from src.utils import ft_check_collision_point_rec, ft_fade


class Button:
    """Represent a clickable, styled rectangular button."""

    def __init__(
        self,
        pos_x: int,
        pos_y: int,
        width: int,
        height: int,
        text: str = "Button",
        bg_color: pr.Color = pr.Color(14, 26, 39, 255),
        hover_bg_color: pr.Color = pr.Color(20, 42, 65, 255),
        clicked_color: pr.Color = pr.Color(160, 140, 10, 255),
        text_color: pr.Color = pr.WHITE,
        hover_text_color: pr.Color = pr.Color(15, 215, 228, 255),
        font_size: int = 24,
        border_radius: float = 0.35,
        border_width: int = 4,
        border_color: pr.Color = pr.Color(15, 215, 228, 255),
        disabled: bool = False,
    ) -> None:
        """Initialize the Button instance.

        Args:
            pos_x: The horizontal position or grid coordinate.
            pos_y: The vertical position or grid coordinate.
            width: The width in tiles or pixels.
            height: The height in tiles or pixels.
            text: The text to display or process.
            bg_color: The bg color value.
            hover_bg_color: The hover bg color value.
            clicked_color: The clicked color value.
            text_color: The foreground text color.
            hover_text_color: The hover text color value.
            font_size: The font size in pixels.
            border_radius: The border radius value.
            border_width: The border width value.
            border_color: The border color value.
            disabled: The disabled value.

        Returns:
            The requested result.
        """
        self.rect = pr.Rectangle(pos_x, pos_y, width, height)
        self.text: str = text
        self.bg_color: pr.Color = bg_color
        self.hover_bg_color: pr.Color = hover_bg_color
        self.hover_text_color: pr.Color = hover_text_color
        self.clicked_color: pr.Color = clicked_color
        self.text_color: pr.Color = text_color
        self.border_color: pr.Color = border_color
        self.shadow_color = ft_fade(pr.BLACK, 0.45)
        self.is_clicked = False
        self.font_size = font_size
        self.border_radius = border_radius
        self.border_width = border_width
        self.disabled = disabled

    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        self.is_clicked = False
        current_border_color = self.border_color
        if self.disabled:
            current_color = pr.GRAY
        else:
            mouse_pos = pr.get_mouse_position()
            is_hovered = ft_check_collision_point_rec(mouse_pos, self.rect)

            if is_hovered:
                current_color = self.hover_bg_color
            else:
                current_color = self.bg_color

            if is_hovered and pr.is_mouse_button_pressed(
                pr.MouseButton.MOUSE_BUTTON_LEFT
            ):
                self.is_clicked = True

            if is_hovered and pr.is_mouse_button_down(
                pr.MouseButton.MOUSE_BUTTON_LEFT
            ):
                current_color = self.clicked_color

        text_disp_color = self.text_color

        shadow_rect = pr.Rectangle(
            self.rect.x + 4,
            self.rect.y + 6,
            self.rect.width,
            self.rect.height,
        )
        pr.draw_rectangle_rounded(
            shadow_rect, self.border_radius, 12, self.shadow_color
        )
        border_rect = pr.Rectangle(
            self.rect.x - self.border_width,
            self.rect.y - self.border_width,
            self.rect.width + (self.border_width * 2),
            self.rect.height + (self.border_width * 2),
        )
        pr.draw_rectangle_rounded(
            border_rect, self.border_radius, 12, current_border_color
        )
        pr.draw_rectangle_rounded(
            self.rect, self.border_radius, 12, current_color
        )
        tx, ty = centered_text_position(
            self.text,
            self.rect.x + (self.rect.width / 2),
            self.rect.y,
            self.rect.height,
            self.font_size,
        )
        if current_color != self.clicked_color:
            pr.draw_text(
                str(self.text),
                int(tx + 1),
                int(ty + 1),
                self.font_size,
                pr.fade(pr.WHITE, 0.5),
            )
        pr.draw_text(
            str(self.text), int(tx), int(ty), self.font_size, text_disp_color
        )
