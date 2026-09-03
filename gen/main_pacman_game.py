import pyray as pr
import os
from abc import ABC, abstractmethod
from typing import List, Dict


# =========================================================================== #
# 1. ABSTRACT BASE CHARACTER COMPONENT
# =========================================================================== #
class CharacterComponent(ABC):
    def __init__(
        self,
        maze_data: List[List[int]],
        tile_size: int,
        grid_x: int,
        grid_y: int,
        speed: float,
        animation_speed: float
    ) -> None:
        self.maze_data = maze_data
        self.grid_cols = len(maze_data[0]) if maze_data else 0
        self.grid_rows = len(maze_data) if maze_data else 0
        self.tile_size = tile_size
        self.speed = speed
        self.animation_speed = animation_speed
        self.assets_path = "assets"  # Set base folder structure path

        self.grid_pos = pr.Vector2(grid_x, grid_y)
        self.pixel_pos = self.get_tile_center(self.grid_pos)
        self.direction = pr.Vector2(0, 0)
        self.next_direction = pr.Vector2(0, 0)

        self.frame_index = 0
        self.frame_timer = 0.0

        self.load_textures()

    def get_tile_center(self, grid_pos: pr.Vector2) -> pr.Vector2:
        return pr.Vector2(
            grid_pos.x * self.tile_size + self.tile_size // 2,
            grid_pos.y * self.tile_size + self.tile_size // 2
        )

    def load_tex(self, filename: str, fallback_color: pr.Color) -> pr.Texture:
        path = os.path.join(self.assets_path, filename)
        if not os.path.exists(path):
            img = pr.gen_image_color(
                self.tile_size, self.tile_size, fallback_color
            )
        else:
            img = pr.load_image(path)
            pr.image_resize(img, self.tile_size, self.tile_size)
        tex = pr.load_texture_from_image(img)
        pr.unload_image(img)
        return tex

    def check_wall_collision(self, gx: int, gy: int, dx: int, dy: int) -> bool:
        if not (0 <= gx < self.grid_cols and 0 <= gy < self.grid_rows):
            return True
        cell = self.maze_data[int(gy)][int(gx)]
        if cell == 15:
            return True
        if dy == -1 and (cell & 1):
            return True
        if dx == 1 and (cell & 2):
            return True
        if dy == 1 and (cell & 4):
            return True
        if dx == -1 and (cell & 8):
            return True

        nx, ny = int(gx + dx), int(gy + dy)
        if 0 <= nx < self.grid_cols and 0 <= ny < self.grid_rows:
            next_cell = self.maze_data[ny][nx]
            if next_cell == 15:
                return True
            if dy == 1 and (next_cell & 1):
                return True
            if dx == -1 and (next_cell & 2):
                return True
            if dy == -1 and (next_cell & 4):
                return True
            if dx == 1 and (next_cell & 8):
                return True
            return False
        return True

    def update_movement_and_grid(self) -> None:
        center = self.get_tile_center(self.grid_pos)
        if (
            abs(self.pixel_pos.x - center.x) < self.speed
            and abs(self.pixel_pos.y - center.y) < self.speed
        ):
            if not self.check_wall_collision(
                int(self.grid_pos.x), int(self.grid_pos.y),
                int(self.next_direction.x), int(self.next_direction.y)
            ):
                self.direction = self.next_direction
                self.on_direction_changed()
            if self.check_wall_collision(
                int(self.grid_pos.x), int(self.grid_pos.y),
                int(self.direction.x), int(self.direction.y)
            ):
                self.direction = pr.Vector2(0, 0)
                self.pixel_pos = center

        self.pixel_pos.x += self.direction.x * self.speed
        self.pixel_pos.y += self.direction.y * self.speed
        self.grid_pos.x = int(self.pixel_pos.x // self.tile_size)
        self.grid_pos.y = int(self.pixel_pos.y // self.tile_size)

    def update_animation_timer(self) -> None:
        self.frame_timer += pr.get_frame_time()
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0.0
            self.frame_index += 1

    @abstractmethod
    def load_textures(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    def on_direction_changed(self) -> None:
        pass


# =========================================================================== #
# 2. PACMAN CHARACTER IMPLEMENTATION
# =========================================================================== #
class PacmanCharacter(CharacterComponent):
    def load_textures(self) -> None:
        self.move_textures = [
            self.load_tex("pacman/pacman_closed.png", pr.YELLOW),
            self.load_tex("pacman/pacman_move_0.png", pr.YELLOW),
            self.load_tex("pacman/pacman_move_1.png", pr.YELLOW)
        ]
        self.death_textures = [self.load_tex(f"pacman/pacman_death{i}.png", pr.ORANGE) for i in range(11)]
        self.rotation = 0.0
        self.is_dead = False

    def on_direction_changed(self) -> None:
        if self.direction.x == 1:    self.rotation = 0.0
        elif self.direction.x == -1: self.rotation = 180.0
        elif self.direction.y == -1: self.rotation = 270.0
        elif self.direction.y == 1:  self.rotation = 90.0

    def update(self) -> None:
        if self.is_dead:
            # When dead, stop all movement immediately and loop only death frames up to the final one
            self.direction = pr.Vector2(0, 0)
            self.next_direction = pr.Vector2(0, 0)
            
            self.frame_timer += pr.get_frame_time()
            if self.frame_timer >= self.animation_speed:
                self.frame_timer = 0.0
                if self.frame_index < len(self.death_textures) - 1:
                    self.frame_index += 1
            return

        # Regular processing when alive
        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):   self.next_direction = pr.Vector2(1, 0)
        elif pr.is_key_down(pr.KeyboardKey.KEY_LEFT):  self.next_direction = pr.Vector2(-1, 0)
        elif pr.is_key_down(pr.KeyboardKey.KEY_UP):    self.next_direction = pr.Vector2(0, -1)
        elif pr.is_key_down(pr.KeyboardKey.KEY_DOWN):  self.next_direction = pr.Vector2(0, 1)

        self.update_movement_and_grid()
        self.update_animation_timer()

    def render(self) -> None:
        if self.is_dead:
            tex = self.death_textures[self.frame_index]
        else:
            tex = self.move_textures[self.frame_index % len(self.move_textures)]

        pr.draw_texture_pro(
            tex, pr.Rectangle(0, 0, tex.width, tex.height),
            pr.Rectangle(self.pixel_pos.x, self.pixel_pos.y, self.tile_size, self.tile_size),
            pr.Vector2(self.tile_size / 2, self.tile_size / 2), self.rotation, pr.WHITE
        )


# ============================================================================ #
# 3. GHOST CHARACTER IMPLEMENTATION
# ============================================================================ #
class GhostCharacter(CharacterComponent):
    def load_textures(self) -> None:
        self.ghost_move_textures: Dict[int, List[pr.Texture]] = {
            0: [self.load_tex("ghost/ghost0_d0_0.png", pr.ORANGE), self.load_tex("ghost/ghost0_d0_1.png", pr.ORANGE)],
            1: [self.load_tex("ghost/ghost0_d1_0.png", pr.ORANGE), self.load_tex("ghost/ghost0_d1_1.png", pr.ORANGE)],
            2: [self.load_tex("ghost/ghost0_d2_0.png", pr.ORANGE), self.load_tex("ghost/ghost0_d2_1.png", pr.ORANGE)],
            3: [self.load_tex("ghost/ghost0_d3_0.png", pr.ORANGE), self.load_tex("ghost/ghost0_d3_1.png", pr.ORANGE)]
        }
        self.ghost_edible_textures = [
            self.load_tex("ghost/edible_blue0.png", pr.BLUE),
            self.load_tex("ghost/edible_blue1.png", pr.BLUE)
        ]
        self.look_id = 1
        self.direction = pr.Vector2(-1, 0)
        self.next_direction = pr.Vector2(-1, 0)
        self.is_edible = False
        self.is_frozen = False  # Allows freezing ghost when Pacman is dying

    def on_direction_changed(self) -> None:
        if self.direction.x == 1:    self.look_id = 0
        elif self.direction.x == -1: self.look_id = 1
        elif self.direction.y == -1: self.look_id = 2
        elif self.direction.y == 1:  self.look_id = 3

    def update(self) -> None:
        if self.is_frozen:
            return

        center = self.get_tile_center(self.grid_pos)
        if abs(self.pixel_pos.x - center.x) < self.speed and abs(self.pixel_pos.y - center.y) < self.speed:
            if self.check_wall_collision(int(self.grid_pos.x), int(self.grid_pos.y), int(self.direction.x), int(self.direction.y)):
                all_dirs = [pr.Vector2(1, 0), pr.Vector2(-1, 0), pr.Vector2(0, -1), pr.Vector2(0, 1)]
                for d in all_dirs:
                    if not self.check_wall_collision(int(self.grid_pos.x), int(self.grid_pos.y), int(d.x), int(d.y)):
                        self.next_direction = d
                        break

        self.update_movement_and_grid()
        self.update_animation_timer()

    def render(self) -> None:
        if self.is_edible:
            tex = self.ghost_edible_textures[self.frame_index % len(self.ghost_edible_textures)]
        else:
            seq = self.ghost_move_textures[self.look_id]
            tex = seq[self.frame_index % len(seq)]

        pr.draw_texture_pro(
            tex, pr.Rectangle(0, 0, tex.width, tex.height),
            pr.Rectangle(self.pixel_pos.x, self.pixel_pos.y, self.tile_size, self.tile_size),
            pr.Vector2(self.tile_size / 2, self.tile_size / 2), 0.0, pr.WHITE
        )


# ============================================================================ #
# 4. MAZE RENDERING COMPONENT
# ============================================================================ #
class MazeComponent:
    def __init__(
        self, maze: List[List[int]], x: int, y: int, scale: int,
        wall_thickness: float, color: pr.Color, logo_color: pr.Color = pr.BLUE
    ) -> None:
        self.maze = maze
        self.offset_x = x
        self.offset_y = y
        self.scale = scale
        self.wall_thickness = wall_thickness
        self.color = color
        self.logo_color = logo_color
        self.shadow_color = pr.fade(pr.BLACK, 0.4)

    def _draw_maze_lines(self, thickness: float, color: pr.Color) -> None:
        radius = thickness / 2.0
        for r in range(len(self.maze)):
            for c in range(len(self.maze[0])):
                cell = self.maze[r][c]
                if cell == 15:
                    continue
                x = c * self.scale + self.offset_x
                y = r * self.scale + self.offset_y

                if cell & 1:
                    pr.draw_line_ex(pr.Vector2(x, y), pr.Vector2(x + self.scale, y), thickness, color)
                    pr.draw_circle_v(pr.Vector2(x, y), radius, color)
                    pr.draw_circle_v(pr.Vector2(x + self.scale, y), radius, color)
                if cell & 2:
                    pr.draw_line_ex(pr.Vector2(x + self.scale, y), pr.Vector2(x + self.scale, y + self.scale), thickness, color)
                    pr.draw_circle_v(pr.Vector2(x + self.scale, y), radius, color)
                    pr.draw_circle_v(pr.Vector2(x + self.scale, y + self.scale), radius, color)
                if cell & 4:
                    pr.draw_line_ex(pr.Vector2(x, y + self.scale), pr.Vector2(x + self.scale, y + self.scale), thickness, color)
                    pr.draw_circle_v(pr.Vector2(x, y + self.scale), radius, color)
                    pr.draw_circle_v(pr.Vector2(x + self.scale, y + self.scale), radius, color)
                if cell & 8:
                    pr.draw_line_ex(pr.Vector2(x, y), pr.Vector2(x, y + self.scale), thickness, color)
                    pr.draw_circle_v(pr.Vector2(x, y), radius, color)
                    pr.draw_circle_v(pr.Vector2(x, y + self.scale), radius, color)

    def render(self) -> None:
        self._draw_maze_lines(self.wall_thickness * 4.5, self.shadow_color)
        self._draw_maze_lines(self.wall_thickness * 2.5, self.color)
        self._draw_maze_lines(self.wall_thickness * 1.2, pr.BLACK)

        for r in range(len(self.maze)):
            for c in range(len(self.maze[0])):
                if self.maze[r][c] == 15:
                    x = c * self.scale + self.offset_x
                    y = r * self.scale + self.offset_y
                    pr.draw_rectangle(int(x - 2), int(y - 2), int(self.scale + 4), int(self.scale + 4), self.shadow_color)
                    pr.draw_rectangle(int(x + 1), int(y + 1), self.scale - 2, self.scale - 2, self.logo_color)


# ============================================================================ #
# 5. MAIN GAME SYSTEM MANAGER
# ============================================================================ #
class PacmanGame:
    def __init__(self) -> None:
        self.tile_size = 32
        self.grid_cols = 19
        self.grid_rows = 11

        self.screen_width = self.grid_cols * self.tile_size
        self.screen_height = self.grid_rows * self.tile_size
        pr.init_window(self.screen_width, self.screen_height, "Pacman Game Over & Immobility Showcase")
        pr.set_target_fps(60)

        self.animation_speed = 0.12

        self.maze_data = [
            [11, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6],
            [ 9, 0, 0, 0, 0, 0, 0, 0, 0,15, 0, 0, 0, 0, 0, 0, 0, 0,12],
            [ 9, 0,11, 3, 6, 0,11, 3, 2,15, 8, 3, 6, 0,11, 3, 6, 0,12],
            [ 9, 0, 9, 0,12, 0, 9, 0, 0, 0, 0, 0,12, 0, 9, 0,12, 0,12],
            [ 9, 0, 9, 0,12, 0, 8, 3, 3, 3, 3, 3, 1, 0, 9, 0,12, 0,12],
            [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [ 9, 0,13, 3, 7, 0,11, 3, 3, 3, 3, 3, 6, 0,13, 3, 7, 0,12],
            [ 9, 0, 0, 0, 0, 0,12, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0,12],
            [ 9, 0,11, 3, 6, 0, 9, 0,11, 3, 6, 0,12, 0,11, 3, 6, 0,12],
            [ 9, 0, 8, 3, 2, 0, 0, 0, 8, 3, 2, 0, 0, 0, 8, 3, 2, 0,12],
            [ 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,12]
        ]

        self.maze_renderer = MazeComponent(self.maze_data, 0, 0, self.tile_size, 2.5, pr.SKYBLUE)

        # Instantiate characters
        self.pacman = PacmanCharacter(
            maze_data=self.maze_data, tile_size=self.tile_size,
            grid_x=1, grid_y=1, speed=2.0, animation_speed=self.animation_speed
        )

        self.ghost = GhostCharacter(
            maze_data=self.maze_data, tile_size=self.tile_size,
            grid_x=17, grid_y=9, speed=1.5, animation_speed=self.animation_speed
        )

    def check_character_collision(self) -> bool:
        collision_distance = self.tile_size * 0.75
        distance = pr.vector2_distance(
            self.pacman.pixel_pos, self.ghost.pixel_pos
        )
        return distance < collision_distance

    def update(self) -> None:
        if not self.pacman.is_dead:
            if pr.is_key_pressed(pr.KeyboardKey.KEY_G):
                self.ghost.is_edible = not self.ghost.is_edible
            if self.check_character_collision():
                self.pacman.is_dead = True
                self.pacman.frame_index = 0
                self.ghost.is_frozen = True

        self.pacman.update()
        self.ghost.update()

    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        self.maze_renderer.render()
        self.pacman.render()
        self.ghost.render()

        if self.pacman.is_dead:
            pr.draw_text("GAME OVER", self.screen_width // 2 - 70, self.screen_height // 2 - 15, 28, pr.RED)
            pr.draw_text("Pacman is immobile.", self.screen_width // 2 - 75, self.screen_height // 2 + 20, 16, pr.RAYWHITE)
        else:
            pr.draw_text("ARROWS: Move | [G]: Toggle Ghost Edible State", 15, self.screen_height - 25, 14, pr.RAYWHITE)

        pr.end_drawing()

    def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
        pr.unload_texture(self.pacman.move_textures[0])
        pr.unload_texture(self.pacman.move_textures[1])
        pr.unload_texture(self.pacman.move_textures[2])
        for t in self.pacman.death_textures:
            pr.unload_texture(t)
        for d_list in self.ghost.ghost_move_textures.values():
            for t in d_list:
                pr.unload_texture(t)
        pr.unload_texture(self.ghost.ghost_edible_textures[0])
        pr.unload_texture(self.ghost.ghost_edible_textures[1])

        pr.close_window()


if __name__ == "__main__":
    game = PacmanGame()
    game.run()
