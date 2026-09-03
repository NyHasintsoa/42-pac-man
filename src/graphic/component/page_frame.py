import pyray as pr


class PageFrame:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.neon_cyan = pr.Color(15, 215, 228, 255)
        self.dark_blue = pr.Color(8, 15, 28, 255)

        self.glow_far = pr.Color(15, 215, 228, 25)
        self.glow_mid = pr.Color(15, 215, 228, 60)
        self.glow_near = pr.Color(15, 215, 228, 120)

        self.pad = 48
        self.gap = 6
        self.tunnel_y = height // 2
        self.tunnel_h = 70
        self.out_pad = 18
        self.thick = 4
        self.corner_offset = 18
        self.c_len = 30

    def render(self) -> None:
        pr.clear_background(self.dark_blue)

        def draw_rounded_line(
            p1: pr.Vector2, p2: pr.Vector2, thickness: float, color: pr.Color
        ) -> None:
            pr.draw_line_ex(p1, p2, thickness, color)
            pr.draw_circle_v(p1, thickness / 2.0, color)
            pr.draw_circle_v(p2, thickness / 2.0, color)

        def draw_ribbons(thickness: float, color: pr.Color) -> None:

            draw_rounded_line(
                pr.Vector2(self.out_pad, self.out_pad),
                pr.Vector2(self.width - self.out_pad, self.out_pad),
                thickness,
                color,
            )
            draw_rounded_line(
                pr.Vector2(self.out_pad, self.out_pad),
                pr.Vector2(self.out_pad, self.pad - 12),
                thickness,
                color,
            )
            draw_rounded_line(
                pr.Vector2(self.width - self.out_pad, self.out_pad),
                pr.Vector2(self.width - self.out_pad, self.pad - 12),
                thickness,
                color,
            )

            draw_rounded_line(
                pr.Vector2(self.out_pad, self.height - self.out_pad),
                pr.Vector2(
                    self.width - self.out_pad, self.height - self.out_pad
                ),
                thickness,
                color,
            )
            draw_rounded_line(
                pr.Vector2(self.out_pad, self.height - self.out_pad),
                pr.Vector2(self.out_pad, self.height - self.pad + 12),
                thickness,
                color,
            )
            draw_rounded_line(
                pr.Vector2(
                    self.width - self.out_pad, self.height - self.out_pad
                ),
                pr.Vector2(
                    self.width - self.out_pad, self.height - self.pad + 12
                ),
                thickness,
                color,
            )

            draw_rounded_line(
                pr.Vector2(self.out_pad, self.pad + 20),
                pr.Vector2(self.pad - 15, self.pad + 20),
                thickness,
                color,
            )
            draw_rounded_line(
                pr.Vector2(self.pad - 15, self.pad + 20),
                pr.Vector2(
                    self.pad - 15, self.tunnel_y - self.tunnel_h // 2 - 15
                ),
                thickness,
                color,
            )

            draw_rounded_line(
                pr.Vector2(self.width - self.out_pad, self.pad + 20),
                pr.Vector2(self.width - self.pad + 15, self.pad + 20),
                thickness,
                color,
            )
            draw_rounded_line(
                pr.Vector2(self.width - self.pad + 15, self.pad + 20),
                pr.Vector2(
                    self.width - self.pad + 15,
                    self.tunnel_y - self.tunnel_h // 2 - 15,
                ),
                thickness,
                color,
            )

            draw_rounded_line(
                pr.Vector2(
                    self.pad - 15, self.tunnel_y + self.tunnel_h // 2 + 15
                ),
                pr.Vector2(self.pad - 15, self.height - self.pad - 20),
                thickness,
                color,
            )
            draw_rounded_line(
                pr.Vector2(self.pad - 15, self.height - self.pad - 20),
                pr.Vector2(self.out_pad, self.height - self.pad - 20),
                thickness,
                color,
            )

            draw_rounded_line(
                pr.Vector2(
                    self.width - self.pad + 15,
                    self.tunnel_y + self.tunnel_h // 2 + 15,
                ),
                pr.Vector2(
                    self.width - self.pad + 15, self.height - self.pad - 20
                ),
                thickness,
                color,
            )
            draw_rounded_line(
                pr.Vector2(
                    self.width - self.pad + 15, self.height - self.pad - 20
                ),
                pr.Vector2(
                    self.width - self.out_pad, self.height - self.pad - 20
                ),
                thickness,
                color,
            )

        draw_ribbons(self.thick + 14, self.glow_far)
        draw_ribbons(self.thick + 8, self.glow_mid)
        draw_ribbons(self.thick + 4, self.glow_near)

        draw_ribbons(self.thick, self.neon_cyan)

        pr.draw_line_ex(
            pr.Vector2(self.pad, self.pad),
            pr.Vector2(self.width - self.pad, self.pad),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(self.pad + self.gap, self.pad + self.gap),
            pr.Vector2(self.width - self.pad - self.gap, self.pad + self.gap),
            2,
            self.neon_cyan,
        )

        pr.draw_line_ex(
            pr.Vector2(self.pad, self.height - self.pad),
            pr.Vector2(self.width - self.pad, self.height - self.pad),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(self.pad + self.gap, self.height - self.pad - self.gap),
            pr.Vector2(
                self.width - self.pad - self.gap,
                self.height - self.pad - self.gap,
            ),
            2,
            self.neon_cyan,
        )

        pr.draw_line_ex(
            pr.Vector2(self.pad, self.pad),
            pr.Vector2(self.pad, self.tunnel_y - self.tunnel_h // 2),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(self.pad + self.gap, self.pad + self.gap),
            pr.Vector2(
                self.pad + self.gap, self.tunnel_y - self.tunnel_h // 2
            ),
            2,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(self.pad, self.tunnel_y + self.tunnel_h // 2),
            pr.Vector2(self.pad, self.height - self.pad),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.pad + self.gap, self.tunnel_y + self.tunnel_h // 2
            ),
            pr.Vector2(self.pad + self.gap, self.height - self.pad - self.gap),
            2,
            self.neon_cyan,
        )

        pr.draw_line_ex(
            pr.Vector2(self.width - self.pad, self.pad),
            pr.Vector2(
                self.width - self.pad, self.tunnel_y - self.tunnel_h // 2
            ),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(self.width - self.pad - self.gap, self.pad + self.gap),
            pr.Vector2(
                self.width - self.pad - self.gap,
                self.tunnel_y - self.tunnel_h // 2,
            ),
            2,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.width - self.pad, self.tunnel_y + self.tunnel_h // 2
            ),
            pr.Vector2(self.width - self.pad, self.height - self.pad),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.width - self.pad - self.gap,
                self.tunnel_y + self.tunnel_h // 2,
            ),
            pr.Vector2(
                self.width - self.pad - self.gap,
                self.height - self.pad - self.gap,
            ),
            2,
            self.neon_cyan,
        )

        pr.draw_line_ex(
            pr.Vector2(self.pad, self.tunnel_y - self.tunnel_h // 2),
            pr.Vector2(self.pad - 25, self.tunnel_y - self.tunnel_h // 2),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(self.pad, self.tunnel_y + self.tunnel_h // 2),
            pr.Vector2(self.pad - 25, self.tunnel_y + self.tunnel_h // 2),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.width - self.pad, self.tunnel_y - self.tunnel_h // 2
            ),
            pr.Vector2(
                self.width - self.pad + 25, self.tunnel_y - self.tunnel_h // 2
            ),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.width - self.pad, self.tunnel_y + self.tunnel_h // 2
            ),
            pr.Vector2(
                self.width - self.pad + 25, self.tunnel_y + self.tunnel_h // 2
            ),
            3,
            self.neon_cyan,
        )

        pr.draw_line_ex(
            pr.Vector2(
                self.pad + self.corner_offset, self.pad + self.corner_offset
            ),
            pr.Vector2(
                self.pad + self.corner_offset + self.c_len,
                self.pad + self.corner_offset,
            ),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.pad + self.corner_offset, self.pad + self.corner_offset
            ),
            pr.Vector2(
                self.pad + self.corner_offset,
                self.pad + self.corner_offset + self.c_len,
            ),
            3,
            self.neon_cyan,
        )

        pr.draw_line_ex(
            pr.Vector2(
                self.pad + self.corner_offset,
                self.height - self.pad - self.corner_offset,
            ),
            pr.Vector2(
                self.pad + self.corner_offset + self.c_len,
                self.height - self.pad - self.corner_offset,
            ),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.pad + self.corner_offset,
                self.height - self.pad - self.corner_offset,
            ),
            pr.Vector2(
                self.pad + self.corner_offset,
                self.height - self.pad - self.corner_offset - self.c_len,
            ),
            3,
            self.neon_cyan,
        )

        pr.draw_line_ex(
            pr.Vector2(
                self.width - self.pad - self.corner_offset,
                self.pad + self.corner_offset,
            ),
            pr.Vector2(
                self.width - self.pad - self.corner_offset - self.c_len,
                self.pad + self.corner_offset,
            ),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.width - self.pad - self.corner_offset,
                self.pad + self.corner_offset,
            ),
            pr.Vector2(
                self.width - self.pad - self.corner_offset,
                self.pad + self.corner_offset + self.c_len,
            ),
            3,
            self.neon_cyan,
        )

        pr.draw_line_ex(
            pr.Vector2(
                self.width - self.pad - self.corner_offset,
                self.height - self.pad - self.corner_offset,
            ),
            pr.Vector2(
                self.width - self.pad - self.corner_offset - self.c_len,
                self.height - self.pad - self.corner_offset,
            ),
            3,
            self.neon_cyan,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.width - self.pad - self.corner_offset,
                self.height - self.pad - self.corner_offset,
            ),
            pr.Vector2(
                self.width - self.pad - self.corner_offset,
                self.height - self.pad - self.corner_offset - self.c_len,
            ),
            3,
            self.neon_cyan,
        )
