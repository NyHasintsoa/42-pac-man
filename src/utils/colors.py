"""Colors utility functions for the Pacman game."""

import pyray as pr


def ft_fade(color: pr.Color, alpha: float) -> pr.Color:
    """Recreates pr.fade(color, alpha) using standard Python logic.

    Args:
        color (pr.Color): Base pr.Color(r, g, b, a)
        alpha (float): Opacity multiplier from 0.0 (transparent) to 1.0 (fully opaque)

    Returns:
        pr.Color: Returns a new pr.Color with the same RGB values.
    """
    alpha = max(0.0, min(1.0, alpha))
    new_alpha = int(color.a * alpha)

    return pr.Color(color.r, color.g, color.b, new_alpha)
