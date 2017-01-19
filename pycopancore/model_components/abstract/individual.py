# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Abstract class which all Individual mixin classes must implement.
"""

from pycopancore.private import _AbstractEntityMixin


class Individual (_AbstractEntityMixin):
    """
    Abstract class which all Individual mixin classes must implement.
    """
    def __init__(self):
        super().__init__()

    processes = []
