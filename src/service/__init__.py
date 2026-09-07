"""Expose application service classes without importing them eagerly."""

from importlib import import_module
from typing import Any, Dict, Tuple

_EXPORTS: Dict[str, Tuple[str, str]] = {
    "CheatingManager": ("src.service.cheating_manager", "CheatingManager"),
    "ConfigParser": ("src.service.config_parser", "ConfigParser"),
    "GhostManager": ("src.service.ghost_manager", "GhostManager"),
    "LevelGenerator": ("src.service.level_generator", "LevelGenerator"),
    "LevelManager": ("src.service.level_manager", "LevelManager"),
    "ResourceManager": ("src.service.resource_manager", "ResourceManager"),
    "ScoreManager": ("src.service.score_manager", "ScoreManager"),
}


def __getattr__(name: str) -> Any:
    """Load a service class only when it is requested."""
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, class_name = _EXPORTS[name]
    service_class = getattr(import_module(module_name), class_name)
    globals()[name] = service_class
    return service_class


__all__ = [
    "ConfigParser",
    "LevelGenerator",
    "LevelManager",
    "ResourceManager",
    "CheatingManager",
    "GhostManager",
    "ScoreManager",
]
