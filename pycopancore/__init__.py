"""
This is the pycopancore package.
"""
from .private import _AbstractRunner, _AbstractEntityMixin
from .private import _AbstractProcess, _AbstractProcessTaxonMixin
from .process_types import ODE, Explicit, Step, Event, Implicit
from .data_model import *
from .runners import Runner
from . import model_components, models

__url__ = "http://www.pik-potsdam.de/copan/software"
__version__ = "0.1.0"
