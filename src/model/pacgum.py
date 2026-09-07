"""Define collectible pellet objects."""

from abc import ABC
from typing import List, Tuple, TypeAlias

from pyray import WHITE, YELLOW, Color


class Pacgum(ABC):
    """Represent a collectible pellet and its visual properties."""

    def __init__(
        self, x: int, y: int, score: int, color: Color = WHITE
    ) -> None:
        """Initialize the Pacgum instance.

        Args:
            x: The horizontal drawing coordinate.
            y: The vertical drawing coordinate.
            score: The points awarded when collected.
            color: The drawing color.

        Returns:
            The requested result.
        """
        self.x = x
        self.y = y
        self.color = color
        self.radius: int = 5
        self.collected = False
        self.score: int = score


class SimplePacgum(Pacgum):
    """Represent a standard collectible pellet."""

    def __init__(
        self, x: int, y: int, score: int, color: Color = WHITE
    ) -> None:
        """Initialize the SimplePacgum instance.

        Args:
            x: The horizontal drawing coordinate.
            y: The vertical drawing coordinate.
            score: The points awarded when collected.
            color: The drawing color.

        Returns:
            The requested result.
        """
        super().__init__(x, y, score, color)


class SuperPacgum(Pacgum):
    """Represent a collectible power pellet with animation state."""

    def __init__(
        self, x: int, y: int, score: int, color: Color = YELLOW
    ) -> None:
        """Initialize the SuperPacgum instance.

        Args:
            x: The horizontal drawing coordinate.
            y: The vertical drawing coordinate.
            score: The points awarded when collected.
            color: The drawing color.

        Returns:
            The requested result.
        """
        super().__init__(x, y, score, color)
        self.radius = 8
        self.animation_counter = 0

    def update(self) -> None:
        """Update component state from current input or timers.

        Returns:
            The requested result.
        """
        self.animation_counter += 1


Pacgums: TypeAlias = Tuple[List[SuperPacgum], List[SimplePacgum]]
