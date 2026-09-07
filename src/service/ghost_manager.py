"""Create and update the ghosts in a game level."""

from typing import TYPE_CHECKING, List

from src.graphic.component import (
    GhostCharacter,
    PacgumComponent,
    PacmanCharacter,
)
from src.model import MazeData

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class GhostManager:
    """Manage all ghosts active in a game level."""

    def __init__(
        self, window: "MainWindow", maze_data: "MazeData", current_level: int
    ) -> None:
        """Initialize the GhostManager instance.

        Args:
            window: The application window owning the component.
            maze_data: The maze grid encoded with wall bit flags.
            current_level: The one-based level currently being initialized.

        Returns:
            The requested result.
        """
        self.window = window
        self.maze_data = maze_data
        self.ghosts: List[GhostCharacter] = []
        self._initialize_ghosts(current_level)

    def _initialize_ghosts(self, current_level: int) -> None:
        """Create the four ghosts for the current level.

        Args:
            current_level: The one-based level currently being initialized.

        Returns:
            The requested result.
        """
        rows = len(self.maze_data)
        cols = len(self.maze_data[0])
        animation_speed: float = 0.15
        speed: float = 3.0
        score = self.window.context.config.levels[
            current_level - 1
        ].points_per_ghost

        self.blinky = GhostCharacter(
            self.maze_data,
            cols - 2,
            1,
            speed,
            animation_speed,
            self.window,
            score,
            "blinky",
        )
        self.pinky = GhostCharacter(
            self.maze_data,
            1,
            1,
            speed,
            animation_speed,
            self.window,
            score,
            "pinky",
        )
        self.inky = GhostCharacter(
            self.maze_data,
            cols - 2,
            rows - 2,
            speed,
            animation_speed,
            self.window,
            score,
            "inky",
        )
        self.clyde = GhostCharacter(
            self.maze_data,
            1,
            rows - 2,
            speed,
            animation_speed,
            self.window,
            score,
            "clyde",
        )

        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def reset_ghost_position(self, ghost: GhostCharacter) -> None:
        """Return a ghost to its eye-returning respawn state.

        Args:
            ghost: The ghost whose movement is being calculated.

        Returns:
            The requested result.
        """
        ghost.is_returning_eyes = True
        ghost.is_waiting_to_respawn = False
        ghost.respawn_timer = 0.0
        ghost.is_edible = False
        ghost.movement_history = []

    def update_ghosts(
        self,
        super_timer: float,
        pacman: PacmanCharacter,
        pacgums_component: PacgumComponent,
    ) -> None:
        """Update every ghost using the current power-pellet state.

        Args:
            super_timer: The remaining power-pellet duration in seconds.
            pacman: The current Pac-Man character and its position or
        direction.
            pacgums_component: The pellet component used by active ghosts.

        Returns:
            The requested result.
        """
        remaining_dots = sum(
            1 for p in pacgums_component.pacgums if not p.collected
        ) + sum(1 for p in pacgums_component.super_pacgums if not p.collected)

        blinky_is_angry = remaining_dots < 30

        for ghost in self.ghosts:
            ghost.super_timer = super_timer
            ghost.update(super_timer, pacman, self.blinky, blinky_is_angry)
