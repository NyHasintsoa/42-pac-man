from typing import List

from pydantic import BaseModel, Field, model_validator

from src.exception import ConfigError


class LevelConfig(BaseModel):
    width: int = 20
    height: int = 10

    seed: int = Field(default=1, ge=1)
    level_max_time: int = Field(default=1, ge=1)
    pacgum: int = Field(default=1, ge=1)
    points_per_pacgum: int = Field(default=1, ge=1)
    points_per_super_pacgum: int = Field(default=1, ge=1)
    points_per_ghost: int = Field(default=1, ge=1)


class GameConfig(BaseModel):
    highscore_filename: str = Field(min_length=6)
    cheating: bool = Field(default=False)
    lives: int = Field(ge=1)
    level_max_time: int = Field(ge=5)
    seed: int
    pacgum: int = Field(ge=1)
    points_per_pacgum: int = Field(ge=1)
    points_per_super_pacgum: int = Field(ge=1)
    points_per_ghost: int = Field(ge=1)
    levels: List[LevelConfig]

    @model_validator(mode="after")
    def populate_level_defaults(self) -> GameConfig:
        count: int = 1
        for level in self.levels:
            if level.seed == 1:
                level.seed = self.seed
            if level.level_max_time == 1:
                level.level_max_time = self.level_max_time
            if level.pacgum == 1:
                level.pacgum = self.pacgum
            if level.points_per_pacgum == 1:
                level.points_per_pacgum = self.points_per_pacgum
            if level.points_per_super_pacgum == 1:
                level.points_per_super_pacgum = self.points_per_super_pacgum
            if level.points_per_ghost == 1:
                level.points_per_ghost = self.points_per_ghost
            max_pacgum: int = (level.width * level.height) - 23
            if max_pacgum < level.pacgum:
                raise ConfigError("pacgum can't be inserted")
            count += 1
        if count < 10:
            raise ConfigError("not enough level")
        return self

    @classmethod
    def parse_json(cls, json_str: str) -> GameConfig:
        return cls.model_validate_json(json_str)
