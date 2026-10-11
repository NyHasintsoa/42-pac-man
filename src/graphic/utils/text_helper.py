"""Small helpers for positioning raylib's built-in font."""


def text_width(text: str, font_size: int) -> int:
    """Measure the width of a string in pixels.

    Args:
        text (str): The string to measure.
        font_size (int): Target font size in pixels.

    Returns:
        int: Width of the rendered text in pixels.
    """
    if not text:
        return 0

    BASE_FONT_SIZE = 10.0
    scale_factor = font_size / BASE_FONT_SIZE
    spacing = font_size / 10.0

    DEFAULT_ADVANCE = 6.0
    GLYPH_ADVANCES = {
        "i": 2.0,
        "l": 2.0,
        "|": 2.0,
        "!": 2.0,
        ".": 2.0,
        ",": 2.0,
        ":": 2.0,
        ";": 2.0,
        "'": 2.0,
        "I": 3.0,
        "j": 3.0,
        '"': 3.0,
        "`": 3.0,
        "1": 4.0,
        "t": 4.0,
        "f": 4.0,
        "r": 4.0,
        " ": 4.0,
        "(": 4.0,
        ")": 4.0,
        "[": 4.0,
        "]": 4.0,
        "c": 5.0,
        "k": 5.0,
        "s": 5.0,
        "v": 5.0,
        "x": 5.0,
        "z": 5.0,
        "J": 5.0,
        "-": 5.0,
        "m": 8.0,
        "w": 8.0,
        "W": 8.0,
        "M": 8.0,
        "@": 9.0,
        "%": 8.0,
        "Q": 7.0,
        "#": 7.0,
    }

    max_line_width = 0.0
    current_line_width = 0.0

    for char in text:
        if char == "\n":
            if current_line_width > max_line_width:
                max_line_width = current_line_width
            current_line_width = 0.0
        else:
            advance = GLYPH_ADVANCES.get(char, DEFAULT_ADVANCE)
            current_line_width += (advance * scale_factor) + spacing

    if current_line_width > max_line_width:
        max_line_width = current_line_width

    return int(max_line_width)


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
