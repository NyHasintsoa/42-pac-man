# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacgum_component.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 09:00:00 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 18:26:57 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import List

from src.model import SuperPacgum, SimplePacgum


class PacgumComponent:
    def __init__(self, scale: int = 40) -> None:
        self.pacgums: List[SimplePacgum] = []
        self.power_pacgums: List[SuperPacgum] = []
        self.scale = scale

    def add_pacgum(self, x: int, y: int) -> None:
        self.pacgums.append(SimplePacgum(x, y, radius=2, color=pr.WHITE))

    def add_power_pacgum(self, x: int, y: int) -> None:
        self.power_pacgums.append(SuperPacgum(x, y, radius=6, color=pr.WHITE))

    def generate_pacgums(
        self, maze_data: List[List[int]], offset_x: int, offset_y: int
    ) -> None:
        for row_idx, row in enumerate(maze_data):
            for col_idx, cell in enumerate(row):
                if cell != 15:
                    x = offset_x + col_idx * self.scale + \
                        self.scale // 2
                    y = offset_y + row_idx * self.scale + \
                        self.scale // 2
                    if (
                        (row_idx % 5 == 1 and col_idx % 5 == 1)
                        or (row_idx % 5 == 1 and col_idx % 5 == 4)
                        or (row_idx % 5 == 4 and col_idx % 5 == 1)
                        or (row_idx % 5 == 4 and col_idx % 5 == 4)
                    ):
                        self.add_power_pacgum(x, y)
                    else:
                        self.add_pacgum(x, y)

    def render(self) -> None:
        for simple_pacgum in self.pacgums:
            simple_pacgum.render()
        for power_pacgum in self.power_pacgums:
            power_pacgum.render()

    def update(self) -> None:
        for power_pacgum in self.power_pacgums:
            power_pacgum.update()

    def collect_pacgums(self, px: int, py: int) -> int:
        score = 0
        for simple_pacgum in self.pacgums:
            if (
                not simple_pacgum.collected
                and simple_pacgum.check_collision(px, py)
            ):
                simple_pacgum.collected = True
                score += 10
        for power_pacgum in self.power_pacgums:
            if (
                not power_pacgum.collected
                and power_pacgum.check_collision(px, py)
            ):
                power_pacgum.collected = True
                score += 50
        return score
