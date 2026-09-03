# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_component.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 08:22:35 by nramalan        #+#    #+#               #
#  Updated: 2026/05/14 22:09:40 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import List


class MazeComponent:
    def __init__(
        self, maze: List[List[int]], x: int, y: int,
        scale: int, wall_thickness: float = 5,
        color: pr.Color = pr.Color(4, 4, 214, 255),
        logo_color: pr.Color = pr.Color(33, 208, 220, 255)
    ) -> None:
        self.maze = maze
        self.offset_x = x
        self.offset_y = y
        self.scale = scale
        self.wall_thickness = wall_thickness
        self.color = color
        self.logo_color = logo_color

    def _draw_maze_lines(self, thickness: float, color: pr.Color) -> None:
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
                        pr.Vector2(x + self.scale, y), thickness, color
                    )
                    pr.draw_circle_v(pr.Vector2(x, y), radius, color)
                    pr.draw_circle_v(
                        pr.Vector2(x + self.scale, y), radius, color
                    )
                if cell & 2:
                    pr.draw_line_ex(
                        pr.Vector2(x + self.scale, y),
                        pr.Vector2(x + self.scale, y + self.scale),
                        thickness, color
                    )
                    pr.draw_circle_v(
                        pr.Vector2(x + self.scale, y), radius, color
                    )
                    pr.draw_circle_v(
                        pr.Vector2(x + self.scale, y + self.scale),
                        radius, color
                    )
                if cell & 4:
                    pr.draw_line_ex(
                        pr.Vector2(x, y + self.scale),
                        pr.Vector2(x + self.scale, y + self.scale),
                        thickness, color
                    )
                    pr.draw_circle_v(
                        pr.Vector2(x, y + self.scale), radius, color
                    )
                    pr.draw_circle_v(
                        pr.Vector2(x + self.scale, y + self.scale),
                        radius, color
                    )
                if cell & 8:
                    pr.draw_line_ex(
                        pr.Vector2(x, y),
                        pr.Vector2(x, y + self.scale),
                        thickness, color
                    )
                    pr.draw_circle_v(pr.Vector2(x, y), radius, color)
                    pr.draw_circle_v(
                        pr.Vector2(x, y + self.scale), radius, color
                    )

    def render(self) -> None:
        self._draw_maze_lines(self.wall_thickness * 2.5, self.color)
        self._draw_maze_lines(self.wall_thickness * 1.2, pr.BLACK)
        for r in range(len(self.maze)):
            for c in range(len(self.maze[0])):
                if self.maze[r][c] == 15:
                    x = c * self.scale + self.offset_x
                    y = r * self.scale + self.offset_y
                    pr.draw_rectangle(
                        int(x + 1), int(y + 1),
                        int(self.scale - 2), int(self.scale - 2),
                        self.logo_color
                    )
