from typing import TYPE_CHECKING

from src.model.enums import PageState

if TYPE_CHECKING:
    from src.graphic.component import PacgumComponent
    from src.graphic.page import GamePage
    from src.model import GameContext


class LevelManager:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def count_remaining_pacgums(
        self, pacgum_component: PacgumComponent
    ) -> int:
        remaining = 0
        for pacgum in getattr(pacgum_component, "pacgums", []):
            if not pacgum.collected:
                remaining += 1

        for pacgum in getattr(pacgum_component, "super_pacgums", []):
            if not pacgum.collected:
                remaining += 1

        return remaining

    def is_level_completed(self, pacgum_component: PacgumComponent) -> bool:
        return self.count_remaining_pacgums(pacgum_component) == 0

    def advance_level(self, game_page: GamePage) -> bool:
        if not self.is_level_completed(game_page.pacgums):
            return False

        if game_page.current_level < len(game_page.levels):
            game_page.current_level += 1
            self.context.current_level = game_page.current_level
            game_page.init(self.context)
            return True

        self.context.score = game_page.score
        self.context.is_winner = True

        game_page.next_state = PageState.PLAYER_NAME_PAGE
        self.context.current_level = 1
        return False
