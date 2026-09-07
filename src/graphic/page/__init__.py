"""Expose the application pages."""

from src.graphic.page.game import GamePage
from src.graphic.page.high_score import HighScorePage
from src.graphic.page.how_to_play import HowToPlayPage
from src.graphic.page.loading import LoadingPage
from src.graphic.page.menu import MenuPage
from src.graphic.page.parent import ParentPage
from src.graphic.page.player_name import PlayerNamePage

__all__ = [
    "ParentPage",
    "MenuPage",
    "HowToPlayPage",
    "GamePage",
    "PlayerNamePage",
    "LoadingPage",
    "HighScorePage",
]
