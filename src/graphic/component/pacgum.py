import math
from typing import TYPE_CHECKING, List, Tuple

import pyray as pr

from src.model import Pacgums, SimplePacgum, SuperPacgum

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class PacgumComponent:
    def __init__(
        self,
        maze_data: List[List[int]],
        window: "MainWindow",
        pacgums: "Pacgums",
    ) -> None:
        margin_top: int = 80
        margin_bottom: int = 30
        padding_x: int = 20

        self.pacgums: List[SimplePacgum] = pacgums[1]
        self.super_pacgums: List[SuperPacgum] = pacgums[0]

        self.grid_cols = len(maze_data[0]) if maze_data else 0
        self.grid_rows = len(maze_data) if maze_data else 0

        available_width = float(window.width - (padding_x * 2))
        available_height = float(
            window.height - margin_top - (padding_x * 2) - margin_bottom
        )
        scale_x = (
            available_width / self.grid_cols if self.grid_cols > 0 else 1.0
        )
        scale_y = (
            available_height / self.grid_rows if self.grid_rows > 0 else 1.0
        )
        self.scale = min(scale_x, scale_y)

        self.offset_x = (window.width - (self.grid_cols * self.scale)) / 2.0
        self.offset_y = (
            margin_top
            + (available_height - (self.grid_rows * self.scale)) / 2.0
        )

    def get_pixel_position(self, grid_x: int, grid_y: int) -> pr.Vector2:
        return pr.Vector2(
            grid_x * self.scale + self.offset_x + (self.scale / 2.0),
            grid_y * self.scale + self.offset_y + (self.scale / 2.0),
        )

    def render(self) -> None:
        simple_radius = self.scale * 0.1
        base_super_radius = self.scale * 0.18

        bounce_factor = 1.0 + 0.08 * math.sin(pr.get_time() * 8.0)
        animated_super_radius = base_super_radius * bounce_factor

        for simple_pacgum in self.pacgums:
            if not simple_pacgum.collected:
                pos = self.get_pixel_position(simple_pacgum.x, simple_pacgum.y)
                pr.draw_circle_v(pos, simple_radius, simple_pacgum.color)

        for power_pacgum in self.super_pacgums:
            if not power_pacgum.collected:
                pos = self.get_pixel_position(power_pacgum.x, power_pacgum.y)
                pr.draw_circle_v(
                    pos, animated_super_radius, power_pacgum.color
                )

    def update(self) -> None:
        for power_pacgum in self.super_pacgums:
            power_pacgum.update()

    def collect_pacgums(self, px: int, py: int) -> Tuple[int, bool]:
        score = 0
        super_collected = False
        collection_threshold = self.scale * 0.45
        threshold_sq = collection_threshold * collection_threshold

        for simple_pacgum in self.pacgums:
            if not simple_pacgum.collected:
                pos = self.get_pixel_position(simple_pacgum.x, simple_pacgum.y)
                dx = pos.x - px
                dy = pos.y - py
                if (dx * dx + dy * dy) < threshold_sq:
                    simple_pacgum.collected = True
                    score += simple_pacgum.score

        for power_pacgum in self.super_pacgums:
            if not power_pacgum.collected:
                pos = self.get_pixel_position(power_pacgum.x, power_pacgum.y)
                dx = pos.x - px
                dy = pos.y - py
                if (dx * dx + dy * dy) < threshold_sq:
                    power_pacgum.collected = True
                    score += power_pacgum.score
                    super_collected = True

        return score, super_collected
