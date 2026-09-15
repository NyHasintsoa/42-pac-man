"""Run the active Pac-Man game page."""

from typing import TYPE_CHECKING, List

import pyray as pr

from src.graphic.component import (
    CheatComponent,
    GhostCharacter,
    MazeComponent,
    PacgumComponent,
    PacmanCharacter,
    PauseComponent,
    ScoreBoardComponent,
)
from src.graphic.page.parent import ParentPage
from src.graphic.utils import ft_vector2_distance
from src.graphic.utils.text_helper import centered_x
from src.model import GameContext, LevelConfig, MazeData
from src.model.enums import PageState
from src.service import (
    CheatingManager,
    GhostManager,
    LevelManager,
    ScoreManager,
)

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class GamePage(ParentPage):
    """Run one playable level and coordinate its components."""

    def __init__(self, window: "MainWindow") -> None:
        """Initialize the GamePage instance.

        Args:
            window: The application window owning the component.

        Returns:
            The requested result.
        """
        super().__init__(window)
        self.state = PageState.GAME_PAGE
        self.super_duration: float = 8

        self.cheat_manager = CheatingManager()
        self.level_manager = LevelManager(self.context)
        self.pause_menu = PauseComponent(self.window)
        self.cheat_menu = CheatComponent(self.window, self.cheat_manager)

        self.levels: List[LevelConfig]
        self.maze_data: MazeData
        self.ready_timer: float
        self.ghosts: List[GhostCharacter]

        self.current_level: int = 1
        self.super_timer: float = 0.0
        self.score: int = 0
        self.lives: int = 5
        self.time_elapsed: float = 0
        self.is_paused: bool = False
        self.is_cheating: bool = False

    def init(self, context: "GameContext") -> None:
        """Initialize the page with a shared game context.

        Args:
            context: The shared mutable game context.

        Returns:
            The requested result.
        """
        super().init(context)
        if self.current_level == 1:
            self.reset_runtime_state()
            self.levels = self.context.config.levels
        self.time_elapsed = self.levels[self.current_level - 1].level_max_time
        self.maze_data = self.context.maze_levels[self.current_level - 1]

        level_pacgums = self.context.pacgums[self.current_level - 1]
        for super_pacgum in level_pacgums[0]:
            super_pacgum.collected = False
        for simple_pacgum in level_pacgums[1]:
            simple_pacgum.collected = False

        self.ready_timer = 3.0
        self.is_paused = False
        self.is_cheating = False
        self.super_timer = 0.0

        self.score_board = ScoreBoardComponent(
            self.window,
            high_score=ScoreManager(
                self.context.config.highscore_filename
            ).get_high_score(),
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

        self.initial_pacman_x, self.initial_pacman_y = (
            self._find_pacman_spawn()
        )

        self.pacman = PacmanCharacter(
            self.maze_data,
            self.initial_pacman_x,
            self.initial_pacman_y,
            4.5,
            0.15,
            self.window,
        )

        self.ghost_manager = GhostManager(
            self.window, self.maze_data, self.current_level
        )
        self.ghosts = self.ghost_manager.ghosts

        self.pacgums = PacgumComponent(
            self.maze_data, self.window, level_pacgums
        )

    def _find_pacman_spawn(self) -> tuple[int, int]:
        """Return the walkable tile closest to the cente."""
        rows = len(self.maze_data)
        cols = len(self.maze_data[0]) if rows else 0
        if cols % 2 == 0:
            cols -= 1
        if not rows or not cols:
            raise ValueError("Maze data is empty")

        center_x = cols // 2
        center_y = rows // 2

        return (center_x, center_y)

    def unload(self) -> None:
        """Release graphical resources owned by the component.

        Returns:
            The requested result.
        """
        if self._is_unloaded:
            return
        if hasattr(self, "score_board"):
            self.score_board.unload()
        if hasattr(self, "pacman"):
            self.pacman.unload()
        if hasattr(self, "ghosts"):
            for ghost in self.ghosts:
                ghost.unload()
        super().unload()

    def _event_listener(self) -> None:
        """Process keyboard and mouse events for the page.

        Returns:
            The requested result.
        """
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
        """Resume play from the pause menu.

        Returns:
            The requested result.
        """
        self.is_paused = False

    def restart_game(self) -> None:
        """Reset runtime state and restart the current game.

        Returns:
            The requested result.
        """
        self.reset_runtime_state()
        self.init(self.context)

    def return_to_menu(self) -> None:
        """Reset runtime state and switch to the main menu.

        Returns:
            The requested result.
        """
        self.reset_runtime_state()
        self.next_state = PageState.MAIN_MENU

    def reset_runtime_state(self) -> None:
        """Reset score, level, timers, lives, and related context state.

        Returns:
            The requested result.
        """
        self.current_level = 1
        self.score = 0
        self.lives = self.context.lives
        self.time_elapsed = 0.0
        self.super_timer = 0.0
        self.ready_timer = 0.0
        self.is_paused = False
        self.is_cheating = False
        self.context.score = 0
        self.context.current_level = 1
        self.context.time_elapsed = 0
        self.context.is_winner = False

    def add_extra_life(self) -> None:
        """Add one life to the active game page.

        Returns:
            The requested result.
        """
        self.cheat_manager.add_extra_life(self)

    def skip_level(self) -> None:
        """Move to the next level or return to the menu after the final level.

        Returns:
            The requested result.
        """
        self.cheat_manager.skip_level(self)

    def close_cheats(self) -> None:
        """Close the cheat panel.

        Returns:
            The requested result.
        """
        self.is_cheating = False

    def finish_game(self, is_winner: bool = False) -> None:
        """Store final game state and switch to player-name entry.

        Args:
            is_winner: Whether the game ended in a win.

        Returns:
            The requested result.
        """
        self.context.score = self.score
        self.context.current_level = self.current_level
        self.context.time_elapsed = int(self.time_elapsed)
        self.context.is_winner = is_winner
        self.next_state = PageState.PLAYER_NAME_PAGE

    def check_character_collision(self) -> bool:
        """Return whether Pac-Man collides with an active ghost.

        Returns:
            True when an active ghost hits Pac-Man.
        """
        if self.cheat_manager.invincible:
            return False

        collision_distance = self.pacman.scale * 0.75
        for ghost in self.ghosts:
            if ghost.is_returning_eyes or ghost.is_waiting_to_respawn:
                continue

            distance = ft_vector2_distance(
                self.pacman.pixel_pos, ghost.pixel_pos
            )
            if distance < collision_distance:
                if ghost.is_edible:
                    self.score += ghost.score
                    self.reset_ghost_position(ghost)
                else:
                    return True
        return False

    def reset_ghost_position(self, ghost: "GhostCharacter") -> None:
        """Return a ghost to its eye-returning respawn state.

        Args:
            ghost: The ghost whose movement is being calculated.

        Returns:
            The requested result.
        """
        self.ghost_manager.reset_ghost_position(ghost)

    def reset_positions(self) -> None:
        """Reset Pac-Man and ghost positions for another life.

        Returns:
            The requested result.
        """
        self.ready_timer = 3.0
        self.pacman.is_dead = False
        self.pacman.frame_index = 0
        self.pacman.frame_timer = 0.0
        self.pacman.grid_pos = pr.Vector2(
            self.initial_pacman_x, self.initial_pacman_y
        )
        self.pacman.pixel_pos = self.pacman.get_pixel_position(
            self.pacman.grid_pos
        )
        self.pacman.direction = pr.Vector2(0, 0)
        self.pacman.next_direction = pr.Vector2(0, 0)

        for ghost in self.ghosts:
            ghost.is_returning_eyes = False
            ghost.is_waiting_to_respawn = False
            ghost.respawn_timer = 0.0
            self.reset_ghost_position(ghost)
            ghost.is_returning_eyes = False

    def render_pacman_spawn_bg(self) -> None:
        """Draw the spawn marker around Pac-Man.

        Returns:
            The requested result.
        """
        home_pixel = self.pacman.get_pixel_position(
            pr.Vector2(self.initial_pacman_x, self.initial_pacman_y)
        )
        px = int(home_pixel.x)
        py = int(home_pixel.y)
        sz = int(self.pacman.scale - 8)

        half_sz = sz // 2
        bx = px - half_sz
        by = py - half_sz
        thick = 2
        length = 5

        color = pr.GOLD
        pr.draw_rectangle(bx, by, length, thick, color)
        pr.draw_rectangle(bx, by, thick, length, color)
        pr.draw_rectangle(bx + sz - length, by, length, thick, color)
        pr.draw_rectangle(bx + sz - thick, by, thick, length, color)
        pr.draw_rectangle(bx, by + sz - thick, length, thick, color)
        pr.draw_rectangle(bx, by + sz - length, thick, length, color)
        pr.draw_rectangle(
            bx + sz - length, by + sz - thick, length, thick, color
        )
        pr.draw_rectangle(
            bx + sz - thick, by + sz - length, thick, length, color
        )

    def update(self) -> None:
        """Update component state from current input or timers.

        Returns:
            The requested result.
        """
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
                    self.finish_game(is_winner=False)
                else:
                    self.reset_positions()
            return

        if self.ready_timer > 0:
            self.ready_timer -= pr.get_frame_time()
        else:
            if self.time_elapsed > 0:
                self.time_elapsed -= pr.get_frame_time()
                if self.time_elapsed <= 0:
                    self.time_elapsed = 0.0
                    self.finish_game(is_winner=False)
                    return

            if self.super_timer > 0.0:
                self.super_timer -= pr.get_frame_time()
                if self.super_timer <= 0.0:
                    for ghost in self.ghosts:
                        if not ghost.is_returning_eyes:
                            ghost.is_edible = False

            base_speed_factor = 4.5
            speed_multiplier = 2.0 if self.cheat_manager.speed_boost else 1.0
            self.pacman.speed = base_speed_factor * speed_multiplier

            self.pacman.update()

            if not self.cheat_manager.ghost_freeze:
                self.ghost_manager.update_ghosts(
                    self.super_timer, self.pacman, self.pacgums
                )

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
                if (
                    not ghost.is_returning_eyes
                    and not ghost.is_waiting_to_respawn
                ):
                    ghost.is_edible = True

        if self.level_manager.is_level_completed(self.pacgums):
            self.level_manager.advance_level(self)

    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        self.update()

        self.score_board.render()
        self.maze_view.render()

        self.render_pacman_spawn_bg()
        for ghost in self.ghosts:
            ghost.render_spawn_background()

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
            y_pos = (self.window.height // 2) + 20
            pr.draw_text(
                ready_text,
                centered_x(ready_text, self.window.width / 2, font_size),
                y_pos,
                font_size,
                pr.Color(254, 222, 23, 255),
            )

        if self.is_paused:
            self.pause_menu.render()

        if self.is_cheating and self.window.context.config.cheating:
            self.cheat_menu.render()
