# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacgum.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 17:54:15 by nramalan        #+#    #+#               #
#  Updated: 2026/07/10 20:08:37 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC

from pyray import WHITE, YELLOW, Color


class Pacgum(ABC):
    def __init__(self, x: int, y: int, color: Color = WHITE) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.radius: int = 5
        self.collected = False

    def check_collision(self, px: int, py: int, distance: int = 15) -> bool:
        dx = self.x - px
        dy = self.y - py
        return (dx * dx + dy * dy) < (distance * distance)


class SimplePacgum(Pacgum):
    def __init__(self, x: int, y: int, color: Color = WHITE) -> None:
        super().__init__(x, y, color)


class SuperPacgum(Pacgum):
    def __init__(self, x: int, y: int, color: Color = YELLOW) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.radius: int = 8
        self.collected = False
        self.animation_counter = 0

    def update(self) -> None:
        self.animation_counter += 1
