import pyray as rl

# Define game states
STATE_MAIN_MENU = 0
STATE_LEVEL_SELECT = 1
STATE_GAMEPLAY = 2


def main():
    # Initialize Window
    screen_width = 800
    screen_height = 600
    rl.init_window(screen_width, screen_height, "Pacman - Main Menu Transition")
    rl.set_target_fps(60)

    # Current state tracker
    current_state = STATE_MAIN_MENU

    while not rl.window_should_close():
        # --- Logic / Update Section ---
        if current_state == STATE_MAIN_MENU:
            if rl.is_key_pressed(rl.KEY_ENTER):
                current_state = STATE_LEVEL_SELECT

        elif current_state == STATE_LEVEL_SELECT:
            if rl.is_key_pressed(rl.KEY_BACKSPACE):
                current_state = STATE_MAIN_MENU
            if rl.is_key_pressed(rl.KEY_ONE):
                current_state = STATE_GAMEPLAY

        # --- Drawing Section ---
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        if current_state == STATE_MAIN_MENU:
            draw_main_menu()
        elif current_state == STATE_LEVEL_SELECT:
            draw_level_menu()
        elif current_state == STATE_GAMEPLAY:
            draw_gameplay()

        rl.end_drawing()

    rl.close_window()


# --- Screen Views ---


def draw_main_menu():
    rl.draw_text("PACMAN", 280, 150, 60, rl.YELLOW)
    rl.draw_text("Press [ENTER] to Start", 270, 350, 20, rl.WHITE)


def draw_level_menu():
    rl.draw_text("SELECT LEVEL", 250, 100, 40, rl.RAYWHITE)
    rl.draw_text("1. Classic Maze", 300, 250, 20, rl.GREEN)
    rl.draw_text("2. Ghost House", 300, 300, 20, rl.RED)
    rl.draw_text("Press [BACKSPACE] for Menu", 250, 500, 20, rl.GRAY)


def draw_gameplay():
    rl.draw_text("GAME STARTING...", 300, 300, 30, rl.YELLOW)
    rl.draw_circle(400, 400, 20, rl.YELLOW)  # Placeholder Pacman


if __name__ == "__main__":
    main()
