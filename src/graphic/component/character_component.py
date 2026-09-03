# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  character_component.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 20:50:28 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 13:23:31 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
import os
from abc import ABC, abstractmethod
from typing import List


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
        self.assets_path: str

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
