from abc import ABC
from typing import List, Tuple, TypeAlias

from pyray import WHITE, YELLOW, Color


class Pacgum(ABC):
    def __init__(
        self, x: int, y: int, score: int, color: Color = WHITE
    ) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.radius: int = 5
        self.collected = False
        self.score: int = score


class SimplePacgum(Pacgum):
    def __init__(
        self, x: int, y: int, score: int, color: Color = WHITE
    ) -> None:
        super().__init__(x, y, score, color)


class SuperPacgum(Pacgum):
    def __init__(
        self, x: int, y: int, score: int, color: Color = YELLOW
    ) -> None:
        super().__init__(x, y, score, color)
        self.radius = 8
        self.animation_counter = 0

    def update(self) -> None:
        self.animation_counter += 1


Pacgums: TypeAlias = Tuple[List[SuperPacgum], List[SimplePacgum]]
