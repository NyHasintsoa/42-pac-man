"""Define the shared interface for application pages."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.model import GameContext
from src.model.enums import PageState

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class ParentPage(ABC):
    """Define the base interface and lifecycle for a page."""

    def __init__(self, window: "MainWindow") -> None:
        """Initialize the ParentPage instance.

        Args:
            window: The application window owning the component.

        Returns:
            The requested result.
        """
        self.window = window
        self.context: GameContext = window.context
        self.state: PageState
        self.next_state: PageState
        self._is_unloaded = False

    def init(self, context: "GameContext") -> None:
        """Initialize the page with a shared game context.

        Args:
            context: The shared mutable game context.

        Returns:
            The requested result.
        """
        self.next_state = self.state
        self.context = context

    def unload(self) -> None:
        """Release graphical resources owned by the component.

        Returns:
            The requested result.
        """
        if self._is_unloaded:
            return
        self._is_unloaded = True

    @abstractmethod
    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        pass
