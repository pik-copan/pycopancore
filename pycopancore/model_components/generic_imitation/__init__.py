"""
Generic imitation component.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# make sure model composer has named the variables to imitate before importing the component:
from .. import config
try:
    config.generic_imitation['variables']
except:
    config.generic_imitation = {'variables': []}
    print("WARNING (model component generic_imitation): Empty list of variables! Before importing generic_imitation in the model definition, you must import config from model_components and set config.generic_imitation['variables'].")

from . import interface

# export all implementation classes:
from .implementation import *

# export model component mixin class:
from .model import Model
