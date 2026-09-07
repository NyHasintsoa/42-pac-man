"""Track pellet completion and advance game levels."""

from typing import TYPE_CHECKING

from src.model.enums import PageState

if TYPE_CHECKING:
    from src.graphic.component import PacgumComponent
    from src.graphic.page import GamePage
    from src.model import GameContext


class LevelManager:
    """Determine when levels are complete and advance them."""

    def __init__(self, context: "GameContext") -> None:
        """Initialize the LevelManager instance.

        Args:
            context: The shared mutable game context.

        Returns:
            The requested result.
        """
        self.context = context

    def count_remaining_pacgums(
        self, pacgum_component: "PacgumComponent"
    ) -> int:
        """Count pellets that have not yet been collected.

        Args:
            pacgum_component: The pellet component to inspect.

        Returns:
            The number of uncollected pellets.
        """
        remaining = 0
        for pacgum in getattr(pacgum_component, "pacgums", []):
            if not pacgum.collected:
                remaining += 1

        for pacgum in getattr(pacgum_component, "super_pacgums", []):
            if not pacgum.collected:
                remaining += 1

        return remaining

    def is_level_completed(self, pacgum_component: "PacgumComponent") -> bool:
        """Return whether every pellet in a level has been collected.

        Args:
            pacgum_component: The pellet component to inspect.

        Returns:
            True when no pellets remain; otherwise False.
        """
        return self.count_remaining_pacgums(pacgum_component) == 0

    def advance_level(self, game_page: "GamePage") -> bool:
        """Advance the game page or finish the game when the level is complete.

        Args:
            game_page: The active game page to update.

        Returns:
            True when another level starts, otherwise False.
        """
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
