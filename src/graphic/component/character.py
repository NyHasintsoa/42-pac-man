import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

import pyray as pr

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class CharacterComponent(ABC):
    def __init__(
        self,
        maze_data: List[List[int]],
        pos_x: int,
        pos_y: int,
        speed: float,
        animation_speed: float,
        window: "MainWindow",
        margin_top: int = 80,
        margin_bottom: int = 30,
        padding_x: int = 20,
    ) -> None:
        self.maze_data = maze_data
        self.grid_cols = len(maze_data[0]) if maze_data else 0
        self.grid_rows = len(maze_data) if maze_data else 0
        self.animation_speed = animation_speed
        self.assets_path: str
        self._loaded_textures: List[pr.Texture] = []
        self._is_unloaded = False
        available_width = float(window.width - (padding_x * 2))
        available_height = float(
            window.height - margin_top - (padding_x * 2) - margin_bottom
        )
        scale_x = (
            available_width / self.grid_cols if self.grid_cols > 0 else 1.0
        )
        scale_y = (
            available_height / self.grid_rows if self.grid_rows > 0 else 1.0
        )
        self.scale = min(scale_x, scale_y)

        self.offset_x = (window.width - (self.grid_cols * self.scale)) / 2.0
        self.offset_y = (
            margin_top
            + (available_height - (self.grid_rows * self.scale)) / 2.0
        )
        self.speed = speed
        self.grid_pos = pr.Vector2(pos_x, pos_y)
        self.pixel_pos = self.get_pixel_position(self.grid_pos)
        self.direction = pr.Vector2(0, 0)
        self.next_direction = pr.Vector2(0, 0)
        self.frame_index = 0
        self.frame_timer = 0.0
        self.load_textures()

    def get_pixel_position(self, grid_pos: pr.Vector2) -> pr.Vector2:
        return pr.Vector2(
            grid_pos.x * self.scale + self.offset_x + (self.scale / 2.0),
            grid_pos.y * self.scale + self.offset_y + (self.scale / 2.0),
        )

    def load_tex(self, filename: str, fallback_color: pr.Color) -> pr.Texture:
        path = os.path.join(self.assets_path, filename)
        size = int(self.scale) if int(self.scale) > 0 else 1

        if not os.path.exists(path):
            img = pr.gen_image_color(size, size, fallback_color)
        else:
            img = pr.load_image(path)
            pr.image_resize(img, size, size)
        tex = pr.load_texture_from_image(img)
        pr.unload_image(img)
        self._loaded_textures.append(tex)
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
        center = self.get_pixel_position(self.grid_pos)
        if (
            abs(self.pixel_pos.x - center.x) < self.speed
            and abs(self.pixel_pos.y - center.y) < self.speed
        ):
            if not self.check_wall_collision(
                int(self.grid_pos.x),
                int(self.grid_pos.y),
                int(self.next_direction.x),
                int(self.next_direction.y),
            ):
                self.direction = self.next_direction
                self.on_direction_changed()
            if self.check_wall_collision(
                int(self.grid_pos.x),
                int(self.grid_pos.y),
                int(self.direction.x),
                int(self.direction.y),
            ):
                self.direction = pr.Vector2(0, 0)
                self.pixel_pos = center

        self.pixel_pos.x += self.direction.x * self.speed
        self.pixel_pos.y += self.direction.y * self.speed

        self.grid_pos.x = int((self.pixel_pos.x - self.offset_x) // self.scale)
        self.grid_pos.y = int((self.pixel_pos.y - self.offset_y) // self.scale)

    def update_animation_timer(self) -> None:
        self.frame_timer += pr.get_frame_time()
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0.0
            self.frame_index += 1

    def unload(self) -> None:
        if self._is_unloaded:
            return
        for texture in list(self._loaded_textures):
            pr.unload_texture(texture)
        self._loaded_textures.clear()
        self._is_unloaded = True

    @abstractmethod
    def load_textures(self) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def on_direction_changed(self) -> None:
        pass
