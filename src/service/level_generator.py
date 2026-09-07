"""Generate mazes and pellet placements for levels."""

import random
from typing import List, Optional, Set, Tuple

from mazegenerator import MazeGenerator

from src.model import (
    GameConfig,
    LevelConfig,
    MazeData,
    Pacgums,
    SimplePacgum,
    SuperPacgum,
)


class LevelGenerator:
    """Generate maze layouts and their pellet placements."""

    def __init__(self, config: GameConfig) -> None:
        """Initialize the LevelGenerator instance.

        Args:
            config: The validated game configuration.

        Returns:
            The requested result.
        """
        self.config = config

    def _get_wall_42_spots(self, rows: int, cols: int) -> Set[Tuple[int, int]]:
        """Return maze coordinates reserved for the 42 logo.

        Args:
            rows: The number of maze rows.
            cols: The number of maze columns.

        Returns:
            Coordinates occupied by the 42 logo.
        """
        ft_small = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]
        wall_42_spots: Set[Tuple[int, int]] = set()

        if not (len(ft_small) * 2 > rows or len(ft_small[0]) * 2 > cols):
            posy = int((rows - len(ft_small)) / 2)
            posx = int((cols - len(ft_small[0])) / 2)

            for y in range(len(ft_small)):
                for x in range(len(ft_small[0])):
                    if ft_small[y][x] == 1:
                        wall_42_spots.add((posy + y, posx + x))
        return wall_42_spots

    def _generate_super_pacgums(
        self,
        rows: int,
        cols: int,
        wall_42_spots: Set[Tuple[int, int]],
        score: int,
    ) -> List[SuperPacgum]:
        """Create power pellets at available maze corners.

        Args:
            rows: The number of maze rows.
            cols: The number of maze columns.
            wall_42_spots: Coordinates reserved for the 42 logo.
            score: The points awarded when collected.

        Returns:
            Power pellets placed at available corners.
        """
        chosen_super_spots: Set[Tuple[int, int]] = set()
        corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]

        for corner in corners:
            if corner not in wall_42_spots:
                chosen_super_spots.add(corner)
        return [SuperPacgum(c, r, score) for (r, c) in chosen_super_spots]

    def _generate_simple_pacgums(
        self,
        maze: List[List[int]],
        num_pacgums: int,
        min_distance_tiles: int,
        wall_42_spots: Set[Tuple[int, int]],
        chosen_super_spots: Set[Tuple[int, int]],
        score: int,
    ) -> List[SimplePacgum]:
        """Choose and create separated standard pellet positions.

        Args:
            maze: The generated maze grid.
            num_pacgums: The requested number of standard pellets.
            min_distance_tiles: The preferred Manhattan distance between
        pellets.
            wall_42_spots: Coordinates reserved for the 42 logo.
            chosen_super_spots: Coordinates already occupied by power pellets.
            score: The points awarded when collected.

        Returns:
            The generated standard pellets.
        """
        rows = len(maze)
        cols = len(maze[0])

        corridors = [
            (r, c)
            for r in range(rows)
            for c in range(cols)
            if maze[r][c] == 0 and (r, c) not in wall_42_spots
        ]

        if not corridors:
            return []

        available_slots = [p for p in corridors if p not in chosen_super_spots]
        random.shuffle(available_slots)

        chosen_simple_spots: Set[Tuple[int, int]] = set()

        def is_well_separated(
            pos: Tuple[int, int],
            existing_spots: Set[Tuple[int, int]],
            dist_threshold: int,
        ) -> bool:
            """Check tile spacing.

            Args:
                pos: The pos value.
                existing_spots: Coordinates already selected.
                dist_threshold: The minimum Manhattan distance.

            Returns:
                The requested result.
            """
            for ep in existing_spots:
                if abs(pos[0] - ep[0]) + abs(pos[1] - ep[1]) < dist_threshold:
                    return False
            return True

        for slot in available_slots:
            if len(chosen_simple_spots) >= num_pacgums:
                break
            if is_well_separated(
                slot, chosen_simple_spots, min_distance_tiles
            ):
                chosen_simple_spots.add(slot)

        if len(chosen_simple_spots) < num_pacgums:
            for slot in available_slots:
                if len(chosen_simple_spots) >= num_pacgums:
                    break
                if slot not in chosen_simple_spots:
                    chosen_simple_spots.add(slot)

        if len(chosen_simple_spots) < num_pacgums:
            all_possible_grid_slots = [
                (r, c)
                for r in range(rows)
                for c in range(cols)
                if (r, c) not in chosen_super_spots
                and (r, c) not in wall_42_spots
            ]
            random.shuffle(all_possible_grid_slots)

            for slot in all_possible_grid_slots:
                if len(chosen_simple_spots) >= num_pacgums:
                    break
                if slot not in chosen_simple_spots:
                    chosen_simple_spots.add(slot)
        return [SimplePacgum(c, r, score) for (r, c) in chosen_simple_spots]

    def _generate_pacgums(
        self,
        maze: List[List[int]],
        level: LevelConfig,
        min_distance_tiles: int = 3,
    ) -> Pacgums:
        """Generate both power and standard pellets for one maze.

        Args:
            maze: The generated maze grid.
            level: The level configuration supplying pellet settings.
            min_distance_tiles: The preferred Manhattan distance between
        pellets.

        Returns:
            A tuple containing power and standard pellets.
        """
        rows = len(maze)
        cols = len(maze[0])

        wall_42_spots = self._get_wall_42_spots(rows, cols)

        super_pacgums_list = self._generate_super_pacgums(
            rows, cols, wall_42_spots, level.points_per_super_pacgum
        )

        chosen_super_spots = {(p.y, p.x) for p in super_pacgums_list}

        simple_pacgums_list = self._generate_simple_pacgums(
            maze,
            level.pacgum,
            min_distance_tiles,
            wall_42_spots,
            chosen_super_spots,
            level.points_per_pacgum,
        )

        return super_pacgums_list, simple_pacgums_list

    def generate_levels(self) -> Tuple[List[MazeData], List[Pacgums]]:
        """Generate all configured mazes and their pellet collections.

        Returns:
            A tuple of maze grids and pellet collections.
        """
        levels: List[MazeData] = []
        pacgums: List[Pacgums] = []
        for _, lvl in enumerate(self.config.levels):
            print(f"level {lvl.model_dump_json()}")
            maze = self._generate_maze(lvl.width, lvl.height, lvl.seed)
            pacgums.append(self._generate_pacgums(maze, lvl))
            levels.append(maze)
        return (levels, pacgums)

    def _generate_maze(
        self, width: int, height: int, seed: Optional[int]
    ) -> MazeData:
        """Generate one maze using the requested dimensions and seed.

        Args:
            width: The width in tiles or pixels.
            height: The height in tiles or pixels.
            seed: The optional random seed.

        Returns:
            A generated maze grid.
        """
        gen = MazeGenerator(
            size=(width, height),
            perfect=False,
        )
        gen.generate(
            seed if seed else 42,
        )
        return gen.maze
