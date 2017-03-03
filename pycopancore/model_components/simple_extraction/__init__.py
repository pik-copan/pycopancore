# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is the simple_extraction model-component package.
"""

# Import of all interface modules
from . import interface as I

# Import entities
from .cell import Cell
from .individual import Individual

# Import the dynamics
from .metabolism import Metabolism

# Import Model
from .model import Model

