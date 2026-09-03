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
    def __init__(self, window: "MainWindow", maze_data: MazeData) -> None:
        self.window = window
        self.maze_data = maze_data
        self.ghosts: List[GhostCharacter] = []
        self._initialize_ghosts()

    def _initialize_ghosts(self) -> None:
        rows = len(self.maze_data)
        cols = len(self.maze_data[0])
        animation_speed: float = 0.15
        speed: float = 2.2

        self.blinky = GhostCharacter(
            self.maze_data,
            cols - 2,
            1,
            speed,
            animation_speed,
            self.window,
            "blinky",
        )
        self.pinky = GhostCharacter(
            self.maze_data, 1, 1, speed, animation_speed, self.window, "pinky"
        )
        self.inky = GhostCharacter(
            self.maze_data,
            cols - 2,
            rows - 2,
            speed,
            animation_speed,
            self.window,
            "inky",
        )
        self.clyde = GhostCharacter(
            self.maze_data,
            1,
            rows - 2,
            speed,
            animation_speed,
            self.window,
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
