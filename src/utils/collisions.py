"""Collision detection utility functions for the Pacman game."""

import pyray as pr
import math


def ft_vector2_distance(v1: pr.Vector2, v2: pr.Vector2) -> float:
    """Calculate the Euclidean distance between two Vector2 points.

    Recreates pr.vector2_distance(v1, v2).

    Args:
        v1 (pr.Vector2): First point in 2D space.
        v2 (pr.Vector2): Second point in 2D space.

    Returns:
        float: Return the Euclidean distance between the two points.
    """
    dx = v2.x - v1.x
    dy = v2.y - v1.y

    return math.sqrt(dx * dx + dy * dy)


def ft_check_collision_point_rec(
    point: pr.Vector2, rect: pr.Rectangle
) -> bool:
    """Manually checks if a Vector2 point is inside a Rectangle.

    Replaces pr.check_collision_point_rec().

    Args:
        point (pr.Vector2): Mouse position or any other point to check.
        rect (pr.Rectangle): Rectangle to check against.

    Returns:
        bool: Returns True if the point is inside the rectangle.
    """
    is_inside_x = rect.x <= point.x <= (rect.x + rect.width)
    is_inside_y = rect.y <= point.y <= (rect.y + rect.height)

    return is_inside_x and is_inside_y
