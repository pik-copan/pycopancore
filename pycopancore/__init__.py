"""
This is the pycopancore package.
"""
from pycopancore.data_model import *
from .private import _AbstractEntityMixin, _AbstractProcessTaxonMixin
Variable._et_abc = _AbstractEntityMixin  # to avoid circular imports
Variable._pt_abc = _AbstractProcessTaxonMixin  # to avoid circular imports

from .private import *
from .process_types import ODE, Explicit, Step, Event, Implicit
from .runners.runner import Runner
from . import model_components, models
from .model_components import base

__url__ = "http://www.pik-potsdam.de/copan/software"
__version__ = "0.1.0"
