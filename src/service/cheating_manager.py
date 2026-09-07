"""Apply optional gameplay cheats."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.graphic.page import GamePage


class CheatingManager:
    """Store and apply optional gameplay cheat actions."""

    def __init__(self) -> None:
        """Initialize the CheatingManager instance.

        Returns:
            The requested result.
        """
        self.invincible: bool = False
        self.ghost_freeze: bool = False
        self.speed_boost: bool = False

    def add_extra_life(self, game_page: "GamePage") -> None:
        """Add one life to the active game page.

        Args:
            game_page: The active game page to update.

        Returns:
            The requested result.
        """
        game_page.lives += 1

    def skip_level(self, game_page: "GamePage") -> None:
        """Move to the next level or return to the menu after the final level.

        Args:
            game_page: The active game page to update.

        Returns:
            The requested result.
        """
        game_page.is_cheating = False
        if game_page.current_level < len(game_page.levels):
            game_page.current_level += 1
            game_page.init(game_page.context)
        else:
            game_page.return_to_menu()
