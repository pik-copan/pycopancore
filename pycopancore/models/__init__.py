# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is the model package. It fuses different classes to new classes. The
base-classes need to be used, especially the base.model, since it has the
configure method
"""

from .base_only import Model
from .base_and_dummy import Model
