"""Define errors raised for invalid game configuration."""


class ConfigError(Exception):
    """Represent an invalid or unreadable configuration error."""

    def __init__(self, *args: object) -> None:
        """Initialize the ConfigError instance.

        Args:
            args: The args value.

        Returns:
            The requested result.
        """
        super().__init__(*args)
