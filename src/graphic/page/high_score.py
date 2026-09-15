"""Display and navigate saved high scores."""

import math
from typing import TYPE_CHECKING, Any, List

import pyray as pr
import time
from src.graphic.component import PageFrame
from src.graphic.page.parent import ParentPage
from src.model.enums import PageState
from src.service.score_manager import ScoreManager

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow
    from src.model import GameContext


class HighScorePage(ParentPage):
    """Display saved scores and handle score-list navigation."""

    def __init__(self, window: "MainWindow") -> None:
        """Initialize the HighScorePage instance.

        Args:
            window: The application window owning the component.

        Returns:
            The requested result.
        """
        super().__init__(window)
        self.state = PageState.HIGH_SCORES_PAGE
        self.page_frame = PageFrame(window.width, window.height)

        self.max_visible_rows = 5
        self.selected_index = 0
        self.scroll_offset = 0
        self.last_input_time = 0.0
        self.input_cooldown = 0.16

        self.color_title = pr.Color(249, 44, 114, 255)
        self.color_headers = pr.Color(27, 199, 233, 255)
        self.color_player_text = pr.Color(255, 255, 255, 255)
        self.color_player_shadow = pr.Color(0, 0, 0, 255)
        self.color_gold_text = pr.Color(255, 255, 0, 255)

        self.high_scores: List[Any] = []

    def init(self, context: "GameContext") -> None:
        """Initialize the page with a shared game context.

        Args:
            context: The shared mutable game context.

        Returns:
            The requested result.
        """
        super().init(context)
        self.refresh_scores()

    def refresh_scores(self) -> None:
        """Reload high scores and reset list navigation.

        Returns:
            The requested result.
        """
        filename = getattr(
            self.context.config, "highscore_filename", "high_scores.json"
        )
        score_manager = ScoreManager(filename)
        self.high_scores = score_manager.load_scores()
        self.selected_index = 0
        self.scroll_offset = 0

    def unload(self) -> None:
        """Release graphical resources owned by the component.

        Returns:
            The requested result.
        """
        if self._is_unloaded:
            return
        super().unload()

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
    ) -> None:
        """Draw text with a configurable offset shadow.

        Args:
            text: The text to display or process.
            x: The horizontal drawing coordinate.
            y: The vertical drawing coordinate.
            font_size: The font size in pixels.
            spacing: The spacing between rendered characters.
            text_color: The foreground text color.
            shadow_color: The shadow color.
            offset: The shadow offset in pixels.

        Returns:
            The requested result.
        """
        pr.draw_text(
            text,
            x + offset,
            y + offset,
            font_size,
            shadow_color,
        )
        pr.draw_text(text, x, y, font_size, text_color)

    def _draw_retro_trophy(
        self, x: int, y: int, scale: float, color: pr.Color
    ) -> None:
        """Draw a small trophy beside the selected score.

        Args:
            x: The horizontal drawing coordinate.
            y: The vertical drawing coordinate.
            scale: The scale value.
            color: The drawing color.

        Returns:
            The requested result.
        """
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
        """Process keyboard and mouse events for the page.

        Returns:
            The requested result.
        """
        total_time = time.perf_counter()
        total_scores = len(self.high_scores)

        if total_scores == 0:
            if pr.is_key_pressed(pr.KeyboardKey.KEY_ESCAPE):
                self.next_state = PageState.MAIN_MENU
            return

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
            self.next_state = PageState.MAIN_MENU

    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        self._event_listener()
        total_time = time.perf_counter()
        self.page_frame.render()

        scale_x = self.window.width / 800
        scale_y = self.window.height / 600
        layout_scale = min(scale_x, scale_y)

        padding_x = 100 * scale_x
        padding_y = 40 * scale_y

        spacing = 2 * layout_scale

        usable_width = self.window.width - (2 * padding_x)
        usable_height = self.window.height - (2 * padding_y)

        col_rank_x = int(padding_x + (usable_width * 0.02))
        col_name_x = int(padding_x + (usable_width * 0.16))
        col_score_x = int(padding_x + (usable_width * 0.58))
        col_stage_x = int(padding_x + (usable_width * 0.86))

        title_text = "HIGH SCORES"
        title_font_size = int(38 * layout_scale)
        title_size = pr.measure_text(title_text, title_font_size)
        title_x = (self.window.width - title_size) // 2
        title_y = padding_y + (usable_height * 0.05)

        pr.draw_text(
            title_text,
            title_x,
            int(title_y),
            title_font_size,
            self.color_title,
        )

        header_font_size = int(18 * layout_scale)
        y_start = int(title_y + title_size + (usable_height * 0.08))

        pr.draw_text(
            "RANK",
            col_rank_x,
            y_start,
            header_font_size,
            self.color_headers,
        )
        pr.draw_text(
            "NAME",
            col_name_x,
            y_start,
            header_font_size,
            self.color_headers,
        )
        pr.draw_text(
            "SCORE",
            col_score_x,
            y_start,
            header_font_size,
            self.color_headers,
        )
        pr.draw_text(
            "STAGE",
            col_stage_x,
            y_start,
            header_font_size,
            self.color_headers,
        )

        pr.draw_line(
            int(padding_x),
            int(y_start + (28 * layout_scale)),
            int(self.window.width - padding_x),
            int(y_start + (28 * layout_scale)),
            pr.Color(27, 199, 233, 60),
        )

        row_height = 48 * layout_scale
        content_start_y = y_start + (45 * layout_scale)

        if not self.high_scores:
            no_score_text = "NO HIGH SCORES YET"
            no_score_font_size = int(20 * layout_scale)
            no_score_size = pr.measure_text(no_score_text, no_score_font_size)
            no_score_x = (self.window.width - no_score_size) // 2
            no_score_y = content_start_y + (usable_height * 0.15)

            empty_pulse = int(140 + 115 * math.cos(total_time * 3.0))
            self._draw_text_with_shadow_ex(
                no_score_text,
                int(no_score_x),
                int(no_score_y),
                no_score_font_size,
                spacing,
                pr.Color(255, 255, 255, empty_pulse),
                self.color_player_shadow,
            )
        else:
            visible_subset = self.high_scores[
                self.scroll_offset : self.scroll_offset + self.max_visible_rows
            ]

            for i, entry in enumerate(visible_subset):
                actual_rank = self.scroll_offset + i + 1
                current_y = content_start_y + (i * row_height)

                rank_str = f"{actual_rank:02d}"
                name_str = str(entry.get("name", "---")).upper()
                score_str = f"{entry.get('score', 0):,}"
                level_str = f"{entry.get('level', 1):02d}"

                is_selected = (actual_rank - 1) == self.selected_index
                text_color = (
                    self.color_gold_text
                    if is_selected
                    else self.color_player_text
                )

                self._draw_text_with_shadow_ex(
                    rank_str,
                    int(col_rank_x + (10 * layout_scale)),
                    int(current_y),
                    header_font_size,
                    spacing,
                    text_color,
                    self.color_player_shadow,
                )
                self._draw_text_with_shadow_ex(
                    name_str,
                    int(col_name_x + (5 * layout_scale)),
                    int(current_y),
                    header_font_size,
                    spacing,
                    text_color,
                    self.color_player_shadow,
                )
                self._draw_text_with_shadow_ex(
                    score_str,
                    int(col_score_x),
                    int(current_y),
                    header_font_size,
                    spacing,
                    text_color,
                    self.color_player_shadow,
                )
                self._draw_text_with_shadow_ex(
                    level_str,
                    int(col_stage_x + (10 * layout_scale)),
                    int(current_y),
                    header_font_size,
                    spacing,
                    text_color,
                    self.color_player_shadow,
                )

                if is_selected:
                    trophy_x = int(
                        col_rank_x
                        - (30 * layout_scale)
                        + int(4 * math.cos(total_time * 7.0))
                    )
                    trophy_y = int(current_y + (header_font_size // 2) - 1)
                    self._draw_retro_trophy(
                        trophy_x,
                        trophy_y,
                        scale=1.1 * layout_scale,
                        color=self.color_gold_text,
                    )

        alpha_pulse = int(130 + 125 * math.cos(total_time * 4.5))
        footer_color = pr.Color(249, 44, 114, alpha_pulse)

        footer_text = "USE [UP/DOWN] TO SELECT  |  PRESS [ESC] TO EXIT"
        footer_font_size = int(12 * layout_scale)
        footer_size = pr.measure_text(footer_text, footer_font_size)
        footer_x = (self.window.width - footer_size) // 2
        footer_y = int(self.window.height - padding_y - (usable_height * 0.05))

        pr.draw_text(
            footer_text,
            footer_x,
            footer_y,
            footer_font_size,
            footer_color,
        )
