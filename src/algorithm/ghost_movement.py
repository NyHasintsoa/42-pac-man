"""Choose movement directions for ghost characters."""

from typing import TYPE_CHECKING, List

import pyray as pr

from src.algorithm.ghost_pathfinding import GhostPathfinding
from src.algorithm.ghost_targeting import GhostTargeting

if TYPE_CHECKING:
    from src.graphic.component import GhostCharacter, PacmanCharacter


class GhostMovement:
    """Choose movement directions for a ghost based on its state and target."""

    @staticmethod
    def get_next_direction(
        ghost: "GhostCharacter",
        pacman: "PacmanCharacter",
        blinky: "GhostCharacter",
        is_angry_blinky: bool = False,
        history_limit: int = 20,
    ) -> pr.Vector2:
        """Choose the next legal direction for a ghost.

        Args:
            ghost: The ghost whose movement is being calculated.
            pacman: The current Pac-Man character and its position or
        direction.
            blinky: Blinky, used as a reference for Inky targeting.
            is_angry_blinky: Whether Blinky should directly chase Pac-Man.
            history_limit: Maximum number of recent movement tiles to retain.

        Returns:
            A legal movement vector for the ghost.
        """
        directions = [
            pr.Vector2(1, 0),
            pr.Vector2(-1, 0),
            pr.Vector2(0, -1),
            pr.Vector2(0, 1),
        ]
        valid_choices: List[pr.Vector2] = []
        for d in directions:
            if not ghost.check_wall_collision(
                int(ghost.grid_pos.x),
                int(ghost.grid_pos.y),
                int(d.x),
                int(d.y),
            ):
                if not (
                    d.x == -ghost.direction.x and d.y == -ghost.direction.y
                ):
                    valid_choices.append(d)

        if not valid_choices:
            fallback_dir = pr.Vector2(-ghost.direction.x, -ghost.direction.y)
            chosen_tile = (
                int(ghost.grid_pos.x + fallback_dir.x),
                int(ghost.grid_pos.y + fallback_dir.y),
            )
            ghost.movement_history.append(chosen_tile)
            if len(ghost.movement_history) > history_limit:
                ghost.movement_history.pop(0)
            return fallback_dir

        if ghost.is_returning_eyes:
            start_tile = (int(ghost.grid_pos.x), int(ghost.grid_pos.y))
            target_tile = (
                int(ghost.initial_grid_pos.x),
                int(ghost.initial_grid_pos.y),
            )

            bfs_dir = GhostPathfinding.find_bfs_path(
                start_tile, target_tile, ghost.maze_data, ghost
            )
            if bfs_dir is not None:
                return bfs_dir

        target_tile_v2 = GhostTargeting.calculate_target(
            ghost=ghost,
            pacman=pacman,
            blinky=blinky,
            is_angry_blinky=is_angry_blinky,
        )

        target_pixel_pos = ghost.get_pixel_position(target_tile_v2)
        best_direction: pr.Vector2 = valid_choices[0]

        extreme_score = -999999.0 if ghost.is_edible else float("inf")
        for choice in valid_choices:
            step_x = int(ghost.grid_pos.x + choice.x)
            step_y = int(ghost.grid_pos.y + choice.y)
            step_tile = (step_x, step_y)
            projected_pos = ghost.get_pixel_position(
                pr.Vector2(step_x, step_y)
            )

            if ghost.is_edible:

                simulated_dist = pr.vector2_distance(
                    projected_pos, pacman.pixel_pos
                )
                recent_visits = ghost.movement_history.count(step_tile)
                history_penalty = recent_visits * (ghost.scale * 2.0)
                score = simulated_dist - history_penalty
                if score > extreme_score:
                    extreme_score = score
                    best_direction = choice
            else:

                simulated_dist = pr.vector2_distance(
                    projected_pos, target_pixel_pos
                )
                recent_visits = ghost.movement_history.count(step_tile)
                history_penalty = recent_visits * (ghost.scale * 2.5)
                score = simulated_dist + history_penalty
                if score < extreme_score:
                    extreme_score = score
                    best_direction = choice

        chosen_tile = (
            int(ghost.grid_pos.x + best_direction.x),
            int(ghost.grid_pos.y + best_direction.y),
        )
        ghost.movement_history.append(chosen_tile)
        if len(ghost.movement_history) > history_limit:
            ghost.movement_history.pop(0)

        return best_direction
