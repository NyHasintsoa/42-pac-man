# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_window.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/06 18:44:46 by nramalan        #+#    #+#               #
#  Updated: 2026/05/06 19:18:28 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pyray as pr


class MainWindow:
    def __init__(self, width: int, height: int, title: str) -> None:
        self.width = width
        self.height = height
        self.title = title
        pr.set_trace_log_level(7)
        pr.init_window(self.width, self.height, self.title)
        pr.set_target_fps(60)

    def add_event(self) -> None:
        pr.set_exit_key(pr.KeyboardKey.KEY_NULL)

    def render(self) -> None:
        while not pr.window_should_close():
            pr.begin_drawing()
            pr.clear_background(pr.BLACK)
            pr.end_drawing()
