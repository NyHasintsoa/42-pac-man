# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 08:07:34 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 08:27:37 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import TYPE_CHECKING

from mazegenerator import MazeGenerator

from src.enums import PageState
from src.graphic.component import Button, MazeComponent
from src.graphic.page.parent_page import ParentPage

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow

class GamePage(ParentPage):
    def __init__(self, window: "MainWindow") -> None:
        super().__init__(window)
        self.state = PageState.GAME_PAGE
        
        # 1. Generate Maze Data
        # We make it slightly smaller than the screen to fit the UI
        self.maze_gen = MazeGenerator(size=(18, 11), perfect=True)
        
        # 2. Setup Maze Component
        # Arguments: data, x, y, cell_size, wall_width, color
        self.maze_view = MazeComponent(
            self.maze_gen.maze, 
            x=40, 
            y=150, 
            cell_size=40, 
            wall_width=4.0, 
            color=pr.BLUE,       # Standard walls
            logo_color=pr.WHITE  # The '42' logo/path color
        )

        self.btn_back = Button(300, 20, 200, 40, "Go to Main Menu", font_size=15)

    def _event_listener(self) -> None:
        if self.btn_back.is_clicked:
            self.next_state = PageState.MAIN_MENU

    def render(self) -> None:
        # Draw UI
        pr.draw_text("PACMAN MAZE", 40, 30, 30, pr.YELLOW)
        self.btn_back.render()
        
        # Render the Maze Component
        self.maze_view.render()
        
        self._event_listener()