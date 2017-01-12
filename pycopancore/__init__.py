"""
This is the pycopancore package
"""
from .private import _AbstractRunner, _AbstractEntityMixin
from .private import _AbstractProcess, _AbstractDynamicsMixin, Variable
from .process_types import ODE, Explicit, Step, Event, Implicit
from .models import Model

__author__ = "Jonathan F. Donges <donges@pik-potsdam.de>"
__copyright__ = \
    "Copyright (C) 2016 Jonathan F. Donges and COPAN team"
__license__ = "MIT license"
__url__ = "http://www.pik-potsdam.de/copan/software"
__version__ = "0.1.0"
__date__ = "2016-05-30"
