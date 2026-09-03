import pyray as pr
import os
from typing import List
from mazegenerator import MazeGenerator


class PacmanGame:
    def __init__(self) -> None:
        self.tile_size = 50  # Increased for better maze visibility
        self.grid_cols = 20
        self.grid_rows = 20

        # --- Maze Generation Placeholder ---
        self.maze_gen = MazeGenerator(
            (self.grid_cols, self.grid_rows),
            False, (0, 0), (self.grid_cols - 1, self.grid_rows - 1)
        )
        self.maze_gen.generate()
        self.maze: List[List[int]] = self.maze_gen.maze
        # -----------------------------------
        # self.maze = [
        #     [
        #         15 if (r == 0 or r == 19 or c == 0 or c == 19) else 0
        #         for c in range(self.grid_cols)
        #     ] for r in range(self.grid_rows)
        # ]
        # -----------------------------------

        self.screen_width = self.grid_cols * self.tile_size
        self.screen_height = self.grid_rows * self.tile_size
        pr.init_window(self.screen_width, self.screen_height, "Pacman Maze")
        pr.set_target_fps(60)

        # Neon Wall Properties
        self.wall_thickness = 2.0
        self.wall_color = pr.Color(4, 4, 214, 255)
        self.logo_color = pr.Color(33, 208, 220, 255)
        self.offset_x = 0
        self.offset_y = 0
        self.grid_pos = pr.Vector2(
            (self.grid_cols // 2) - 1, self.grid_rows // 2
        )
        self.pixel_pos = pr.Vector2(
            self.grid_pos.x * self.tile_size + self.tile_size // 2,
            self.grid_pos.y * self.tile_size + self.tile_size // 2
        )
        self.direction = pr.Vector2(0, 0)
        self.next_direction = pr.Vector2(0, 0)
        self.speed = 3
        self.rotation = 0.0

        # Assets
        self.assets_path = "assets/pacman"
        self.move_textures = [
            self.load_tex("pacman_move_1.png"),
            self.load_tex("pacman_move_0.png")
        ]
        self.frame_index = 0
        self.frame_timer = 0.0

    def load_tex(self, filename: str) -> pr.Texture:
        path = os.path.join(self.assets_path, filename)
        if not os.path.exists(path):
            img = pr.gen_image_color(self.tile_size, self.tile_size, pr.YELLOW)
        else:
            img = pr.load_image(path)
        pr.image_resize(img, self.tile_size, self.tile_size)
        tex = pr.load_texture_from_image(img)
        pr.unload_image(img)
        return tex

    def can_move(
        self, curr_x: int, curr_y: int, dir_x: int, dir_y: int
    ) -> bool:
        cell_value = self.maze[int(curr_y)][int(curr_x)]
        if cell_value == 15:
            return False
        if dir_y == -1 and (cell_value & 1):
            return False  # Blocked North
        if dir_x == 1 and (cell_value & 2):
            return False  # Blocked East
        if dir_y == 1 and (cell_value & 4):
            return False  # Blocked South
        if dir_x == -1 and (cell_value & 8):
            return False  # Blocked West

        # Check the destination cell's opposite wall (for boundary safety)
        next_x, next_y = int(curr_x + dir_x), int(curr_y + dir_y)
        if 0 <= next_x < self.grid_cols and 0 <= next_y < self.grid_rows:
            next_cell = self.maze[next_y][next_x]
            if next_cell == 15:
                return False  # Can't enter solid blocks
            if dir_y == 1 and (next_cell & 1):
                return False  # Next cell blocks from North
            if dir_x == -1 and (next_cell & 2):
                return False  # Next cell blocks from East
            if dir_y == -1 and (next_cell & 4):
                return False  # Next cell blocks from South
            if dir_x == 1 and (next_cell & 8):
                return False  # Next cell blocks from West
            return True
        return False

    def _draw_maze_lines(self, thickness: float, color: pr.Color) -> None:
        half_t = thickness / 2.0
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell = self.maze[r][c]
                if cell == 15:
                    continue  # Drawn separately as solid blocks
                x = c * self.tile_size + self.offset_x
                y = r * self.tile_size + self.offset_y

                # Bitwise wall drawing
                if cell & 1:  # North
                    pr.draw_line_ex(
                        pr.Vector2(x, y),
                        pr.Vector2(x + self.tile_size, y), thickness, color
                    )
                    pr.draw_circle(int(x), int(y), int(half_t), color)
                if cell & 2:  # East
                    pr.draw_line_ex(
                        pr.Vector2(x + self.tile_size, y),
                        pr.Vector2(x + self.tile_size, y + self.tile_size),
                        thickness, color
                    )
                    pr.draw_circle(
                        int(x + self.tile_size), int(y), int(half_t), color
                    )
                if cell & 4:  # South
                    pr.draw_line_ex(
                        pr.Vector2(x, y + self.tile_size),
                        pr.Vector2(x + self.tile_size, y + self.tile_size),
                        thickness, color
                    )
                    pr.draw_circle(
                        int(x), int(y + self.tile_size), int(half_t), color
                    )
                if cell & 8:  # West
                    pr.draw_line_ex(
                        pr.Vector2(x, y), pr.Vector2(x, y + self.tile_size),
                        thickness, color
                    )
                    pr.draw_circle(int(x), int(y), int(half_t), color)

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        # Layer 1: Outer Neon Glow
        self._draw_maze_lines(self.wall_thickness * 2.5, self.wall_color)
        # Layer 2: Inner Core
        self._draw_maze_lines(self.wall_thickness * 1.2, pr.BLACK)

        # Layer 3: Solid Blocks (Logo/Fill)
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                if self.maze[r][c] == 15:
                    pr.draw_rectangle(
                        c * self.tile_size + 1,
                        r * self.tile_size + 1,
                        self.tile_size - 2,
                        self.tile_size - 2,
                        self.logo_color
                    )

        # Layer 4: Pacman
        tex = self.move_textures[self.frame_index]
        pr.draw_texture_pro(
            tex, pr.Rectangle(0, 0, tex.width, tex.height),
            pr.Rectangle(
                self.pixel_pos.x,
                self.pixel_pos.y,
                self.tile_size,
                self.tile_size
            ),
            pr.Vector2(self.tile_size / 2, self.tile_size / 2),
            self.rotation,
            pr.WHITE
        )
        pr.end_drawing()

    def handle_input(self) -> None:
        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            self.next_direction = pr.Vector2(1, 0)
        elif pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            self.next_direction = pr.Vector2(-1, 0)
        elif pr.is_key_down(pr.KeyboardKey.KEY_UP):
            self.next_direction = pr.Vector2(0, -1)
        elif pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
            self.next_direction = pr.Vector2(0, 1)

    def update(self) -> None:
        self.handle_input()

        # Current Tile Center
        center_x = self.grid_pos.x * self.tile_size + self.tile_size // 2
        center_y = self.grid_pos.y * self.tile_size + self.tile_size // 2

        # Grid-based movement logic
        if (
            abs(self.pixel_pos.x - center_x) < self.speed
            and abs(self.pixel_pos.y - center_y) < self.speed
        ):
            # Check if we can change to next_direction
            if self.can_move(
                int(self.grid_pos.x), int(self.grid_pos.y),
                int(self.next_direction.x), int(self.next_direction.y)
            ):
                self.direction = self.next_direction
                # Update rotation
                if self.direction.x == 1:
                    self.rotation = 0
                elif self.direction.x == -1:
                    self.rotation = 180
                elif self.direction.y == -1:
                    self.rotation = 270
                elif self.direction.y == 1:
                    self.rotation = 90

            # Stop if hitting a wall in current direction
            if not self.can_move(
                int(self.grid_pos.x), int(self.grid_pos.y),
                int(self.direction.x), int(self.direction.y)
            ):
                self.direction = pr.Vector2(0, 0)
                self.pixel_pos = pr.Vector2(center_x, center_y)

        self.pixel_pos.x += self.direction.x * self.speed
        self.pixel_pos.y += self.direction.y * self.speed

        # Update current grid position
        self.grid_pos.x = int(self.pixel_pos.x // self.tile_size)
        self.grid_pos.y = int(self.pixel_pos.y // self.tile_size)

        # Animation
        if self.direction.x != 0 or self.direction.y != 0:
            self.frame_timer += pr.get_frame_time()
            if self.frame_timer > 0.1:
                self.frame_timer = 0
                self.frame_index = (self.frame_index + 1) % len(
                    self.move_textures
                )

    def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
        pr.close_window()


if __name__ == "__main__":
    game = PacmanGame()
    game.run()
