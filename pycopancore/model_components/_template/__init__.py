"""
Model component package template.

TODO: 
Copy this folder, rename it to the name of your model component, 
then adjust or fill in code and documentation in all modules wherever marked by "TODO:", 
finally remove these instructions.
See the model component development tutorial for details.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license


# Import all interface classes:
from .interface import *

# Import all provided entity type implementation mixin classes:
from .world import World
from .cell import Cell
from .society import Society
from .individual import Individual

# Import all provided process taxon implementation mixin classes:
from .nature import Nature
from .culture import Culture
from .metabolism import Metabolism

# Import model component mixin class:
from .model import Model

