# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_generator.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/13 20:58:23 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 22:46:36 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
from typing import List, Optional, Set, Tuple

from mazegenerator import MazeGenerator

from src.model import GameConfig, MazeData, Pacgums, SimplePacgum, SuperPacgum


class LevelGenerator:
    def __init__(self, config: GameConfig) -> None:
        self.config = config

    def _generate_pacgums(
        self,
        maze: List[List[int]],
        num_pacgums: int,
        min_distance_tiles: int = 2,
    ) -> Pacgums:
        """
        Generates instances of SimplePacgum and SuperPacgum for a maze.
        PRIORITY 1: Corridor positions with strict distance spacing
        PRIORITY 2: Fill remaining target using remaining corridors
        PRIORITY 3: Force target match using completely random
                    positions if maze is too small
        Parameters:
        - maze: 2D list where 0 represents a corridor and 1 represents a wall.
        - num_pacgums: The target number of regular pacgums to place.
        - min_distance_tiles: Minimum grid distance between regular pacgums.

        Returns:
        - super_pacgums_list: A list of SuperPacgum instances.
        - simple_pacgums_list: A list of SimplePacgum instances.
        """

        rows = len(maze)
        cols = len(maze[0])

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

        corridors = [
            (r, c)
            for r in range(rows)
            for c in range(cols)
            if maze[r][c] == 0 and (r, c) not in wall_42_spots
        ]

        if not corridors:
            return [], []

        chosen_super_spots: Set[Tuple[int, int]] = set()
        corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]
        for corner in corners:

            if corner not in wall_42_spots:
                chosen_super_spots.add(corner)

        available_slots = [p for p in corridors if p not in chosen_super_spots]
        random.shuffle(available_slots)

        chosen_simple_spots: Set[Tuple[int, int]] = set()

        def is_well_separated(pos, existing_spots, dist_threshold) -> bool:
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

        super_pacgums_list = [
            SuperPacgum(c, r) for (r, c) in chosen_super_spots
        ]
        simple_pacgums_list = [
            SimplePacgum(c, r) for (r, c) in chosen_simple_spots
        ]
        return super_pacgums_list, simple_pacgums_list

    def generate_levels(self) -> Tuple[List[MazeData], List[Pacgums]]:
        levels: List[MazeData] = []
        pacgums: List[Pacgums] = []
        for _, lvl in enumerate(self.config.levels):
            print(f"level {lvl.model_dump_json()}")
            maze = self._generate_maze(lvl.width, lvl.height, lvl.seed)
            pacgums.append(self._generate_pacgums(maze, lvl.pacgum))
            levels.append(maze)
        return (levels, pacgums)

    def _generate_maze(
        self, width: int, height: int, seed: Optional[int]
    ) -> MazeData:
        gen = MazeGenerator(
            size=(width, height),
            perfect=False,
        )
        gen.generate(
            seed if seed else 42,
        )
        return gen.maze
        return gen.maze
