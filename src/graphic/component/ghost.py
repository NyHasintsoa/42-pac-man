# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ghost.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/11 09:00:00 by nramalan        #+#    #+#               #
#  Updated: 2026/05/12 20:31:53 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr


class Ghost:
    def __init__(
        self, x: int, y: int, size: int = 30, color: pr.Color = pr.RED
    ) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.animation_counter = 0

    def update(self, delta_time: float = 0.016) -> None:
        # Animate ghost movement
        self.animation_counter += 1

    def set_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def render(self) -> None:
        # Draw ghost body (round top)
        body_height = self.size // 2
        header_height = self.size - body_height

        # Round top half
        pr.draw_circle(
            int(self.x + self.size // 2),
            int(self.y + header_height // 2),
            self.size // 2,
            self.color
        )

        # Rectangle bottom half
        pr.draw_rectangle(
            self.x,
            int(self.y + header_height // 2),
            self.size,
            body_height,
            self.color
        )

        # Draw eyes
        eye_radius = 3
        eye_y = int(self.y + header_height // 3)
        
        pr.draw_circle(
            int(self.x + self.size // 3),
            eye_y,
            eye_radius,
            pr.WHITE
        )
        pr.draw_circle(
            int(self.x + 2 * self.size // 3),
            eye_y,
            eye_radius,
            pr.WHITE
        )

        # Draw pupils
        pr.draw_circle(
            int(self.x + self.size // 3),
            eye_y,
            2,
            pr.BLACK
        )
        pr.draw_circle(
            int(self.x + 2 * self.size // 3),
            eye_y,
            2,
            pr.BLACK
        )

        # Draw wavy bottom
        wave_height = 4
        wave_width = self.size // 4
        for i in range(4):
            start_x = self.x + i * wave_width
            start_y = int(self.y + self.size - wave_height)
            pr.draw_circle(
                int(start_x + wave_width // 2),
                int(start_y + wave_height),
                wave_width // 3,
                self.color
            )
