"""Load, validate, and save high scores."""

import json
import os
from typing import Any, Dict, List

from src.model import ScoreListModel


class ScoreManager:
    """Persist and retrieve validated high-score entries."""

    def __init__(self, filepath: str) -> None:
        """Initialize the ScoreManager instance.

        Args:
            filepath: The path to the score JSON file.

        Returns:
            The requested result.
        """
        self.filepath = filepath

    def load_scores(self) -> List[Dict[str, Any]]:
        """Load, validate, sort, and return saved scores.

        Returns:
            Validated scores sorted from highest to lowest.
        """
        if not os.path.exists(self.filepath):
            self.save_scores([])
            return []

        try:
            with open(self.filepath, "r") as f:
                raw_data = json.load(f)
            validated_data = ScoreListModel.model_validate(raw_data)
            scores = [entry.model_dump() for entry in validated_data.root]
        except Exception:
            self.save_scores([])
            scores = []

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores

    def save_scores(self, scores: List[Dict[str, Any]]) -> None:
        """Validate and write score entries to the configured file.

        Args:
            scores: Score entries to validate and persist.

        Returns:
            The requested result.
        """
        try:
            validated_data = ScoreListModel.model_validate(scores)
            with open(self.filepath, "w") as f:
                json.dump(
                    [item.model_dump() for item in validated_data.root],
                    f,
                    indent=4,
                )
        except Exception as e:
            print(f"[ScoreManager] Failed to validate or save scores: {e}")

    def get_high_score(self) -> int:
        """Return the highest saved score, or zero when none exist.

        Returns:
            The highest saved score, or zero.
        """
        scores = self.load_scores()
        if not scores:
            return 0
        return max(int(entry.get("score", 0)) for entry in scores)

    def add_score(self, name: str, score: int, level: int) -> None:
        """Append a normalized score entry and save the updated list.

        Args:
            name: The player name to store.
            score: The points awarded when collected.
            level: The level configuration supplying pellet settings.

        Returns:
            The requested result.
        """
        scores = self.load_scores()
        scores.append({"name": name.upper(), "score": score, "level": level})
        scores.sort(key=lambda x: x["score"], reverse=True)
        self.save_scores(scores)
