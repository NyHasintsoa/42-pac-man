# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacgum.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 09:00:00 by nramalan        #+#    #+#               #
#  Updated: 2026/05/15 20:40:18 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import List


class Pacgum:
    def __init__(
        self, x: int, y: int, radius: int = 2, color: pr.Color = pr.WHITE
    ) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.collected = False

    def render(self) -> None:
        if not self.collected:
            pr.draw_circle(self.x, self.y, self.radius, self.color)

    def check_collision(self, px: int, py: int, distance: int = 15) -> bool:
        dx = self.x - px
        dy = self.y - py
        return (dx * dx + dy * dy) < (distance * distance)


class SuperPacgum:
    def __init__(
        self, x: int, y: int, radius: int = 6, color: pr.Color = pr.WHITE
    ) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.collected = False
        self.animation_counter = 0

    def update(self, delta_time: float = 0.016) -> None:
        self.animation_counter += 1

    def render(self) -> None:
        if not self.collected:
            pulse = 1 + 0.3 * (abs((self.animation_counter % 60) - 30) / 30)
            current_radius = int(self.radius * pulse)
            pr.draw_circle(self.x, self.y, current_radius, self.color)

    def check_collision(self, px: int, py: int, distance: int = 20) -> bool:
        dx = self.x - px
        dy = self.y - py
        return (dx * dx + dy * dy) < (distance * distance)


class PacgumManager:
    def __init__(self, scale: int = 40) -> None:
        self.pacgums: List[Pacgum] = []
        self.power_pacgums: List[SuperPacgum] = []
        self.scale = scale

    def add_Pacgum(self, x: int, y: int) -> None:
        self.pacgums.append(Pacgum(x, y, radius=2, color=pr.WHITE))

    def add_power_Pacgum(self, x: int, y: int) -> None:
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
                        self.add_power_Pacgum(x, y)
                    else:
                        self.add_Pacgum(x, y)

    def render(self) -> None:
        for Pacgum in self.pacgums:
            Pacgum.render()
        for power_Pacgum in self.power_pacgums:
            power_Pacgum.render()

    def update(self, delta_time: float = 0.016) -> None:
        for power_Pacgum in self.power_pacgums:
            power_Pacgum.update(delta_time)

    def collect_pacgums(self, px: int, py: int) -> int:
        score = 0
        for Pacgum in self.pacgums:
            if not Pacgum.collected and Pacgum.check_collision(px, py):
                Pacgum.collected = True
                score += 10
        for power_Pacgum in self.power_pacgums:
            if (
                not power_Pacgum.collected
                and power_Pacgum.check_collision(px, py)
            ):
                power_Pacgum.collected = True
                score += 50
        return score
