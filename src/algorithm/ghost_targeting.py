"""Calculate targets for the different ghost personalities."""

from typing import TYPE_CHECKING


import pyray as pr
import time

from src.utils import ft_vector2_distance

if TYPE_CHECKING:
    from src.graphic.component import GhostCharacter, PacmanCharacter


class GhostTargeting:
    """Calculate the target tile for each ghost behavior."""

    PERIMETER_RADIUS: float = 8.0

    @staticmethod
    def calculate_target(
        ghost: "GhostCharacter",
        pacman: "PacmanCharacter",
        blinky: "GhostCharacter",
        is_angry_blinky: bool,
    ) -> pr.Vector2:
        """Calculate the tile targeted by a ghost personality.

        Args:
            ghost: The ghost whose movement is being calculated.
            pacman: The current Pac-Man character and its position or
        direction.
            blinky: Blinky, used as a reference for Inky targeting.
            is_angry_blinky: Whether Blinky should directly chase Pac-Man.

        Returns:
            The target tile as a Raylib vector.
        """
        rows = len(ghost.maze_data)
        cols = len(ghost.maze_data[0]) if rows > 0 else 0

        corner_up_right = pr.Vector2(cols - 1, 0)
        corner_up_left = pr.Vector2(0, 0)
        corner_down_right = pr.Vector2(cols - 1, rows - 1)
        corner_down_left = pr.Vector2(0, rows - 1)

        dist_to_pacman = ft_vector2_distance(ghost.grid_pos, pacman.grid_pos)
        if dist_to_pacman <= GhostTargeting.PERIMETER_RADIUS:
            return pacman.grid_pos

        is_scatter = (ghost.super_timer <= 0.0) and (
            int(time.perf_counter() / 20.0) % 2 == 0
        )

        if ghost.ghost_name == "blinky":
            if is_angry_blinky:
                return pacman.grid_pos
            return corner_up_right if is_scatter else pacman.grid_pos

        elif ghost.ghost_name == "pinky":
            if is_scatter:
                return corner_up_left
            offset_x = pacman.direction.x * 2
            offset_y = pacman.direction.y * 2
            if pacman.direction.y == -1:
                offset_x = -2
            return pr.Vector2(
                pacman.grid_pos.x + offset_x, pacman.grid_pos.y + offset_y
            )

        elif ghost.ghost_name == "inky":
            if is_scatter:
                return corner_down_right
            pac_offset_x = pacman.direction.x * 2
            pac_offset_y = pacman.direction.y * 2
            if pacman.direction.y == -1:
                pac_offset_x = -2

            pivot_x = pacman.grid_pos.x + pac_offset_x
            pivot_y = pacman.grid_pos.y + pac_offset_y
            vec_x = pivot_x - blinky.grid_pos.x
            vec_y = pivot_y - blinky.grid_pos.y
            return pr.Vector2(
                blinky.grid_pos.x + (vec_x * 2),
                blinky.grid_pos.y + (vec_y * 2),
            )

        else:
            if is_scatter:
                return corner_down_left
            return pacman.grid_pos
