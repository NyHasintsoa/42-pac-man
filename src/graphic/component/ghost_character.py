# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ghost_character.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 09:00:00 by nramalan        #+#    #+#               #
#  Updated: 2026/07/10 17:26:53 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import Dict, List, TYPE_CHECKING

from src.graphic.component.character import CharacterComponent

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class GhostCharacter(CharacterComponent):
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
        self.assets_path = "assets/ghost"

        super().__init__(
            maze_data=maze_data,
            pos_x=pos_x,
            pos_y=pos_y,
            speed=speed,
            animation_speed=animation_speed,
            window=window,
            margin_top=margin_top,
            margin_bottom=margin_bottom,
            padding_x=padding_x,
        )

    def load_textures(self) -> None:
        self.ghost_move_textures: Dict[int, List[pr.Texture]] = {
            0: [
                self.load_tex("ghost0_d0_0.png", pr.ORANGE),
                self.load_tex("ghost0_d0_1.png", pr.ORANGE),
            ],
            1: [
                self.load_tex("ghost0_d1_0.png", pr.ORANGE),
                self.load_tex("ghost0_d1_1.png", pr.ORANGE),
            ],
            2: [
                self.load_tex("ghost0_d2_0.png", pr.ORANGE),
                self.load_tex("ghost0_d2_1.png", pr.ORANGE),
            ],
            3: [
                self.load_tex("ghost0_d3_0.png", pr.ORANGE),
                self.load_tex("ghost0_d3_1.png", pr.ORANGE),
            ],
        }
        self.ghost_edible_textures = [
            self.load_tex("edible_blue0.png", pr.BLUE),
            self.load_tex("edible_blue1.png", pr.BLUE),
        ]

        self.look_id = 1
        self.direction = pr.Vector2(-1, 0)
        self.next_direction = pr.Vector2(-1, 0)
        self.is_edible = False

    def on_direction_changed(self) -> None:
        if self.direction.x == 1:
            self.look_id = 0
        elif self.direction.x == -1:
            self.look_id = 1
        elif self.direction.y == -1:
            self.look_id = 2
        elif self.direction.y == 1:
            self.look_id = 3

    def update(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_G):
            self.is_edible = not self.is_edible

        center = self.get_tile_center(self.grid_pos)
        if (
            abs(self.pixel_pos.x - center.x) < self.speed
            and abs(self.pixel_pos.y - center.y) < self.speed
        ):
            if self.check_wall_collision(
                int(self.grid_pos.x),
                int(self.grid_pos.y),
                int(self.direction.x),
                int(self.direction.y),
            ):
                all_dirs = [
                    pr.Vector2(1, 0),
                    pr.Vector2(-1, 0),
                    pr.Vector2(0, -1),
                    pr.Vector2(0, 1),
                ]
                for d in all_dirs:
                    if not self.check_wall_collision(
                        int(self.grid_pos.x),
                        int(self.grid_pos.y),
                        int(d.x),
                        int(d.y),
                    ):
                        self.next_direction = d
                        break
        self.update_movement_and_grid()
        self.update_animation_timer()

    def render(self) -> None:
        if self.is_edible:
            tex = self.ghost_edible_textures[
                self.frame_index % len(self.ghost_edible_textures)
            ]
        else:
            seq = self.ghost_move_textures[self.look_id]
            tex = seq[self.frame_index % len(seq)]

        pr.draw_texture_pro(
            tex,
            pr.Rectangle(0, 0, tex.width, tex.height),
            pr.Rectangle(
                self.pixel_pos.x,
                self.pixel_pos.y,
                (self.scale - 8),
                (self.scale - 8),
            ),
            pr.Vector2((self.scale - 8) / 2.0, (self.scale - 8) / 2.0),
            0.0,
            pr.WHITE,
        )
