# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  parent_page.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/10 17:07:23 by nramalan        #+#    #+#               #
#  Updated: 2026/05/10 21:53:45 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import abstractmethod, ABC

from src.enums.page_state import PageState


class ParentPage(ABC):
    def __init__(self) -> None:
        self.state: PageState
        self.next_state: PageState

    def on_enter(self) -> None:
        self.next_state = self.state

    @abstractmethod
    def render(self) -> None:
        pass
