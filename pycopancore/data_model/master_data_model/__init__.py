# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# Dimension and Unit objects are defined at attributes in
# dimensions_and_units.DimensionsAndUnits so that sphinx will document them.
# The following makes them accessible as package attributes:
from .dimensions_and_units import *
from .dimensions_and_units import DimensionsAndUnits
from .dimensions_and_units import Dimension
from .dimensions_and_units import Unit

from .environment import Environment as ENV
from .environment import Environment as environment
from .environment import Environment
from .metabolism import Metabolism as MET
from .metabolism import Metabolism as metabolism
from .metabolism import Metabolism
from .culture import Culture as CUL
from .culture import Culture as culture
from .culture import Culture

for k, o in DimensionsAndUnits.__dict__.items():
    if isinstance(o, (Dimension, Unit)):
        globals()[k] = o
