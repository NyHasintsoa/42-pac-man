import pyray as rl


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = rl.Rectangle(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_clicked = False

    def draw(self):
        # 1. Get mouse position
        mouse_pos = rl.get_mouse_position()

        # 2. Check for hover
        is_hovered = rl.check_collision_point_rec(mouse_pos, self.rect)

        # 3. Determine current color based on hover
        current_color = self.hover_color if is_hovered else self.color

        # 4. Handle Click logic
        self.is_clicked = False
        if is_hovered and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            self.is_clicked = True

        # 5. Draw the button body
        rl.draw_rectangle_rec(self.rect, current_color)
        rl.draw_rectangle_lines_ex(self.rect, 2, rl.GRAY)  # Add a border

        # 6. Center the text inside the button
        font_size = 20
        text_width = rl.measure_text(self.text, font_size)
        text_x = self.rect.x + (self.rect.width - text_width) // 2
        text_y = self.rect.y + (self.rect.height - font_size) // 2

        rl.draw_text(self.text, int(text_x), int(text_y), font_size, self.text_color)


def main():
    rl.init_window(800, 600, "Raylib Python - Button Component")
    rl.set_target_fps(60)

    # Create instances of our buttons
    start_btn = Button(
        300, 200, 200, 50, "START GAME", rl.DARKGRAY, rl.MAROON, rl.WHITE
    )
    exit_btn = Button(300, 280, 200, 50, "EXIT", rl.DARKGRAY, rl.DARKBLUE, rl.WHITE)

    while not rl.window_should_close():
        # Update / Logic
        if start_btn.is_clicked:
            print("Transitioning to Level Menu...")
            # You would change your state variable here

        if exit_btn.is_clicked:
            break  # Close the app

        # Drawing
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        start_btn.draw()
        exit_btn.draw()

        rl.end_drawing()

    rl.close_window()


if __name__ == "__main__":
    main()
