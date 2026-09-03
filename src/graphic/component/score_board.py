# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  score_board.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/10 15:26:50 by nramalan        #+#    #+#               #
#  Updated: 2026/07/10 20:14:46 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import TYPE_CHECKING

import pyray as pr

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class ScoreBoardComponent:
    def __init__(
        self, window: "MainWindow", high_score: int = 0, padding_x: int = 20
    ) -> None:
        self.width = window.width
        self.height = window.height
        self.padding_x = padding_x
        self.score = 0
        self.high_score = high_score
        self.lives = 3
        self.level = 1
        self.time_elapsed = 0.0

        self.life_texture = pr.load_texture("assets/pacman/pacman_lives.png")

    def update(
        self,
        current_score: int,
        current_lives: int,
        current_level: int,
        time_passed: float,
    ) -> None:
        self.score = current_score
        self.lives = current_lives
        self.level = current_level
        self.time_elapsed = time_passed

        if self.score > self.high_score:
            self.high_score = self.score

    def _draw_pacman_icon(self, cx: float, cy: float, radius: float) -> None:
        draw_x = int(cx - radius)
        draw_y = int(cy - radius)

        scale_x = (radius * 2.0) / self.life_texture.width

        pr.draw_texture_ex(
            self.life_texture,
            pr.Vector2(draw_x, draw_y),
            0.0,
            scale_x,
            pr.WHITE,
        )

    def render(self) -> None:
        score_str = f"{self.score:06d}"
        high_score_str = f"{self.high_score:06d}"

        left_base_x = 30 + self.padding_x
        right_base_x = self.width - self.padding_x

        pr.draw_text("1UP", left_base_x + 30, 12, 25, pr.RED)
        pr.draw_text(score_str, left_base_x, 40, 30, pr.WHITE)

        pr.draw_text("HIGH SCORE", (self.width // 2) - 80, 12, 25, pr.RED)
        pr.draw_text(high_score_str, (self.width // 2) - 55, 40, 30, pr.WHITE)

        lives_start_x = right_base_x - 150
        icon_y = 38
        icon_radius = 15.0

        if self.lives <= 3:
            for i in range(max(0, self.lives)):
                cx = lives_start_x + (i * 40)
                self._draw_pacman_icon(cx, icon_y, icon_radius)
        else:
            self._draw_pacman_icon(lives_start_x, icon_y, icon_radius)
            count_text = f"x {self.lives}"
            pr.draw_text(
                count_text,
                int(lives_start_x + 35),
                int(icon_y - 12),
                30,
                pr.YELLOW,
            )

        minutes = int(self.time_elapsed) // 60
        seconds = int(self.time_elapsed) % 60
        time_str = f"TIME: {minutes:02d}:{seconds:02d}"
        level_str = f"LEVEL: {self.level:02d}"

        pr.draw_text(level_str, left_base_x, self.height - 35, 30, pr.SKYBLUE)

        pr.draw_text(
            time_str, right_base_x - 200, self.height - 35, 30, pr.ORANGE
        )

    def unload(self) -> None:
        pr.unload_texture(self.life_texture)
