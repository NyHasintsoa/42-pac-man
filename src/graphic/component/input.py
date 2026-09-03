import pyray as pr


class Input:
    def __init__(
        self,
        pos_x: int,
        pos_y: int,
        width: int,
        height: int,
        default_value: str = "",
        max_chars: int = 12,
    ) -> None:
        self.box_x = pos_x
        self.box_y = pos_y
        self.box_width = width
        self.box_height = height
        self.max_chars = max_chars
        self.value = default_value

    def clear(self) -> None:
        self.value = ""

    def update(self) -> None:
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
        pr.draw_rectangle_lines(
            self.box_x, self.box_y, self.box_width, self.box_height, pr.SKYBLUE
        )

        display_text = self.value
        if int(pr.get_time() * 2) % 2 == 0:
            display_text += "_"

        pr.draw_text(
            display_text, self.box_x + 15, self.box_y + 13, 24, pr.WHITE
        )
