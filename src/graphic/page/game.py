from typing import TYPE_CHECKING, List

import pyray as pr

from src.graphic.component import (
    GhostCharacter,
    MazeComponent,
    PacgumComponent,
    PacmanCharacter,
    ScoreBoardComponent,
)
from src.graphic.component.cheat import (
    CheatComponent,
)
from src.graphic.component.pause import PauseComponent
from src.graphic.page.parent import ParentPage
from src.model import GameContext, LevelConfig, MazeData
from src.model.enums import PageState
from src.service.cheating_manager import (
    CheatingManager,
)

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class GamePage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.GAME_PAGE
        self.score: int = 0
        self.lives: int = 5
        self.levels: List[LevelConfig]
        self.current_level: int = 1
        self.maze_data: MazeData
        self.time_elapsed: float = 0
        self.is_paused: bool = False
        self.is_cheating: bool = False
        self.ready_timer: float = 3.0
        self.cheat_manager = CheatingManager()

        self.super_timer: float = 0.0
        self.super_duration: float = 7.0

    def init(self, context: GameContext) -> None:
        super().init(context)
        self.lives = self.context.lives
        self.levels = self.context.config.levels
        self.time_elapsed = self.levels[self.current_level - 1].level_max_time
        self.maze_data = self.context.maze_levels[self.current_level - 1]
        pacgums = self.context.pacgums[self.current_level - 1]

        self.ready_timer = 3.0
        self.is_paused = False
        self.is_cheating = False
        self.super_timer = 0.0

        self.score_board = ScoreBoardComponent(
            self.window,
            high_score=120,
            padding_x=50,
        )

        self.maze_view = MazeComponent(
            self.maze_data,
            self.window,
            margin_top=80,
            margin_bottom=30,
            padding_x=20,
            color=pr.Color(4, 4, 214, 255),
            logo_color=pr.Color(33, 208, 220, 255),
        )

        center_y = round(len(self.maze_data) / 2)
        center_x = round(len(self.maze_data[0]) / 2) - 1

        self.pacman = PacmanCharacter(
            self.maze_data,
            center_x,
            center_y,
            5.0,
            0.15,
            self.window,
            80,
            30,
            20,
        )

        self.ghosts: List[GhostCharacter] = []

        self.ghosts.append(
            GhostCharacter(
                self.maze_data, 1, 1, 2.0, 0.15, self.window, 80, 30, 20
            )
        )

        self.ghosts.append(
            GhostCharacter(
                self.maze_data,
                len(self.maze_data[0]) - 2,
                1,
                2.2,
                0.15,
                self.window,
                80,
                30,
                20,
            )
        )

        self.pacgums = PacgumComponent(
            self.maze_data, self.window, pacgums, 80, 30, 20
        )
        self.pause_menu = PauseComponent(self.window)
        self.cheat_menu = CheatComponent(self.window, self.cheat_manager)

    def _event_listener(self) -> None:
        if not self.is_cheating and pr.is_key_pressed(
            pr.KeyboardKey.KEY_ESCAPE
        ):
            self.is_paused = not self.is_paused

        if (
            self.window.context.config.cheating
            and not self.is_paused
            and pr.is_key_pressed(pr.KeyboardKey.KEY_C)
        ):
            self.is_cheating = not self.is_cheating

    def resume_game(self) -> None:
        self.is_paused = False

    def restart_game(self) -> None:
        self.init(self.context)

    def return_to_menu(self) -> None:
        self.window.current_state = PageState.MAIN_MENU

    def add_extra_life(self) -> None:
        self.cheat_manager.add_extra_life(self)

    def skip_level(self) -> None:
        self.cheat_manager.skip_level(self)

    def close_cheats(self) -> None:
        self.is_cheating = False

    def check_character_collision(self) -> bool:
        if self.cheat_manager.invincible:
            return False

        collision_distance = self.pacman.scale * 0.75

        for ghost in self.ghosts:
            distance = pr.vector2_distance(
                self.pacman.pixel_pos, ghost.pixel_pos
            )
            if distance < collision_distance:
                if ghost.is_edible:

                    self.score += 200
                    self.reset_ghost_position(ghost)
                else:
                    return True
        return False

    def reset_ghost_position(self, ghost: GhostCharacter) -> None:
        ghost.grid_pos = pr.Vector2(1, 1)
        ghost.pixel_pos = ghost.get_pixel_position(ghost.grid_pos)
        ghost.direction = pr.Vector2(-1, 0)
        ghost.next_direction = pr.Vector2(-1, 0)
        ghost.is_edible = False

    def reset_positions(self) -> None:
        self.ready_timer = 3.0
        center_y = round(len(self.maze_data) / 2)
        center_x = round(len(self.maze_data[0]) / 2) - 1

        self.pacman.is_dead = False
        self.pacman.frame_index = 0
        self.pacman.frame_timer = 0.0
        self.pacman.grid_pos = pr.Vector2(center_x, center_y)
        self.pacman.pixel_pos = self.pacman.get_pixel_position(
            self.pacman.grid_pos
        )
        self.pacman.direction = pr.Vector2(0, 0)
        self.pacman.next_direction = pr.Vector2(0, 0)

        for ghost in self.ghosts:
            self.reset_ghost_position(ghost)

    def update(self) -> None:
        self._event_listener()

        if self.is_paused:
            self.pause_menu.handle_input(
                on_resume=self.resume_game,
                on_restart=self.restart_game,
                on_menu=self.return_to_menu,
            )
            return

        if self.is_cheating:
            if not self.window.context.config.cheating:
                self.is_cheating = False
            else:
                self.cheat_menu.handle_input(
                    on_add_life=self.add_extra_life,
                    on_skip_level=self.skip_level,
                    on_close=self.close_cheats,
                )
                return

        if self.pacman.is_dead:
            self.pacman.update()
            if self.pacman.frame_index >= len(self.pacman.death_textures) - 1:
                self.lives -= 1
                if self.lives <= 0:
                    self.window.current_state = PageState.MAIN_MENU
                else:
                    self.reset_positions()
            return

        if self.ready_timer > 0:
            self.ready_timer -= pr.get_frame_time()
        else:
            if self.time_elapsed > 0:
                self.time_elapsed -= pr.get_frame_time()

            if self.super_timer > 0.0:
                self.super_timer -= pr.get_frame_time()
                if self.super_timer <= 0.0:

                    for ghost in self.ghosts:
                        ghost.is_edible = False

            original_speed = 5.0
            self.pacman.speed = (
                original_speed * 2.0
                if self.cheat_manager.speed_boost
                else original_speed
            )

            self.pacman.update()

            if not self.cheat_manager.ghost_freeze:
                for ghost in self.ghosts:
                    ghost.super_timer = self.super_timer
                    ghost.update(self.super_timer)

            if self.check_character_collision():
                self.pacman.is_dead = True
                self.pacman.frame_index = 0
                self.pacman.frame_timer = 0.0

        self.score_board.update(
            self.score, self.lives, self.current_level, int(self.time_elapsed)
        )

        screen_px = int(self.pacman.pixel_pos.x)
        screen_py = int(self.pacman.pixel_pos.y)

        gained_score, super_eaten = self.pacgums.collect_pacgums(
            screen_px, screen_py
        )
        self.score += gained_score

        if super_eaten:
            self.super_timer = self.super_duration
            for ghost in self.ghosts:
                ghost.is_edible = True

    def render(self) -> None:
        pr.clear_background(pr.BLACK)

        self.update()

        self.score_board.render()
        self.maze_view.render()
        self.pacgums.render()

        if not self.pacman.is_dead:
            for ghost in self.ghosts:
                ghost.render()

        self.pacman.render()

        if (
            self.ready_timer > 0
            and not self.is_paused
            and not self.is_cheating
            and not self.pacman.is_dead
        ):
            ready_text = "READY!"
            font_size = 32
            text_width = pr.measure_text(ready_text, font_size)
            x_pos = (self.window.width // 2) - (text_width // 2)
            y_pos = (self.window.height // 2) + 20
            pr.draw_text(
                ready_text,
                x_pos,
                y_pos,
                font_size,
                pr.Color(254, 222, 23, 255),
            )

        if self.is_paused:
            self.pause_menu.render()

        if self.is_cheating and self.window.context.config.cheating:
            self.cheat_menu.render()
