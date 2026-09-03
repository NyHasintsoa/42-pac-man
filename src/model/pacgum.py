# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacgum.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 17:54:15 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 18:24:32 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from pyray import WHITE, Color, draw_circle


class Pacgum(ABC):
    def __init__(
        self, x: int, y: int, radius: int = 2, color: Color = WHITE
    ) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.collected = False

    @abstractmethod
    def render(self) -> None:
        pass

    def check_collision(self, px: int, py: int, distance: int = 15) -> bool:
        dx = self.x - px
        dy = self.y - py
        return (dx * dx + dy * dy) < (distance * distance)


class SimplePacgum(Pacgum):
    def __init__(
        self, x: int, y: int, radius: int = 2, color: Color = WHITE
    ) -> None:
        super().__init__(x, y, radius, color)

    def render(self) -> None:
        if not self.collected:
            draw_circle(self.x, self.y, self.radius, self.color)


class SuperPacgum(Pacgum):
    def __init__(
        self, x: int, y: int, radius: int = 6, color: Color = WHITE
    ) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.collected = False
        self.animation_counter = 0

    def update(self) -> None:
        self.animation_counter += 1

    def render(self) -> None:
        if not self.collected:
            pulse = 1 + 0.3 * (abs((self.animation_counter % 60) - 30) / 30)
            current_radius = int(self.radius * pulse)
            draw_circle(self.x, self.y, current_radius, self.color)
