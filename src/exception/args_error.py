"""Define errors raised for invalid command-line arguments."""

from src.exception.pacman_error import PacmanError


class ArgsError(PacmanError):
    """Represent an invalid command-line argument error."""

    def __init__(self, *args: object) -> None:
        """Initialize the ArgsError instance.

        Args:
            args: The args value.

        Returns:
            The requested result.
        """
        super().__init__(*args)
