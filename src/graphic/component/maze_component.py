# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_component.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 08:22:35 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 10:16:51 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import List

class MazeComponent:
    def __init__(
        self, maze_data: List[List[int]], x: int, y: int, cell_size: int,
        wall_width: float, color: pr.Color, logo_color: pr.Color = pr.BLUE
    ) -> None:
        self.maze_data = maze_data
        self.offset_x = x
        self.offset_y = y
        self.cell_size = cell_size
        self.wall_width = wall_width
        self.color = color
        self.logo_color = logo_color

    def render(self) -> None:
        for row_idx, row in enumerate(self.maze_data):
            for col_idx, cell in enumerate(row):
                x = self.offset_x + col_idx * self.cell_size
                y = self.offset_y + row_idx * self.cell_size
                
                # In your generator, '42' logo cells are exactly 15
                if cell == 15:
                    # Draw a solid filled box for the '42' logo as seen in the image
                    # We subtract 1-2 pixels to create the 'grid' look between blocks
                    pr.draw_rectangle(
                        int(x + 1), int(y + 1), 
                        self.cell_size - 2, self.cell_size - 2, 
                        self.logo_color
                    )
                else:
                    # Draw standard thin lines for the rest of the maze
                    # 1: North, 2: East, 4: South, 8: West
                    
                    if cell & 1: # North
                        pr.draw_line_ex(
                            pr.Vector2(x, y), 
                            pr.Vector2(x + self.cell_size, y), 
                            self.wall_width, self.color
                        )
                    if cell & 2: # East
                        pr.draw_line_ex(
                            pr.Vector2(x + self.cell_size, y), 
                            pr.Vector2(x + self.cell_size, y + self.cell_size), 
                            self.wall_width, self.color
                        )
                    if cell & 4: # South
                        pr.draw_line_ex(
                            pr.Vector2(x, y + self.cell_size), 
                            pr.Vector2(x + self.cell_size, y + self.cell_size), 
                            self.wall_width, self.color
                        )
                    if cell & 8: # West
                        pr.draw_line_ex(
                            pr.Vector2(x, y), 
                            pr.Vector2(x, y + self.cell_size), 
                            self.wall_width, self.color
                        )

                    # Optional: Rounded joints for the standard walls
                    radius = self.wall_width / 2
                    pr.draw_circle(int(x), int(y), radius, self.color)