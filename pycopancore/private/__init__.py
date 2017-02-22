# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is the dummy model-component package.
"""

from ._abstract_process import _AbstractProcess
from ._abstract_dynamics_mixin import _AbstractDynamicsMixin
from ._abstract_entity_mixin import _AbstractEntityMixin
from ._abstract_runner import _AbstractRunner

from .variable import Variable
from .reference_variable import ReferenceVariable
from .set_variable import SetVariable
