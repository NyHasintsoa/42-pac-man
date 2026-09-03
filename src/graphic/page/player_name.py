from typing import TYPE_CHECKING

import pyray as pr

from src.graphic.component import Button, Input, PageFrame
from src.graphic.page.parent import ParentPage
from src.model import GameContext
from src.model.enums import PageState
from src.service.score_manager import ScoreManager

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class PlayerNamePage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
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

    def init(self, context: GameContext) -> None:
        super().init(context)
        self.name_input.clear()

    def update(self) -> None:
        self.name_input.update()
        enter_pressed = pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER)
        if self.submit_btn.is_clicked or enter_pressed:
            self._handle_submit()

    def _handle_submit(self) -> None:
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
        self.update()
        self.page_frame.render()

        if getattr(self.context, "is_winner", False):
            outcome_text = "YOU WIN!"
            outcome_color = pr.Color(46, 204, 113, 255)
        else:
            outcome_text = "GAME OVER"
            outcome_color = pr.Color(231, 76, 60, 255)

        outcome_font_size = 52
        outcome_width = pr.measure_text(outcome_text, outcome_font_size)
        pr.draw_text(
            outcome_text,
            (self.window.width // 2) - (outcome_width // 2),
            self.box_y - 180,
            outcome_font_size,
            outcome_color,
        )

        score_text = f"FINAL SCORE: {getattr(self.context, 'score', 0)}"
        score_font_size = 24
        score_width = pr.measure_text(score_text, score_font_size)
        pr.draw_text(
            score_text,
            (self.window.width // 2) - (score_width // 2),
            self.box_y - 120,
            score_font_size,
            pr.WHITE,
        )

        prompt_text = "ENTER PLAYER NAME"
        prompt_size = 18
        prompt_width = pr.measure_text(prompt_text, prompt_size)
        pr.draw_text(
            prompt_text,
            (self.window.width // 2) - (prompt_width // 2),
            self.box_y - 30,
            prompt_size,
            pr.YELLOW,
        )

        self.name_input.render()
        self.submit_btn.render()
