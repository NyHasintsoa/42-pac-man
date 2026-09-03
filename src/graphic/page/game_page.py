# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_page.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 08:07:34 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 10:47:24 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr
from typing import TYPE_CHECKING
from mazegenerator import MazeGenerator

from src.enums import PageState
from src.graphic.component import (
    Button, MazeComponent, PacmanCharacter, Ghost, PelletManager
)
from src.graphic.page.parent_page import ParentPage

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class GamePage(ParentPage):
    def __init__(self, window: "MainWindow") -> None:
        super().__init__(window)
        self.state = PageState.GAME_PAGE
        self.score = 0
        self.lives = 3
        self.time_elapsed = 0
        self.game_running = True

        self.maze_gen = MazeGenerator(size=(18, 11), perfect=False)
        self.maze_gen.generate()
        self.maze_view = MazeComponent(
            self.maze_gen.maze,
            x=50,
            y=100,
            cell_size=38,
            wall_width=10.0,
            color=pr.GRAY,
            logo_color=pr.BLUE
            # color=pr.Color(160, 160, 164, 1),
            # logo_color=pr.Color(60, 91, 197, 1)
        )
        self.pacman = PacmanCharacter(
            x=360, y=300, size=28, color=pr.YELLOW
        )
        self.ghost_red = Ghost(
            x=480, y=300, size=26, color=pr.RED
        )
        self.ghost_green = Ghost(
            x=50, y=820, size=24, color=pr.LIME
        )
        self.ghost_pink = Ghost(
            x=920, y=820, size=24, color=pr.MAGENTA
        )
        self.pellet_manager = PelletManager(cell_size=38)
        self.pellet_manager.generate_pellets(
            self.maze_gen.maze, 50, 100
        )
        self.btn_back = Button(
            760, 20, 220, 50, "Main Menu",
            color=pr.DARKPURPLE, hover_color=pr.VIOLET,
            clicked_color=pr.GOLD, text_color=pr.WHITE,
            font_size=20, border_radius=0.35
        )

    def _event_listener(self) -> None:
        if self.btn_back.is_clicked:
            self.next_state = PageState.MAIN_MENU

    def render(self) -> None:
        # Dark arcade background
        pr.clear_background(pr.BLACK)

        # Top bar
        top_bar = pr.Rectangle(0, 0, 1000, 80)
        pr.draw_rectangle(int(top_bar.x), int(top_bar.y), int(top_bar.width), int(top_bar.height), pr.DARKBLUE)
        pr.draw_rectangle_lines(int(top_bar.x), int(top_bar.y), int(top_bar.width), int(top_bar.height), pr.GOLD)

        pr.draw_text("PAC-MAN", 20, 20, 48, pr.YELLOW)
        self.btn_back.render()

        # Render maze
        self.maze_view.render()

        # Render pellets
        self.pellet_manager.render()

        # Render characters
        self.pacman.render()
        self.ghost_red.render()
        self.ghost_green.render()
        self.ghost_pink.render()

        # Bottom info bar
        bottom_bar = pr.Rectangle(0, 920, 1000, 80)
        pr.draw_rectangle(int(bottom_bar.x), int(bottom_bar.y), int(bottom_bar.width), int(bottom_bar.height), pr.DARKBLUE)
        pr.draw_rectangle_lines(int(bottom_bar.x), int(bottom_bar.y), int(bottom_bar.width), int(bottom_bar.height), pr.GOLD)

        pr.draw_text(f"Score: {self.score}", 20, 935, 28, pr.YELLOW)
        pr.draw_text(f"Lives: {self.lives}", 350, 935, 28, pr.LIME)
        pr.draw_text(f"Time: {int(self.time_elapsed)}", 650, 935, 28, pr.LIGHTGRAY)

        self._event_listener()
