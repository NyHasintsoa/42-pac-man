# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parent.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:07:23 by nramalan        #+#    #+#               #
#  Updated: 2026/07/13 15:14:45 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.model import GameContext
from src.model.enums.page_state import PageState

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class ParentPage(ABC):
    def __init__(self, window: MainWindow) -> None:
        self.window = window
        self.context: GameContext = window.context
        self.state: PageState
        self.next_state: PageState

    def init(self, context: GameContext) -> None:
        self.next_state = self.state
        self.context = context

    @abstractmethod
    def render(self) -> None:
        pass
