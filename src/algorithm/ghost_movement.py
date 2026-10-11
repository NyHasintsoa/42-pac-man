"""Choose movement directions for ghost characters."""

from typing import TYPE_CHECKING

import pyray as pr

if TYPE_CHECKING:
    from src.graphic.component import GhostCharacter


class GhostMovement:
    """Choose horizontal movement directions for ghosts."""

    @staticmethod
    def get_next_direction(ghost: "GhostCharacter") -> pr.Vector2:
        """Continue horizontally or reverse when blocked.

        Args:
            ghost: The ghost whose movement is being calculated.

        Returns:
            A horizontal movement vector for the ghost.
        """
        current = (
            pr.Vector2(1, 0)
            if ghost.direction.x > 0
            else pr.Vector2(-1, 0)
        )
        reverse = pr.Vector2(-current.x, 0)
        grid_x = int(round(ghost.grid_pos.x))
        grid_y = int(round(ghost.grid_pos.y))

        if not ghost.check_wall_collision(grid_x, grid_y, int(current.x), 0):
            return current
        if not ghost.check_wall_collision(grid_x, grid_y, int(reverse.x), 0):
            return reverse
        return current
