"""Render the maze walls and logo tiles."""

from typing import TYPE_CHECKING, List

import pyray as pr

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class MazeComponent:
    """Render a maze encoded with wall bit flags."""

    def __init__(
        self,
        maze: List[List[int]],
        window: "MainWindow",
        margin_top: int = 80,
        margin_bottom: int = 30,
        padding_x: int = 20,
        color: pr.Color = pr.Color(4, 4, 214, 255),
        logo_color: pr.Color = pr.Color(33, 208, 220, 255),
    ) -> None:
        """Initialize the MazeComponent instance.

        Args:
            maze: The generated maze grid.
            window: The application window owning the component.
            margin_top: The top layout margin in pixels.
            margin_bottom: The bottom layout margin in pixels.
            padding_x: The horizontal layout padding in pixels.
            color: The drawing color.
            logo_color: The logo color value.

        Returns:
            The requested result.
        """
        self.maze = maze
        self.color = color
        self.logo_color = logo_color
        maze_rows = len(maze)
        maze_cols = len(maze[0]) if maze_rows > 0 else 1

        available_width = float(window.width - (padding_x * 2))
        available_height = float(
            window.height - margin_top - (padding_x * 2) - margin_bottom
        )

        scale_x = available_width / maze_cols
        scale_y = available_height / maze_rows
        self.scale = min(scale_x, scale_y)

        self.offset_x = (window.width - (maze_cols * self.scale)) / 2.0
        self.offset_y = (
            margin_top + (available_height - (maze_rows * self.scale)) / 2.0
        )

        self.wall_thickness = self.scale * 0.08
        if self.wall_thickness < 1.5:
            self.wall_thickness = 1.5

    def _draw_maze_lines(self, thickness: float, color: pr.Color) -> None:
        """Draw maze wall segments with the requested style.

        Args:
            thickness: The line thickness in pixels.
            color: The drawing color.

        Returns:
            The requested result.
        """
        radius = thickness / 2.0
        for r in range(len(self.maze)):
            for c in range(len(self.maze[0])):
                cell = self.maze[r][c]
                if cell == 15:
                    continue
                x = c * self.scale + self.offset_x
                y = r * self.scale + self.offset_y

                if cell & 1:
                    pr.draw_line_ex(
                        pr.Vector2(x, y),
                        pr.Vector2(x + self.scale, y),
                        thickness,
                        color,
                    )
                    pr.draw_circle_v(pr.Vector2(x, y), radius, color)
                    pr.draw_circle_v(
                        pr.Vector2(x + self.scale, y), radius, color
                    )
                if cell & 2:
                    pr.draw_line_ex(
                        pr.Vector2(x + self.scale, y),
                        pr.Vector2(x + self.scale, y + self.scale),
                        thickness,
                        color,
                    )
                    pr.draw_circle_v(
                        pr.Vector2(x + self.scale, y), radius, color
                    )
                    pr.draw_circle_v(
                        pr.Vector2(x + self.scale, y + self.scale),
                        radius,
                        color,
                    )
                if cell & 4:
                    pr.draw_line_ex(
                        pr.Vector2(x, y + self.scale),
                        pr.Vector2(x + self.scale, y + self.scale),
                        thickness,
                        color,
                    )
                    pr.draw_circle_v(
                        pr.Vector2(x, y + self.scale), radius, color
                    )
                    pr.draw_circle_v(
                        pr.Vector2(x + self.scale, y + self.scale),
                        radius,
                        color,
                    )
                if cell & 8:
                    pr.draw_line_ex(
                        pr.Vector2(x, y),
                        pr.Vector2(x, y + self.scale),
                        thickness,
                        color,
                    )
                    pr.draw_circle_v(pr.Vector2(x, y), radius, color)
                    pr.draw_circle_v(
                        pr.Vector2(x, y + self.scale), radius, color
                    )

    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        self._draw_maze_lines(self.wall_thickness * 2.5, self.color)
        self._draw_maze_lines(self.wall_thickness * 1.2, pr.BLACK)
        for r in range(len(self.maze)):
            for c in range(len(self.maze[0])):
                if self.maze[r][c] == 15:
                    x = c * self.scale + self.offset_x
                    y = r * self.scale + self.offset_y
                    pr.draw_rectangle(
                        int(x + 1),
                        int(y + 1),
                        int(self.scale - 2),
                        int(self.scale - 2),
                        self.logo_color,
                    )
