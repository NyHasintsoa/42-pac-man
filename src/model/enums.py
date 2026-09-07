"""Define enumerations used by the user interface."""

from enum import StrEnum


class PageState(StrEnum):
    """Identify the page currently displayed by the application."""

    LOADING_PAGE = "LOADING_PAGE"
    MAIN_MENU = "MAIN_MENU"
    HELP_MENU = "HELP_MENU"
    GAME_PAGE = "GAME_PAGE"
    PLAYER_NAME_PAGE = "PLAYER_NAME_PAGE"
    HIGH_SCORES_PAGE = "HIGH_SCORES_PAGE"
