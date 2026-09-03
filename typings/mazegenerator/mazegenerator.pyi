# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mazegenerator.pyi                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 15:51:26 by nramalan        #+#    #+#               #
#  Updated: 2026/05/10 15:52:22 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

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

    def generate(self, seed: int = ...) -> None: ...
