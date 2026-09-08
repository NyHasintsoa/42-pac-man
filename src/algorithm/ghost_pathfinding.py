"""Find paths for ghosts navigating the maze."""

from collections import deque
from typing import TYPE_CHECKING, List, Optional, Tuple

import pyray as pr

if TYPE_CHECKING:
    from src.graphic.component import GhostCharacter


class GhostPathfinding:
    """Find shortest paths through the maze for returning ghosts."""

    @staticmethod
    def find_bfs_path(
        start: Tuple[int, int],
        target: Tuple[int, int],
        maze_data: List[List[int]],
        ghost: "GhostCharacter",
    ) -> Optional[pr.Vector2]:
        """Find the first step of a breadth-first path to a target tile.

        Args:
            start: The starting maze coordinate.
            target: The destination maze coordinate.
            maze_data: The maze grid encoded with wall bit flags.
            ghost: The ghost whose movement is being calculated.

        Returns:
            The first movement vector toward the target, or None.
        """
        if start == target:
            return None

        all_directions = [
            (1, 0),
            (-1, 0),
            (0, -1),
            (0, 1),
        ]

        curr_dir = (int(ghost.direction.x), int(ghost.direction.y))
        rev_dir = (-curr_dir[0], -curr_dir[1])

        preferred_directions = []
        if curr_dir in all_directions:
            preferred_directions.append(curr_dir)
        for d in all_directions:
            if d != curr_dir and d != rev_dir:
                preferred_directions.append(d)
        if rev_dir in all_directions and rev_dir != (0, 0):
            preferred_directions.append(rev_dir)

        if not preferred_directions:
            preferred_directions = all_directions

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

            for dx, dy in preferred_directions:
                nx, ny = curr_x + dx, curr_y + dy
                if 0 <= ny < len(maze_data) and 0 <= nx < len(maze_data[0]):
                    if not ghost.check_wall_collision(curr_x, curr_y, dx, dy):
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            new_path = list(path)
                            new_path.append((nx, ny))
                            queue.append(new_path)
        return None
