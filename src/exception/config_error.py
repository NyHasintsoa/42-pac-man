# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_error.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/27 15:42:16 by nramalan        #+#    #+#               #
#  Updated: 2026/05/27 15:47:42 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

class ConfigError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
