# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
pycopancore
===========

Subpackages
-----------

None yet.

"""
from .group import Group
from .group import Metabolism
from .group import EqualDistributor
from .individual import Individual
from .individual import Culture
from .individual import BinarySocialLearner
from .individual import ExploitLike
from .cell import Cell
from .cell import Planet
from .cell import DonutWorld
from .cell import RenewableResource
from .model import Model
from .model import FirstModel


__author__ = "Jonathan F. Donges <donges@pik-potsdam.de>"
__copyright__ = \
    "Copyright (C) 2016 Jonathan F. Donges and COPAN team"
__license__ = "MIT license"
__url__ = "http://www.pik-potsdam.de/copan/software"
__version__ = "0.1.0"
__date__ = "2016-05-30"
__docformat__ = "restructuredtext en"
