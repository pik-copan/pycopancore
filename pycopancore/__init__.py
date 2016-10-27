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
from .group.abstract_group import Group
from .group.abstract_metabolism import Metabolism
from .group.equal_distributor import EqualDistributor
from .individual.abstract_individual import Individual
from .individual.abstract_culture import Culture
from .individual.binary_social_learner import BinarySocialLearner
from .individual.exploit_like import ExploitLike
from .cell.abstract_cell import Cell
from .cell.abstract_planet import Planet
from .cell.donut_world import DonutWorld
from .cell.local_renewable_resource import RenewableResource
from .model.abstract_model import Model
from .model.first_model import FirstModel


__author__ = "Jonathan F. Donges <donges@pik-potsdam.de>"
__copyright__ = \
    "Copyright (C) 2016 Jonathan F. Donges and COPAN team"
__license__ = "MIT license"
__url__ = "http://www.pik-potsdam.de/copan/software"
__version__ = "0.1.0"
__date__ = "2016-05-30"
__docformat__ = "restructuredtext en"
