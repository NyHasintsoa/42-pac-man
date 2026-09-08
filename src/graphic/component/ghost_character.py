"""Render and update an autonomous ghost character."""

from typing import TYPE_CHECKING, Dict, List

import pyray as pr

from src.algorithm import GhostMovement
from src.graphic.component.character import CharacterComponent
from src.graphic.utils import ResourceManager

if TYPE_CHECKING:
    from src.graphic.component import PacmanCharacter
    from src.graphic.main_window import MainWindow


class GhostCharacter(CharacterComponent):
    """Represent an autonomous ghost with normal and frightened states."""

    def __init__(
        self,
        maze_data: List[List[int]],
        pos_x: int,
        pos_y: int,
        speed: float,
        animation_speed: float,
        window: "MainWindow",
        score: int,
        ghost_name: str = "clyde",
    ) -> None:
        """Initialize the GhostCharacter instance.

        Args:
            maze_data: The maze grid encoded with wall bit flags.
            pos_x: The horizontal position or grid coordinate.
            pos_y: The vertical position or grid coordinate.
            speed: The movement speed in pixels per frame.
            animation_speed: The interval between animation frames.
            window: The application window owning the component.
            score: The points awarded when collected.
            ghost_name: The ghost name value.

        Returns:
            The requested result.
        """
        self.ghost_name: str = ghost_name
        self.assets_path: str = ResourceManager.asset("ghost")
        self.super_timer: float = 0.0
        self.score: int = score

        self.initial_grid_pos = pr.Vector2(pos_x, pos_y)
        self.is_returning_eyes: bool = False
        self.respawn_timer: float = 0.0
        self.is_waiting_to_respawn: bool = False
        self.is_edible: bool

        super().__init__(
            maze_data=maze_data,
            pos_x=pos_x,
            pos_y=pos_y,
            speed=speed,
            animation_speed=animation_speed,
            window=window,
            margin_top=80,
            margin_bottom=30,
            padding_x=20,
        )

    def load_textures(self) -> None:
        """Load textures required by the concrete character.

        Returns:
            The requested result.
        """
        self.ghost_move_textures: Dict[int, List[pr.Texture]] = {
            0: [
                self.load_tex(f"ghost_{self.ghost_name}_d0_0.png", pr.ORANGE),
                self.load_tex(f"ghost_{self.ghost_name}_d0_1.png", pr.ORANGE),
            ],
            1: [
                self.load_tex(f"ghost_{self.ghost_name}_d1_0.png", pr.ORANGE),
                self.load_tex(f"ghost_{self.ghost_name}_d1_1.png", pr.ORANGE),
            ],
            2: [
                self.load_tex(f"ghost_{self.ghost_name}_d2_0.png", pr.ORANGE),
                self.load_tex(f"ghost_{self.ghost_name}_d2_1.png", pr.ORANGE),
            ],
            3: [
                self.load_tex(f"ghost_{self.ghost_name}_d3_0.png", pr.ORANGE),
                self.load_tex(f"ghost_{self.ghost_name}_d3_1.png", pr.ORANGE),
            ],
        }

        self.ghost_edible_textures = [
            self.load_tex("edible_blue0.png", pr.BLUE),
            self.load_tex("edible_blue1.png", pr.BLUE),
        ]

        self.ghost_flash_textures = [
            self.load_tex("edible_white0.png", pr.WHITE),
            self.load_tex("edible_white1.png", pr.WHITE),
        ]

        self.look_id = 1
        self.direction = pr.Vector2(-1, 0)
        self.next_direction = pr.Vector2(-1, 0)
        self.is_edible = False

    def on_direction_changed(self) -> None:
        """Update direction-dependent visual state.

        Returns:
            The requested result.
        """
        if self.direction.x == 1:
            self.look_id = 0
        elif self.direction.x == -1:
            self.look_id = 1
        elif self.direction.y == -1:
            self.look_id = 2
        elif self.direction.y == 1:
            self.look_id = 3

    def update(
        self,
        super_timer: float,
        pacman: "PacmanCharacter",
        blinky: "GhostCharacter",
        is_angry_blinky: bool = False,
    ) -> None:
        """Update component state from current input or timers.

        Args:
            super_timer: The remaining power-pellet duration in seconds.
            pacman: The current Pac-Man character and its position or
        direction.
            blinky: Blinky, used as a reference for Inky targeting.
            is_angry_blinky: Whether Blinky should directly chase Pac-Man.

        Returns:
            The requested result.
        """
        self.super_timer = super_timer
        if self.is_waiting_to_respawn:
            self.respawn_timer -= pr.get_frame_time()
            if self.respawn_timer <= 0.0:
                self.is_waiting_to_respawn = False
                self.is_returning_eyes = False
                self.is_edible = False
            return

        if self.is_returning_eyes:
            home_pixel = self.get_pixel_position(self.initial_grid_pos)
            if abs(self.pixel_pos.x - home_pixel.x) < (
                self.speed * 2.0
            ) and abs(self.pixel_pos.y - home_pixel.y) < (self.speed * 2.0):
                self.pixel_pos = home_pixel
                self.grid_pos = pr.Vector2(
                    self.initial_grid_pos.x, self.initial_grid_pos.y
                )
                self.is_waiting_to_respawn = True
                self.respawn_timer = 5.0
                return

        center = self.get_pixel_position(self.grid_pos)
        if (
            abs(self.pixel_pos.x - center.x) < self.speed
            and abs(self.pixel_pos.y - center.y) < self.speed
        ):
            calculated_dir = GhostMovement.get_next_direction(
                ghost=self,
                pacman=pacman,
                blinky=blinky,
                is_angry_blinky=is_angry_blinky,
            )
            self.direction = calculated_dir
            self.next_direction = calculated_dir

        saved_speed = self.speed
        if self.is_returning_eyes:
            self.speed *= 2.5

        self.update_movement_and_grid()
        self.speed = saved_speed
        self.update_animation_timer()

    def render_spawn_background(self) -> None:
        """Process the render spawn background operation.

        Returns:
            The requested result.
        """
        home_pixel = self.get_pixel_position(self.initial_grid_pos)
        hx = int(home_pixel.x)
        hy = int(home_pixel.y)
        sz = int(self.scale - 8)

        half_sz = sz // 2
        bx = hx - half_sz
        by = hy - half_sz
        thick = 2
        length = 5

        color = pr.GRAY
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

    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        if self.is_returning_eyes or self.is_waiting_to_respawn:
            hx = int(self.pixel_pos.x)
            hy = int(self.pixel_pos.y)

            pr.draw_rectangle(hx - 5, hy - 3, 4, 4, pr.WHITE)
            pr.draw_rectangle(hx + 2, hy - 3, 4, 4, pr.WHITE)

            px1, py1 = hx - 4, hy - 2
            px2, py2 = hx + 3, hy - 2
            if self.direction.x > 0:
                px1 += 1
                px2 += 1
            elif self.direction.x < 0:
                px1 -= 1
                px2 -= 1
            elif self.direction.y > 0:
                py1 += 1
                py2 += 1
            elif self.direction.y < 0:
                py1 -= 1
                py2 -= 1

            pr.draw_rectangle(px1, py1, 2, 2, pr.BLUE)
            pr.draw_rectangle(px2, py2, 2, 2, pr.BLUE)
            return

        if self.is_edible:
            if 0.0 < self.super_timer < 2.5:
                use_flash_texture = int(pr.get_time() / 0.25) % 2 == 0
                if use_flash_texture:
                    tex = self.ghost_flash_textures[
                        self.frame_index % len(self.ghost_flash_textures)
                    ]
                else:
                    tex = self.ghost_edible_textures[
                        self.frame_index % len(self.ghost_edible_textures)
                    ]
            else:
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
