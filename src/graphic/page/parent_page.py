# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parent_page.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:07:23 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 17:02:09 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from src.data import GameContext
from src.enums.page_state import PageState
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
