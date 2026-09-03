import json
import math
import os
from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.component import PageFrame
from src.graphic.page.parent import ParentPage
from src.model.enums import PageState

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class HighScorePage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.HIGH_SCORES_PAGE
        self.page_frame = PageFrame(window.width, window.height)

        self.json_file_path = "high_scores.json"
        self.max_visible_rows = 5
        self.row_height = 48

        self.selected_index = 0
        self.scroll_offset = 0
        self.last_input_time = 0.0
        self.input_cooldown = 0.16

        self.font_path = "assets/fonts/emulogic.ttf"
        self.font = pr.load_font(self.font_path)

        self.high_scores = self._load_high_scores()

        self.color_title = pr.Color(249, 44, 114, 255)
        self.color_headers = pr.Color(27, 199, 233, 255)
        self.color_player_text = pr.Color(255, 255, 255, 255)
        self.color_player_shadow = pr.Color(0, 0, 0, 255)
        self.color_gold_text = pr.Color(255, 255, 0, 255)
        self.color_footer = pr.Color(249, 44, 114, 255)

    def _load_high_scores(self) -> list:
        scores = []
        if os.path.exists(self.json_file_path):
            try:
                with open(self.json_file_path, "r") as f:
                    scores = json.load(f)
            except Exception:
                scores = []

        if len(scores) < 12:
            extra_defaults = [
                {"name": "PAC", "score": 99990, "level": 21},
                {"name": "CRA", "score": 88880, "level": 15},
                {"name": "NRA", "score": 77770, "level": 12},
                {"name": "BKY", "score": 55550, "level": 8},
                {"name": "PNK", "score": 44440, "level": 6},
                {"name": "INK", "score": 38200, "level": 5},
                {"name": "CLY", "score": 31100, "level": 4},
                {"name": "WKA", "score": 25000, "level": 3},
                {"name": "GHO", "score": 19500, "level": 2},
                {"name": "FRT", "score": 15000, "level": 2},
                {"name": "XYZ", "score": 12000, "level": 1},
                {"name": "AAA", "score": 9000, "level": 1},
                {"name": "BBB", "score": 7500, "level": 1},
                {"name": "CCC", "score": 5000, "level": 1},
                {"name": "POO", "score": 2500, "level": 1},
            ]
            existing_names = {
                item.get("name") for item in scores if "name" in item
            }
            for d in extra_defaults:
                if d["name"] not in existing_names:
                    scores.append(d)

        scores.sort(key=lambda x: x.get("score", 0), reverse=True)
        return scores

    def _draw_text_with_shadow_ex(
        self,
        text: str,
        x: int,
        y: int,
        font_size: int,
        spacing: float,
        text_color: pr.Color,
        shadow_color: pr.Color,
        offset: int = 2,
    ):
        pr.draw_text_ex(
            self.font,
            text,
            pr.Vector2(x + offset, y + offset),
            font_size,
            spacing,
            shadow_color,
        )
        pr.draw_text_ex(
            self.font, text, pr.Vector2(x, y), font_size, spacing, text_color
        )

    def _draw_retro_trophy(
        self, x: int, y: int, scale: float, color: pr.Color
    ):
        pr.draw_rectangle(
            int(x - 10 * scale),
            int(y - 12 * scale),
            int(20 * scale),
            int(10 * scale),
            color,
        )
        pr.draw_triangle(
            pr.Vector2(x - 10 * scale, y - 2 * scale),
            pr.Vector2(x + 10 * scale, y - 2 * scale),
            pr.Vector2(x, y + 4 * scale),
            color,
        )
        pr.draw_rectangle(
            int(x - 2 * scale),
            int(y + 2 * scale),
            int(4 * scale),
            int(8 * scale),
            color,
        )
        pr.draw_rectangle(
            int(x - 8 * scale),
            int(y + 8 * scale),
            int(16 * scale),
            int(4 * scale),
            color,
        )
        pr.draw_rectangle(
            int(x - 14 * scale),
            int(y - 10 * scale),
            int(4 * scale),
            int(6 * scale),
            color,
        )
        pr.draw_rectangle(
            int(x + 10 * scale),
            int(y - 10 * scale),
            int(4 * scale),
            int(6 * scale),
            color,
        )
        pr.draw_rectangle(
            int(x - 12 * scale),
            int(y - 8 * scale),
            int(2 * scale),
            int(3 * scale),
            pr.BLACK,
        )
        pr.draw_rectangle(
            int(x + 10 * scale),
            int(y - 8 * scale),
            int(2 * scale),
            int(3 * scale),
            pr.BLACK,
        )

    def _event_listener(self) -> None:
        total_time = pr.get_time()
        total_scores = len(self.high_scores)

        if total_time - self.last_input_time > self.input_cooldown:
            if pr.is_key_down(pr.KeyboardKey.KEY_DOWN) or pr.is_key_down(
                pr.KeyboardKey.KEY_S
            ):
                if self.selected_index < total_scores - 1:
                    self.selected_index += 1
                    if (
                        self.selected_index
                        >= self.scroll_offset + self.max_visible_rows
                    ):
                        self.scroll_offset += 1
                    self.last_input_time = total_time

            elif pr.is_key_down(pr.KeyboardKey.KEY_UP) or pr.is_key_down(
                pr.KeyboardKey.KEY_W
            ):
                if self.selected_index > 0:
                    self.selected_index -= 1
                    if self.selected_index < self.scroll_offset:
                        self.scroll_offset -= 1
                    self.last_input_time = total_time

        if pr.is_key_pressed(pr.KeyboardKey.KEY_ESCAPE):
            self.next_state = PageState.INIT_MENU

    def render(self) -> None:
        self._event_listener()
        total_time = pr.get_time()
        self.page_frame.render()
        spacing = 2
        table_width = 580
        start_x = (self.window.width - table_width) // 2

        col_rank_x = start_x + 20
        col_name_x = start_x + 150
        col_score_x = start_x + 300
        col_stage_x = start_x + 470

        title_text = "HIGH SCORES"
        title_font_size = 40
        title_size_vec = pr.measure_text_ex(
            self.font, title_text, title_font_size, spacing
        )
        title_x = (self.window.width - title_size_vec.x) // 2
        pr.draw_text_ex(
            self.font,
            title_text,
            pr.Vector2(title_x, 80),
            title_font_size,
            spacing,
            self.color_title,
        )

        header_font_size = 20
        y_start = 175

        pr.draw_text_ex(
            self.font,
            "RANK",
            pr.Vector2(col_rank_x, y_start),
            header_font_size,
            spacing,
            self.color_headers,
        )
        pr.draw_text_ex(
            self.font,
            "NAME",
            pr.Vector2(col_name_x, y_start),
            header_font_size,
            spacing,
            self.color_headers,
        )
        pr.draw_text_ex(
            self.font,
            "SCORE",
            pr.Vector2(col_score_x, y_start),
            header_font_size,
            spacing,
            self.color_headers,
        )
        pr.draw_text_ex(
            self.font,
            "STAGE",
            pr.Vector2(col_stage_x, y_start),
            header_font_size,
            spacing,
            self.color_headers,
        )

        pr.draw_line(
            start_x,
            y_start + 28,
            start_x + table_width,
            y_start + 28,
            pr.Color(27, 199, 233, 60),
        )

        visible_subset = self.high_scores[
            self.scroll_offset : self.scroll_offset + self.max_visible_rows
        ]

        for i, entry in enumerate(visible_subset):
            actual_rank = self.scroll_offset + i + 1
            current_y = y_start + 45 + (i * self.row_height)

            rank_str = f"{actual_rank:02d}"
            name_str = str(entry.get("name", "---")).upper()[:3]
            score_str = f"{entry.get('score', 0):,}"
            level_str = f"L{entry.get('level', 1):02d}"

            text_color = (
                self.color_gold_text
                if actual_rank == 1
                else self.color_player_text
            )

            self._draw_text_with_shadow_ex(
                rank_str,
                col_rank_x + 10,
                current_y,
                header_font_size,
                spacing,
                text_color,
                self.color_player_shadow,
            )
            self._draw_text_with_shadow_ex(
                name_str,
                col_name_x + 5,
                current_y,
                header_font_size,
                spacing,
                text_color,
                self.color_player_shadow,
            )
            self._draw_text_with_shadow_ex(
                score_str,
                col_score_x,
                current_y,
                header_font_size,
                spacing,
                text_color,
                self.color_player_shadow,
            )
            self._draw_text_with_shadow_ex(
                level_str,
                col_stage_x + 10,
                current_y,
                header_font_size,
                spacing,
                text_color,
                self.color_player_shadow,
            )

            if (actual_rank - 1) == self.selected_index:
                trophy_x = (
                    col_rank_x - 35 + int(4 * math.cos(total_time * 7.0))
                )
                trophy_y = current_y + (header_font_size // 2) - 1
                self._draw_retro_trophy(
                    trophy_x, trophy_y, scale=1.1, color=self.color_gold_text
                )

        alpha_pulse = int(130 + 125 * math.cos(total_time * 4.5))
        footer_color = pr.Color(
            self.color_footer.r,
            self.color_footer.g,
            self.color_footer.b,
            alpha_pulse,
        )

        footer_text = "USE [UP/DOWN] TO SELECT  •  PRESS [ESC] TO EXIT"
        footer_font_size = 14
        footer_size_vec = pr.measure_text_ex(
            self.font, footer_text, footer_font_size, spacing
        )
        footer_x = (self.window.width - footer_size_vec.x) // 2
        pr.draw_text_ex(
            self.font,
            footer_text,
            pr.Vector2(footer_x, self.window.height - 85),
            footer_font_size,
            spacing,
            footer_color,
        )
