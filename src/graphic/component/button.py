# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  button.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/06 18:37:48 by nramalan        #+#    #+#               #
#  Updated: 2026/05/10 16:36:04 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr


class Button:
    def __init__(
        self, x: int, y: int, width: int, height: int, text: str = "Button",
        color: pr.Color = pr.DARKGRAY, hover_color: pr.Color = pr.DARKBLUE,
        text_color: pr.Color = pr.WHITE, font_size: int = 20
    ) -> None:
        self.rect = pr.Rectangle(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_clicked = False
        self.font_size = font_size

    def render(self) -> None:
        mouse_pos = pr.get_mouse_position()
        is_hovered = pr.check_collision_point_rec(mouse_pos, self.rect)
        current_color = self.hover_color if is_hovered else self.color
        self.is_clicked = False
        if is_hovered and pr.is_mouse_button_pressed(
            pr.MouseButton.MOUSE_BUTTON_LEFT
        ):
            self.is_clicked = True

        pr.draw_rectangle_rec(self.rect, current_color)
        pr.draw_rectangle_lines_ex(self.rect, 2, pr.GRAY)

        font_size = self.font_size
        text_width = pr.measure_text(self.text, font_size)
        tx = self.rect.x + (self.rect.width - text_width) / 2
        ty = self.rect.y + (self.rect.height - font_size) / 2
        pr.draw_text(self.text, int(tx), int(ty), font_size, self.text_color)
