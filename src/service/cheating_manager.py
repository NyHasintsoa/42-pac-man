from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.graphic.page import GamePage


class CheatingManager:
    def __init__(self) -> None:
        self.invincible: bool = False
        self.ghost_freeze: bool = False
        self.speed_boost: bool = False

    def add_extra_life(self, game_page: "GamePage") -> None:
        game_page.lives += 1

    def skip_level(self, game_page: "GamePage") -> None:
        game_page.is_cheating = False
        if game_page.current_level < len(game_page.levels):
            game_page.current_level += 1
            game_page.init(game_page.context)
        else:
            game_page.return_to_menu()
