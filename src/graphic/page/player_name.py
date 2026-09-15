"""Collect a player name after a game finishes."""

from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.component import Button, Input, PageFrame
from src.graphic.page.parent import ParentPage
from src.graphic.utils.text_helper import centered_x
from src.model import GameContext
from src.model.enums import PageState
from src.service.score_manager import ScoreManager

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class PlayerNamePage(ParentPage):
    """Collect and save the name associated with a final score."""

    def __init__(self, window: "MainWindow") -> None:
        """Initialize the PlayerNamePage instance.

        Args:
            window: The application window owning the component.

        Returns:
            The requested result.
        """
        super().__init__(window)
        self.state = PageState.PLAYER_NAME_PAGE
        self.page_frame = PageFrame(window.width, window.height)

        box_width = 300
        box_height = 50
        box_x = (self.window.width // 2) - (box_width // 2)
        self.box_y = (self.window.height // 2) + 30

        btn_width = 160
        btn_height = 45
        btn_x = (self.window.width // 2) - (btn_width // 2)
        btn_y = self.box_y + box_height + 25

        self.name_input = Input(
            pos_x=box_x,
            pos_y=self.box_y,
            width=box_width,
            height=box_height,
            max_chars=12,
        )

        self.submit_btn = Button(
            pos_x=btn_x,
            pos_y=btn_y,
            width=btn_width,
            height=btn_height,
            text="SUBMIT",
            font_size=20,
        )

    def init(self, context: "GameContext") -> None:
        """Initialize the page with a shared game context.

        Args:
            context: The shared mutable game context.

        Returns:
            The requested result.
        """
        super().init(context)
        self.name_input.clear()

    def update(self) -> None:
        """Update component state from current input or timers.

        Returns:
            The requested result.
        """
        self.name_input.update()
        enter_pressed = pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER)
        if self.submit_btn.is_clicked or enter_pressed:
            self._handle_submit()

    def _handle_submit(self) -> None:
        """Save the entered player name and final score.

        Returns:
            The requested result.
        """
        raw_name = self.name_input.value.strip()
        display_name = raw_name if raw_name else "AAA"

        final_score = self.context.score
        final_level = self.context.current_level
        filename = self.context.config.highscore_filename

        score_manager = ScoreManager(filename)
        score_manager.add_score(display_name, final_score, final_level)

        self.context.score = 0
        self.context.current_level = 1
        self.context.time_elapsed = 0
        self.context.is_winner = False

        self.next_state = PageState.HIGH_SCORES_PAGE

    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        self.update()
        self.page_frame.render()

        if getattr(self.context, "is_winner", False):
            outcome_text = "YOU WIN!"
            outcome_color = pr.Color(46, 204, 113, 255)
        else:
            outcome_text = "GAME OVER"
            outcome_color = pr.Color(231, 76, 60, 255)

        outcome_font_size = 52
        pr.draw_text(
            outcome_text,
            centered_x(outcome_text, self.window.width / 2, outcome_font_size),
            self.box_y - 180,
            outcome_font_size,
            outcome_color,
        )

        score_text = f"FINAL SCORE: {getattr(self.context, 'score', 0)}"
        score_font_size = 24
        pr.draw_text(
            score_text,
            centered_x(score_text, self.window.width / 2, score_font_size),
            self.box_y - 120,
            score_font_size,
            pr.WHITE,
        )

        prompt_text = "ENTER PLAYER NAME"
        prompt_size = 18
        pr.draw_text(
            prompt_text,
            centered_x(prompt_text, self.window.width / 2, prompt_size),
            self.box_y - 30,
            prompt_size,
            pr.YELLOW,
        )

        self.name_input.render()
        self.submit_btn.render()
