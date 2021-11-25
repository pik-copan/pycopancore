"""
Port of MAGICC6.0 as described in Meinshausen et al. 2008
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from . import interface

# export all implementation classes:
from .implementation import *

# export model component mixin class:
from .model import Model

from .interface import ppmvCO2
