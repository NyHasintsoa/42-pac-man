from typing import List

from pydantic import BaseModel, Field, RootModel


class ScoreEntry(BaseModel):
    name: str = Field(..., min_length=1, max_length=12)
    score: int = Field(..., ge=0)
    level: int = Field(..., ge=1)


ScoreListModel = RootModel[List[ScoreEntry]]
