"""Small helpers for positioning raylib's built-in font."""

import pyray as pr


def text_width(text: str, font_size: int) -> int:
    """Return the rendered width of text."""
    return pr.measure_text(text, font_size)


def centered_x(text: str, center_x: float, font_size: int) -> int:
    """Return the x coordinate that centers text around a point."""
    return int(center_x - (text_width(text, font_size) / 2))


def centered_y(top: float, height: float, font_size: int) -> int:
    """Return the y coordinate that centers text in a region."""
    return int(top + ((height - font_size) / 2))


def centered_text_position(
    text: str,
    center_x: float,
    top: float,
    height: float,
    font_size: int,
) -> tuple[int, int]:
    """Return coordinates that center text in a horizontal region."""
    return centered_x(text, center_x, font_size), centered_y(
        top, height, font_size
    )
