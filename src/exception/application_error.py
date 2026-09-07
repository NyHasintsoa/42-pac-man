"""Define errors raised while running the game application."""

from src.exception.pacman_error import PacmanError


class ApplicationError(PacmanError):
    """Represent an unexpected failure while running the game."""
