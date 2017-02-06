# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is the base model-component package. Modules in this package do not
exhibit dynamics, they are just handling the most basic properties of
entity-types and process-taxa
"""

from .world import World
from .cell import Cell
from .individual import Individual
from .society import Society

from .culture import Culture
from .metabolism import Metabolism
from .nature import Nature

from .model import Model
