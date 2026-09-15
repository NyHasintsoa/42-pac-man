"""Utils for graphic library."""

from src.graphic.utils.collisions import (
    ft_check_collision_point_rec,
    ft_vector2_distance,
)
from src.graphic.utils.resource_manager import ResourceManager

__all__ = [
    "ResourceManager",
    "ft_check_collision_point_rec",
    "ft_vector2_distance",
]
