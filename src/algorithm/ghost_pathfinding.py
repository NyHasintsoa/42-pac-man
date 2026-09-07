from collections import deque
from typing import TYPE_CHECKING, List, Optional, Tuple

import pyray as pr

if TYPE_CHECKING:
    from src.graphic.component import GhostCharacter


class GhostPathfinding:
    @staticmethod
    def find_bfs_path(
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
