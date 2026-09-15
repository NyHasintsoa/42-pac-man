"""Capture and render player text input."""

import pyray as pr

import time
from src.graphic.utils.text_helper import centered_y


class Input:
    """Represent a bounded text input field."""

    def __init__(
        self,
        pos_x: int,
        pos_y: int,
        width: int,
        height: int,
        default_value: str = "",
        max_chars: int = 12,
    ) -> None:
        """Initialize the Input instance.

        Args:
            pos_x: The horizontal position or grid coordinate.
            pos_y: The vertical position or grid coordinate.
            width: The width in tiles or pixels.
            height: The height in tiles or pixels.
            default_value: The initial input value.
            max_chars: The maximum number of accepted characters.

        Returns:
            The requested result.
        """
        self.box_x = pos_x
        self.box_y = pos_y
        self.box_width = width
        self.box_height = height
        self.max_chars = max_chars
        self.value = default_value

    def clear(self) -> None:
        """Clear the current input value.

        Returns:
            The requested result.
        """
        self.value = ""

    def update(self) -> None:
        """Update component state from current input or timers.

        Returns:
            The requested result.
        """
        key = pr.get_char_pressed()
        while key > 0:
            char_pressed = chr(key)

            if (char_pressed.isalnum() or char_pressed == "-") and (
                len(self.value) < self.max_chars
            ):
                self.value += char_pressed
            key = pr.get_char_pressed()

        if (
            pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE)
            and len(self.value) > 0
        ):
            self.value = self.value[:-1]

    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        pr.draw_rectangle_lines(
            self.box_x, self.box_y, self.box_width, self.box_height, pr.SKYBLUE
        )

        display_text = self.value
        if int(time.perf_counter() * 2) % 2 == 0:
            display_text += "_"

        pr.draw_text(
            display_text,
            self.box_x + 15,
            centered_y(self.box_y, self.box_height, 24),
            24,
            pr.WHITE,
        )
