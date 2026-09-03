# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pacman.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 09:00:00 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 08:57:14 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr


class PacmanCharacter:
    def __init__(self, x: int, y: int, size: int = 30, color: pr.Color = pr.YELLOW) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.mouth_angle = 0
        self.direction = 0  # 0: right, 1: down, 2: left, 3: up

    def update(self, delta_time: float = 0.016) -> None:
        # Animate mouth opening/closing
        self.mouth_angle = (self.mouth_angle + 2) % 360

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def set_direction(self, direction: int) -> None:
        """direction: 0=right, 1=down, 2=left, 3=up"""
        self.direction = direction % 4

    def render(self) -> None:
        # Calculate mouth opening
        mouth_open = abs((self.mouth_angle % 180) - 90) / 90
        mouth_angle = 20 * mouth_open

        # Draw the main body
        start_angle = self.direction * 90 - mouth_angle
        end_angle = self.direction * 90 + mouth_angle
        sweep_angle = 360 - (end_angle - start_angle)

        pr.draw_circle_sector(
            pr.Vector2(self.x + self.size / 2, self.y + self.size / 2),
            self.size / 2,
            start_angle,
            end_angle + sweep_angle,
            16,
            self.color
        )

        # Draw eye
        eye_offset = self.size / 4
        eye_x = self.x + self.size / 2 + eye_offset * (1 if self.direction != 2 else -1)
        eye_y = self.y + self.size / 2 - eye_offset * (1 if self.direction != 1 else 0.5)
        pr.draw_circle(int(eye_x), int(eye_y), 2, pr.BLACK)
