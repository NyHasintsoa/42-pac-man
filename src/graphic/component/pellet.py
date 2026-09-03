# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pellet.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 09:00:00 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 08:57:14 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import List


class Pellet:
    """Small dot pellet for the maze"""
    def __init__(self, x: int, y: int, radius: int = 2, color: pr.Color = pr.WHITE) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.collected = False

    def render(self) -> None:
        if not self.collected:
            pr.draw_circle(self.x, self.y, self.radius, self.color)

    def check_collision(self, px: int, py: int, distance: int = 15) -> bool:
        """Check if Pacman collided with this pellet"""
        dx = self.x - px
        dy = self.y - py
        return (dx * dx + dy * dy) < (distance * distance)


class PowerPellet:
    """Large power-up pellet"""
    def __init__(self, x: int, y: int, radius: int = 6, color: pr.Color = pr.WHITE) -> None:
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
            # Pulsing animation
            pulse = 1 + 0.3 * (abs((self.animation_counter % 60) - 30) / 30)
            current_radius = int(self.radius * pulse)
            pr.draw_circle(self.x, self.y, current_radius, self.color)

    def check_collision(self, px: int, py: int, distance: int = 20) -> bool:
        """Check if Pacman collided with this power pellet"""
        dx = self.x - px
        dy = self.y - py
        return (dx * dx + dy * dy) < (distance * distance)


class PelletManager:
    """Manages all pellets in the maze"""
    def __init__(self, cell_size: int = 40) -> None:
        self.pellets: List[Pellet] = []
        self.power_pellets: List[PowerPellet] = []
        self.cell_size = cell_size

    def add_pellet(self, x: int, y: int) -> None:
        self.pellets.append(Pellet(x, y, radius=2, color=pr.WHITE))

    def add_power_pellet(self, x: int, y: int) -> None:
        self.power_pellets.append(PowerPellet(x, y, radius=6, color=pr.WHITE))

    def generate_pellets(self, maze_data: List[List[int]], offset_x: int, offset_y: int) -> None:
        """Generate pellets for all empty spaces in the maze"""
        for row_idx, row in enumerate(maze_data):
            for col_idx, cell in enumerate(row):
                if cell != 15:  # Not a collectible area
                    x = offset_x + col_idx * self.cell_size + self.cell_size // 2
                    y = offset_y + row_idx * self.cell_size + self.cell_size // 2
                    
                    # Add power pellets in corners, regular pellets elsewhere
                    if (row_idx % 5 == 1 and col_idx % 5 == 1) or \
                       (row_idx % 5 == 1 and col_idx % 5 == 4) or \
                       (row_idx % 5 == 4 and col_idx % 5 == 1) or \
                       (row_idx % 5 == 4 and col_idx % 5 == 4):
                        self.add_power_pellet(x, y)
                    else:
                        self.add_pellet(x, y)

    def render(self) -> None:
        for pellet in self.pellets:
            pellet.render()
        for power_pellet in self.power_pellets:
            power_pellet.render()

    def update(self, delta_time: float = 0.016) -> None:
        for power_pellet in self.power_pellets:
            power_pellet.update(delta_time)

    def collect_pellets(self, px: int, py: int) -> int:
        """Collect pellets at Pacman position, return score"""
        score = 0
        for pellet in self.pellets:
            if not pellet.collected and pellet.check_collision(px, py):
                pellet.collected = True
                score += 10
        for power_pellet in self.power_pellets:
            if not power_pellet.collected and power_pellet.check_collision(px, py):
                power_pellet.collected = True
                score += 50
        return score
