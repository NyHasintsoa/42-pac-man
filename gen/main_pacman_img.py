import pyray as pr
import os

class PacmanGame:
    def __init__(self) -> None:
        self.screen_width = 400
        self.screen_height = 400
        pr.init_window(self.screen_width, self.screen_height, "Pacman Directional Demo")
        pr.set_target_fps(60)

        self.animation_speed = 0.12
        self.assets_path = "assets/pacman"
        self.tile_size = 64

        # 2. Load Textures
        self.move_textures = [
            self.load_tex("pacman_closed.png"),
            self.load_tex("pacman_move_0.png"),
            self.load_tex("pacman_move_1.png")
        ]

        self.death_textures = []
        for i in range(11):
            filename = f"pacman_death{i}.png"
            self.death_textures.append(self.load_tex(filename))

        # 3. Animation & Movement State
        self.frame_index = 0
        self.frame_timer = 0.0
        self.is_dead = False
        # Position and Direction
        self.position = pr.Vector2(self.screen_width // 2, self.screen_height // 2)
        self.rotation = 0.0  # Default facing Right
        self.speed = 2.0     # Movement speed pixels per frame

    def load_tex(self, filename: str) -> pr.Texture:
        path = os.path.join(self.assets_path, filename)
        if not os.path.exists(path):
            img = pr.gen_image_color(self.tile_size, self.tile_size, pr.MAGENTA)
        else:
            img = pr.load_image(path)
            pr.image_resize(img, self.tile_size, self.tile_size)

        tex = pr.load_texture_from_image(img)
        pr.unload_image(img)
        return tex

    def handle_input(self) -> None:
        if self.is_dead: return

        # Update Rotation and Position based on keys
        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            self.rotation = 0.0
            self.position.x += self.speed
        elif pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            self.rotation = 180.0
            self.position.x -= self.speed
        elif pr.is_key_down(pr.KeyboardKey.KEY_UP):
            self.rotation = 270.0
            self.position.y -= self.speed
        elif pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
            self.rotation = 90.0
            self.position.y += self.speed

    def update(self) -> None:
        self.handle_input()

        dt = pr.get_frame_time()
        self.frame_timer += dt

        current_sequence = self.death_textures if self.is_dead else self.move_textures

        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.frame_index += 1

            if self.is_dead:
                if self.frame_index >= len(current_sequence):
                    self.frame_index = len(current_sequence) - 1
            else:
                self.frame_index %= len(current_sequence)

        if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
            self.is_dead = not self.is_dead
            self.frame_index = 0

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        current_sequence = self.death_textures if self.is_dead else self.move_textures
        tex = current_sequence[self.frame_index]

        # To rotate the texture around its center:
        # 1. Source rectangle (the whole texture)
        source = pr.Rectangle(0, 0, tex.width, tex.height)
        # 2. Destination rectangle (where it's drawn on screen)
        dest = pr.Rectangle(self.position.x, self.position.y, self.tile_size, self.tile_size)
        # 3. Origin (the center point of the destination rectangle for rotation)
        origin = pr.Vector2(self.tile_size / 2, self.tile_size / 2)

        pr.draw_texture_pro(tex, source, dest, origin, self.rotation, pr.WHITE)

        # UI
        pr.draw_text("ARROWS to Move | SPACE to Die", 10, 10, 20, pr.YELLOW)
        pr.draw_text(f"Rotation: {self.rotation}°", 10, 40, 20, pr.RAYWHITE)

        pr.end_drawing()

    def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
        for t in self.move_textures + self.death_textures:
            pr.unload_texture(t)
        pr.close_window()


if __name__ == "__main__":
    game = PacmanGame()
    game.run()
