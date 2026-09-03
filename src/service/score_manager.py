import json
import os
from typing import Any, Dict, List

from src.model import ScoreListModel


class ScoreManager:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def load_scores(self) -> List[Dict[str, Any]]:
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
        scores = self.load_scores()
        if not scores:
            return 0
        return max(int(entry.get("score", 0)) for entry in scores)

    def add_score(self, name: str, score: int, level: int) -> None:
        scores = self.load_scores()
        scores.append({"name": name.upper(), "score": score, "level": level})
        scores.sort(key=lambda x: x["score"], reverse=True)
        self.save_scores(scores)
