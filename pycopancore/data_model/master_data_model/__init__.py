# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .cell import Cell
from .culture import Culture

# Import dimensions and units
from .dimensions_and_units import DimensionsAndUnits

# Import core classes
from .environment import Environment
from .group import Group
from .individual import Individual
from .metabolism import Metabolism
from .social_system import SocialSystem
from .world import World

# Create aliases for backward compatibility
ENV = Environment
MET = Metabolism
CUL = Culture
W = World
S = SocialSystem
C = Cell
# Individual class is available as Individual
G = Group

# Make dimensions and units available as module attributes
for k, o in DimensionsAndUnits.__dict__.items():
    if hasattr(o, "__class__") and "Dimension" in str(type(o)):
        globals()[k] = o
    elif hasattr(o, "__class__") and "Unit" in str(type(o)):
        globals()[k] = o

# Define what this module exports
__all__ = [
    "Environment",
    "Metabolism",
    "Culture",
    "World",
    "SocialSystem",
    "Cell",
    "Individual",
    "Group",
    "DimensionsAndUnits",
    "ENV",
    "MET",
    "CUL",
    "W",
    "S",
    "C",
    "G",
]
