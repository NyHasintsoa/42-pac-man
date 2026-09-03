# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacman_character.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 09:00:00 by nramalan        #+#    #+#               #
#  Updated: 2026/05/17 20:57:30 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import List

from src.graphic.component.character_component import CharacterComponent


class PacmanCharacter(CharacterComponent):
    def __init__(
        self,
        maze_data: List[List[int]],
        tile_size: int,
        grid_x: int,
        grid_y: int,
        speed: float,
        animation_speed: float
    ) -> None:
        self.assets_path = "assets/pacman"
        self.is_dead = False
        super().__init__(
            maze_data, tile_size, grid_x, grid_y, speed, animation_speed
        )

    def load_textures(self) -> None:
        self.move_textures = [
            self.load_tex("pacman_closed.png", pr.YELLOW),
            self.load_tex("pacman_move_0.png", pr.YELLOW),
            self.load_tex("pacman_move_1.png", pr.YELLOW)
        ]
        self.death_textures = [
            self.load_tex(f"pacman_death{i}.png", pr.ORANGE) for i in range(11)
        ]
        self.rotation = 0.0
        self.is_dead = False

    def on_direction_changed(self) -> None:
        if self.direction.x == 1:
            self.rotation = 0.0
        elif self.direction.x == -1:
            self.rotation = 180.0
        elif self.direction.y == -1:
            self.rotation = 270.0
        elif self.direction.y == 1:
            self.rotation = 90.0

    def update(self) -> None:
        if self.is_dead:
            self.direction = pr.Vector2(0, 0)
            self.next_direction = pr.Vector2(0, 0)
            self.frame_timer += pr.get_frame_time()
            if self.frame_timer >= self.animation_speed:
                self.frame_timer = 0.0
                if self.frame_index < len(self.death_textures) - 1:
                    self.frame_index += 1
            return

        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT):
            self.next_direction = pr.Vector2(1, 0)
        elif pr.is_key_down(pr.KeyboardKey.KEY_LEFT):
            self.next_direction = pr.Vector2(-1, 0)
        elif pr.is_key_down(pr.KeyboardKey.KEY_UP):
            self.next_direction = pr.Vector2(0, -1)
        elif pr.is_key_down(pr.KeyboardKey.KEY_DOWN):
            self.next_direction = pr.Vector2(0, 1)

        self.update_movement_and_grid()
        self.update_animation_timer()

    def render(self) -> None:
        if self.is_dead:
            tex = self.death_textures[self.frame_index]
        else:
            tex = self.move_textures[
                self.frame_index % len(self.move_textures)
            ]

        pr.draw_texture_pro(
            tex, pr.Rectangle(0, 0, tex.width, tex.height),
            pr.Rectangle(
                self.pixel_pos.x, self.pixel_pos.y,
                self.tile_size, self.tile_size
            ),
            pr.Vector2(self.tile_size / 2, self.tile_size / 2),
            self.rotation, pr.WHITE
        )
