from typing import List, Tuple

class MazeGenerator:
    def __init__(
        self,
        size: Tuple[int, int] = ...,
        perfect: bool = ...,
        entry_cell: Tuple[int, int] = ...,
        exit_cell: Tuple[int, int] = ...,
        seed: int = ...,
    ) -> None: ...
    @property
    def maze(self) -> List[List[int]]: ...
    @property
    def shortest_path(self) -> str | bool: ...
    @property
    def maze_entry(self) -> Tuple[int, int]: ...
    @property
    def maze_exit(self) -> Tuple[int, int]: ...
    def generate(self, seed: int = 0) -> None: ...
