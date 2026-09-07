"""Define errors raised while loading or saving high scores."""

from src.exception.pacman_error import PacmanError


class ScoreError(PacmanError):
    """Represent an invalid or inaccessible high-score file."""
