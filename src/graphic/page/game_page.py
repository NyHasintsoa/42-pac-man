# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 08:07:34 by nramalan        #+#    #+#               #
#  Updated: 2026/05/25 17:41:57 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import TYPE_CHECKING
from mazegenerator import MazeGenerator

from src.graphic.component import PacmanCharacter, GhostCharacter
from src.enums import PageState
from src.graphic.component import (
    Button, MazeComponent, PacgumManager
)
from src.graphic.page.parent_page import ParentPage

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class GamePage(ParentPage):
    def __init__(self, window: "MainWindow") -> None:
        super().__init__(window)
        self.state = PageState.GAME_PAGE
        self.score = 0
        self.lives = 3
        self.time_elapsed = 0
        self.game_running = True
        self.is_paused = False

        maze_cols, maze_rows = 20, 10

        if hasattr(self.window, "cached_maze") and self.window.cached_maze is not None:
            self.maze_data = self.window.cached_maze
        else:
            self.maze_gen = MazeGenerator(
                (maze_cols, maze_rows), False,
                (0, 0), (maze_cols - 1, maze_rows - 1)
            )
            self.maze_gen.generate()
            self.maze_data = self.maze_gen.maze

        ui_height = 160
        available_width = self.window.width * 0.95
        available_height = (self.window.height - ui_height) * 0.95
        cell_size_w = available_width // maze_cols
        cell_size_h = available_height // maze_rows
        self.scale = int(min(cell_size_w, cell_size_h))

        maze_pixel_width = maze_cols * self.scale
        maze_pixel_height = maze_rows * self.scale
        self.offset_x = (self.window.width - maze_pixel_width) // 2
        self.offset_y = (
            80 + ((self.window.height - 160) - maze_pixel_height) // 2
        )
        self.maze_view = MazeComponent(
            self.maze_data,
            x=self.offset_x,
            y=self.offset_y,
            scale=self.scale,
            wall_thickness=5.0,
            color=pr.Color(4, 4, 214, 255),
            logo_color=pr.Color(33, 208, 220, 255)
        )

        self.pacgum_manager = PacgumManager(self.scale)
        self.pacgum_manager.generate_pacgums(
            self.maze_data, self.offset_x, self.offset_y
        )

        self.pacman = PacmanCharacter(
            maze_data=self.maze_data, tile_size=self.scale,
            grid_x=1, grid_y=1, speed=2.0,
            animation_speed=0.12
        )

        self.ghost = GhostCharacter(
            maze_data=self.maze_data, tile_size=self.scale,
            grid_x=maze_cols - 2, grid_y=maze_rows - 2, speed=1.5,
            animation_speed=0.12
        )

        self.btn_back = Button(
            self.window.width - 240, 15, 220, 50, "Main Menu",
            color=pr.DARKPURPLE, hover_color=pr.VIOLET,
            clicked_color=pr.GOLD, text_color=pr.WHITE,
            font_size=20, border_radius=0.35
        )

    def check_character_collision(self) -> bool:
        collision_distance = self.scale * 0.75
        distance = pr.vector2_distance(
            self.pacman.pixel_pos, self.ghost.pixel_pos
        )
        return distance < collision_distance

    def _event_listener(self) -> None:
        if self.btn_back.is_clicked:
            self.next_state = PageState.MAIN_MENU

        # Keyboard Pause Listeners
        if pr.is_key_pressed(pr.KeyboardKey.KEY_ESCAPE):
            self.is_paused = True
        elif pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE) and self.is_paused:
            self.is_paused = False

        if not self.pacman.is_dead and not self.is_paused:
            if pr.is_key_pressed(pr.KeyboardKey.KEY_G):
                self.ghost.is_edible = not self.ghost.is_edible

            if self.check_character_collision():
                self.pacman.is_dead = True
                self.pacman.frame_index = 0

    def update(self) -> None:
        self._event_listener()

        if not self.is_paused:
            self.pacman.update()
            self.ghost.update()
            self.pacgum_manager.update(pr.get_frame_time())

            if not self.pacman.is_dead:
                screen_px = int(self.pacman.pixel_pos.x + self.offset_x)
                screen_py = int(self.pacman.pixel_pos.y + self.offset_y)
                gained_score = self.pacgum_manager.collect_pacgums(screen_px, screen_py)
                self.score += gained_score

    def render(self) -> None:
        pr.clear_background(pr.BLACK)

        # Header bar
        pr.draw_rectangle(0, 0, self.window.width, 80, pr.DARKBLUE)
        pr.draw_rectangle_lines(0, 0, self.window.width, 80, pr.GOLD)
        pr.draw_text("PAC-MAN", 20, 20, 48, pr.YELLOW)

        self.update()
        self.btn_back.render()
        self.maze_view.render()
        self.pacgum_manager.render()

        orig_pacman_pos = pr.Vector2(self.pacman.pixel_pos.x, self.pacman.pixel_pos.y)
        orig_ghost_pos = pr.Vector2(self.ghost.pixel_pos.x, self.ghost.pixel_pos.y)

        self.pacman.pixel_pos.x += self.offset_x
        self.pacman.pixel_pos.y += self.offset_y
        self.pacman.render()
        self.pacman.pixel_pos = orig_pacman_pos

        self.ghost.pixel_pos.x += self.offset_x
        self.ghost.pixel_pos.y += self.offset_y
        self.ghost.render()
        self.ghost.pixel_pos = orig_ghost_pos

        # Bottom Hud Panel
        b_y = self.window.height - 80
        pr.draw_rectangle(0, b_y, self.window.width, 80, pr.DARKBLUE)
        pr.draw_rectangle_lines(0, b_y, self.window.width, 80, pr.GOLD)
        if self.pacman.is_dead:
            pr.draw_text("GAME OVER - PACMAN KILLED", 40, b_y + 25, 24, pr.RED)
        else:
            ghost_status = "EDIBLE (Frightened)" if self.ghost.is_edible else "CHASE MODE"
            pr.draw_text(f"SCORE: {self.score}   |   GHOST: {ghost_status}", 40, b_y + 28, 20, pr.RAYWHITE)
            pr.draw_text("Press [ESC] to Pause Game", self.window.width - 320, b_y + 28, 18, pr.GOLD)

        if self.is_paused:
            pr.draw_rectangle(0, 0, self.window.width, self.window.height, pr.Color(0, 0, 0, 180))

            box_w, box_h = 450, 160
            box_x = (self.window.width - box_w) // 2
            box_y = (self.window.height - box_h) // 2

            pr.draw_rectangle_rounded(pr.Rectangle(box_x, box_y, box_w, box_h), 0.15, 4, pr.DARKBLUE)
            pr.draw_rectangle_rounded_lines(pr.Rectangle(box_x, box_y, box_w, box_h), 0.15, 4, pr.GOLD)

            pr.draw_text("GAME PAUSED", box_x + 115, box_y + 35, 32, pr.YELLOW)
            pr.draw_text("Press [SPACE] to Resume Playing", box_x + 55, box_y + 95, 20, pr.RAYWHITE)