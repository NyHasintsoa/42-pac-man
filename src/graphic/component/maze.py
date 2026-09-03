# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 08:22:35 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 08:26:58 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
import pyray as pr

class MazeComponent:
    def __init__(self, maze_data: list[list[int]], x: int, y: int, cell_size: int, 
                 wall_width: float, color: pr.Color, logo_color: pr.Color = pr.RED):
        self.maze_data = maze_data
        self.offset_x = x
        self.offset_y = y
        self.cell_size = cell_size
        self.wall_width = wall_width
        self.color = color
        self.logo_color = logo_color # New color for the '42' path/logo

    def render(self) -> None:
        for row_idx, row in enumerate(self.maze_data):
            for col_idx, cell in enumerate(row):
                x = self.offset_x + col_idx * self.cell_size
                y = self.offset_y + row_idx * self.cell_size
                
                # 1. Determine the color for this specific cell
                # We check if the cell value has the '42' flag.
                # In your generator, cells on the path are marked with 42.
                current_draw_color = self.logo_color if cell == 42 else self.color
                
                # If the cell is a mix of walls and the path, 
                # you might use: if (cell & 42): 
                
                # 2. Draw Walls
                # NORTH Wall
                if cell & 1:
                    pr.draw_line_ex(pr.Vector2(x, y), pr.Vector2(x + self.cell_size, y), 
                                    self.wall_width, current_draw_color)
                # EAST Wall
                if cell & 2:
                    pr.draw_line_ex(pr.Vector2(x + self.cell_size, y), pr.Vector2(x + self.cell_size, y + self.cell_size), 
                                    self.wall_width, current_draw_color)
                # SOUTH Wall
                if cell & 4:
                    pr.draw_line_ex(pr.Vector2(x, y + self.cell_size), pr.Vector2(x + self.cell_size, y + self.cell_size), 
                                    self.wall_width, current_draw_color)
                # WEST Wall
                if cell & 8:
                    pr.draw_line_ex(pr.Vector2(x, y), pr.Vector2(x, y + self.cell_size), 
                                    self.wall_width, current_draw_color)

                # 3. Draw Rounded Joints
                # We use the same current_draw_color to keep the joints matching the walls
                radius = self.wall_width / 2
                pr.draw_circle(int(x), int(y), radius, current_draw_color)
                pr.draw_circle(int(x + self.cell_size), int(y), radius, current_draw_color)
                pr.draw_circle(int(x), int(y + self.cell_size), radius, current_draw_color)
                pr.draw_circle(int(x + self.cell_size), int(y + self.cell_size), radius, current_draw_color)