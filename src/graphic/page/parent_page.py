# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parent_page.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:07:23 by nramalan        #+#    #+#               #
#  Updated: 2026/05/10 21:00:41 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import abstractmethod, ABC
from typing import Optional, Any

from src.enums.page_state import PageState


class ParentPage(ABC):
    def __init__(self) -> None:
        self.state: PageState
        self.next_state: Optional[PageState] = None

    def init(self, window: Any) -> None:
        self.next_state = window.current_state

    @abstractmethod
    def render(self) -> None:
        pass
