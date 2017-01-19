# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is the tmeplate package. Here, templates are written for reducing the
amount of work needed when developing a new component
"""

# Import of all interface modules
from .interface import Cell_, Nature_, Individual_, Culture_, Society_, \
    Metabolism_, Model_

# Import entities
from .cell import Cell
from .nature import Nature
from .individual import Individual

# Import the dynamics
from .culture import Culture
from .society import Society
from .metabolism import Metabolism

# Import Model
from .model import Model

