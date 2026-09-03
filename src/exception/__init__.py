# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __init__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/06 18:36:52 by nramalan        #+#    #+#               #
#  Updated: 2026/07/14 14:56:46 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.exception.args_error import ArgsError
from src.exception.config_error import ConfigError

__all__ = [
    "ArgsError",
    "ConfigError",
]
