# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is the abstract model-component package. All modules in this package are
only used as flags to show that some other module is of the type of the module
in the abstract package.
"""
from .interface import Cell_, Nature_, Individual_, Culture_, Society_, \
    Metabolism_, Model_

from .cell import Cell
from .nature import Nature
from .individual import Individual
from .culture import Culture
from .society import Society
from .metabolism import Metabolism

from .model import Model
