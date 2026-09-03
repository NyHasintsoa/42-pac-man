# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  button.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/06 18:37:48 by nramalan        #+#    #+#               #
#  Updated: 2026/05/11 08:33:33 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr


class Button:
    def __init__(
        self, x: int, y: int, width: int, height: int, text: str = "Button",
        color: pr.Color = pr.DARKBLUE, hover_color: pr.Color = pr.SKYBLUE,
        clicked_color: pr.Color = pr.GOLD, text_color: pr.Color = pr.WHITE,
        font_size: int = 24, border_radius: float = 0.35
    ) -> None:
        self.rect = pr.Rectangle(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.clicked_color = clicked_color
        self.text_color = text_color
        self.border_color = pr.LIGHTGRAY
        self.shadow_color = pr.fade(pr.BLACK, 0.35)
        self.is_clicked = False
        self.font_size = font_size
        self.border_radius = border_radius

    def render(self) -> None:
        mouse_pos = pr.get_mouse_position()
        is_hovered = pr.check_collision_point_rec(mouse_pos, self.rect)
        self.is_clicked = False
        current_color = self.hover_color if is_hovered else self.color

        if is_hovered and pr.is_mouse_button_pressed(
            pr.MouseButton.MOUSE_BUTTON_LEFT
        ):
            self.is_clicked = True
            current_color = self.clicked_color

        shadow_rect = pr.Rectangle(
            self.rect.x + 4,
            self.rect.y + 4,
            self.rect.width,
            self.rect.height,
        )
        pr.draw_rectangle_rounded(shadow_rect, self.border_radius, 12, self.shadow_color)
        pr.draw_rectangle_rounded(self.rect, self.border_radius, 12, current_color)
        pr.draw_rectangle_rounded_lines(self.rect, self.border_radius, 12, self.border_color)

        text_width = pr.measure_text(self.text, self.font_size)
        tx = self.rect.x + (self.rect.width - text_width) / 2
        ty = self.rect.y + (self.rect.height - self.font_size) / 2

        pr.draw_text(str(self.text), int(tx + 2), int(ty + 2), self.font_size, pr.BLACK)
        pr.draw_text(str(self.text), int(tx), int(ty), self.font_size, self.text_color)
