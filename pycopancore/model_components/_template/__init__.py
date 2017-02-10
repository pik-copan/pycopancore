# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is the model component template package. 
Here, templates are written for reducing the amount of work needed when developing a new component
"""

# Import all interface classes:
from .interface import *

# Import all needed entity types:
from .world import World
from .cell import Cell
from .society import Society
from .individual import Individual

# Import all needed process taxons:
from .nature import Nature
from .culture import Culture
from .metabolism import Metabolism

# Import model component class:
from .model import Model

