import pyray as rl

# --- Constants for States ---
STATE_MAIN_MENU = 0
STATE_LEVEL_MENU = 1


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = rl.Rectangle(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_clicked = False

    def update_and_draw(self):
        """Updates the button logic and draws it to the screen."""
        mouse_pos = rl.get_mouse_position()
        is_hovered = rl.check_collision_point_rec(mouse_pos, self.rect)

        # Determine color
        current_color = self.hover_color if is_hovered else self.color

        # Check click (Mouse Button Left Pressed)
        self.is_clicked = False
        if is_hovered and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            self.is_clicked = True

        # Draw Button
        rl.draw_rectangle_rec(self.rect, current_color)
        rl.draw_rectangle_lines_ex(self.rect, 2, rl.GRAY)

        # Center Text
        font_size = 20
        text_width = rl.measure_text(self.text, font_size)
        tx = self.rect.x + (self.rect.width - text_width) / 2
        ty = self.rect.y + (self.rect.height - font_size) / 2
        rl.draw_text(self.text, int(tx), int(ty), font_size, self.text_color)


def main():
    rl.init_window(800, 600, "Pacman State Transitions")
    rl.set_target_fps(60)

    # Track current state
    current_state = STATE_MAIN_MENU

    # --- Initialize Buttons ---
    # Main Menu Buttons
    btn_play = Button(300, 250, 200, 50, "PLAY GAME", rl.DARKGRAY, rl.YELLOW, rl.BLACK)
    btn_exit = Button(300, 320, 200, 50, "QUIT", rl.DARKGRAY, rl.RED, rl.WHITE)

    # Level Menu Buttons
    btn_back = Button(50, 50, 100, 40, "BACK", rl.GRAY, rl.MAROON, rl.WHITE)
    btn_lvl1 = Button(300, 250, 200, 50, "CLASSIC MAZE", rl.BLUE, rl.SKYBLUE, rl.WHITE)

    while not rl.window_should_close():
        # --- UPDATE & DRAW ---
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        if current_state == STATE_MAIN_MENU:
            rl.draw_text("PACMAN MAIN MENU", 220, 100, 40, rl.YELLOW)

            btn_play.update_and_draw()
            btn_exit.update_and_draw()

            if btn_play.is_clicked:
                current_state = STATE_LEVEL_MENU

            if btn_exit.is_clicked:
                break  # Close window

        elif current_state == STATE_LEVEL_MENU:
            rl.draw_text("SELECT A LEVEL", 270, 100, 30, rl.RAYWHITE)

            btn_lvl1.update_and_draw()
            btn_back.update_and_draw()

            if btn_back.is_clicked:
                current_state = STATE_MAIN_MENU

            if btn_lvl1.is_clicked:
                # Here you would trigger the actual game loop
                print("Starting Level 1...")

        rl.end_drawing()

    rl.close_window()


if __name__ == "__main__":
    main()
