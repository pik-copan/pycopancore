"""
This is the pycopancore package.
"""
from .private import _AbstractRunner, _AbstractEntityMixin, _AbstractProcess, \
    _AbstractProcessTaxonMixin
from .process_types import ODE, Explicit, Step, Event, Implicit
from .data_model import *
from .runners.runner import Runner
from . import model_components, models
from .model_components import base

__url__ = "http://www.pik-potsdam.de/copan/software"
__version__ = "0.1.0"
