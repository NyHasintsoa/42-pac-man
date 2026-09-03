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
    def __init__(
        self, window: MainWindow, maze_data: MazeData, current_level: int
    ) -> None:
        self.window = window
        self.maze_data = maze_data
        self.ghosts: List[GhostCharacter] = []
        self._initialize_ghosts(current_level)

    def _initialize_ghosts(self, current_level: int) -> None:
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
        remaining_dots = sum(
            1 for p in pacgums_component.pacgums if not p.collected
        ) + sum(1 for p in pacgums_component.super_pacgums if not p.collected)

        blinky_is_angry = remaining_dots < 30

        for ghost in self.ghosts:
            ghost.super_timer = super_timer
            ghost.update(super_timer, pacman, self.blinky, blinky_is_angry)
