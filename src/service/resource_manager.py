"""Resolve files shipped with the application."""

import sys
from pathlib import Path


class ResourceManager:
    """Provide paths that work from source and PyInstaller bundles."""

    @staticmethod
    def _root() -> Path:
        """Return the application resource root."""
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS)  # type: ignore[attr-defined]
        return Path(__file__).resolve().parents[2]

    @classmethod
    def path(cls, *parts: str) -> str:
        """Return an absolute path for an application resource."""
        return str(cls._root().joinpath(*parts))

    @classmethod
    def asset(cls, *parts: str) -> str:
        """Return an absolute path inside the assets directory."""
        return cls.path("assets", *parts)

    @classmethod
    def font(cls, filename: str) -> str:
        """Return an absolute path for a bundled font."""
        return cls.asset("fonts", filename)
