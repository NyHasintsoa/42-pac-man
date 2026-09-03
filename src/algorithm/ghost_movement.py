from collections import deque
from typing import TYPE_CHECKING, List, Optional, Tuple

import pyray as pr

if TYPE_CHECKING:
    from src.graphic.component import GhostCharacter, PacmanCharacter


class GhostMovement:
    @staticmethod
    def _find_bfs_path(
        start: Tuple[int, int],
        target: Tuple[int, int],
        maze_data: List[List[int]],
        ghost: "GhostCharacter",
    ) -> Optional[pr.Vector2]:
        if start == target:
            return None

        directions = [
            (1, 0),
            (-1, 0),
            (0, -1),
            (0, 1),
        ]

        queue = deque([[start]])
        visited = {start}

        while queue:
            path = queue.popleft()
            curr_x, curr_y = path[-1]

            if (curr_x, curr_y) == target:
                if len(path) > 1:
                    next_tile = path[1]
                    return pr.Vector2(
                        next_tile[0] - start[0], next_tile[1] - start[1]
                    )
                return None

            for dx, dy in directions:
                nx, ny = curr_x + dx, curr_y + dy
                if 0 <= ny < len(maze_data) and 0 <= nx < len(maze_data[0]):
                    if not ghost.check_wall_collision(curr_x, curr_y, dx, dy):
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            new_path = list(path)
                            new_path.append((nx, ny))
                            queue.append(new_path)
        return None

    @staticmethod
    def get_next_direction(
        ghost: "GhostCharacter",
        pacman: "PacmanCharacter",
        blinky: "GhostCharacter",
        is_angry_blinky: bool = False,
        history_limit: int = 8,
    ) -> pr.Vector2:
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

            bfs_dir = GhostMovement._find_bfs_path(
                start_tile, target_tile, ghost.maze_data, ghost
            )
            if bfs_dir is not None:
                return bfs_dir

        target_tile_v2 = GhostMovement._calculate_target(
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

    @staticmethod
    def _calculate_target(
        ghost: "GhostCharacter",
        pacman: "PacmanCharacter",
        blinky: "GhostCharacter",
        is_angry_blinky: bool,
    ) -> pr.Vector2:
        rows = len(ghost.maze_data)
        cols = len(ghost.maze_data[0]) if rows > 0 else 0

        corner_up_right = pr.Vector2(cols - 1, 0)
        corner_up_left = pr.Vector2(0, 0)
        corner_down_right = pr.Vector2(cols - 1, rows - 1)
        corner_down_left = pr.Vector2(0, rows - 1)

        is_scatter = (ghost.super_timer <= 0.0) and (
            int(pr.get_time() / 20.0) % 2 == 0
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
            dist_to_pacman = pr.vector2_distance(
                ghost.grid_pos, pacman.grid_pos
            )
            if dist_to_pacman < 8.0:
                return corner_down_left
            return pacman.grid_pos
