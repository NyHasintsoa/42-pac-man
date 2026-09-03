# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacman_character.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 09:00:00 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 22:03:20 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING, List

import pyray as pr

from src.graphic.component.character import CharacterComponent

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class PacmanCharacter(CharacterComponent):
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
        self.assets_path = "assets/pacman"
        self.is_dead = False
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
        self.move_textures = [
            self.load_tex("pacman_closed.png", pr.YELLOW),
            self.load_tex("pacman_move_0.png", pr.YELLOW),
            self.load_tex("pacman_move_1.png", pr.YELLOW),
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
        if pr.is_key_down(pr.KeyboardKey.KEY_RIGHT) or pr.is_key_down(
            pr.KeyboardKey.KEY_D
        ):
            self.next_direction = pr.Vector2(1, 0)
        elif pr.is_key_down(pr.KeyboardKey.KEY_LEFT) or pr.is_key_down(
            pr.KeyboardKey.KEY_A
        ):
            self.next_direction = pr.Vector2(-1, 0)
        elif pr.is_key_down(pr.KeyboardKey.KEY_UP) or pr.is_key_down(
            pr.KeyboardKey.KEY_W
        ):
            self.next_direction = pr.Vector2(0, -1)
        elif pr.is_key_down(pr.KeyboardKey.KEY_DOWN) or pr.is_key_down(
            pr.KeyboardKey.KEY_S
        ):
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
            tex,
            pr.Rectangle(0, 0, tex.width, tex.height),
            pr.Rectangle(
                self.pixel_pos.x,
                self.pixel_pos.y,
                (self.scale - 5),
                (self.scale - 5),
            ),
            pr.Vector2((self.scale - 5) / 2.0, (self.scale - 5) / 2.0),
            self.rotation,
            pr.WHITE,
        )
