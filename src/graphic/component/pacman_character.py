"""Render and update the player-controlled Pac-Man character."""

from typing import TYPE_CHECKING, List

import pyray as pr

from src.graphic.component.character import CharacterComponent

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class PacmanCharacter(CharacterComponent):
    """Represent the player-controlled Pac-Man character."""

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
        """Initialize the PacmanCharacter instance.

        Args:
            maze_data: The maze grid encoded with wall bit flags.
            pos_x: The horizontal position or grid coordinate.
            pos_y: The vertical position or grid coordinate.
            speed: The movement speed in pixels per frame.
            animation_speed: The interval between animation frames.
            window: The application window owning the component.
            margin_top: The top layout margin in pixels.
            margin_bottom: The bottom layout margin in pixels.
            padding_x: The horizontal layout padding in pixels.

        Returns:
            The requested result.
        """
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
        """Load textures required by the concrete character.

        Returns:
            The requested result.
        """
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
        """Update direction-dependent visual state.

        Returns:
            The requested result.
        """
        if self.direction.x == 1:
            self.rotation = 0.0
        elif self.direction.x == -1:
            self.rotation = 180.0
        elif self.direction.y == -1:
            self.rotation = 270.0
        elif self.direction.y == 1:
            self.rotation = 90.0

    def update(self) -> None:
        """Update component state from current input or timers.

        Returns:
            The requested result.
        """
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
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
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
