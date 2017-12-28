
# Dimension and Unit objects are defined at attributes in 
# dimensions_and_units.DimensionsAndUnits so that sphinx will document them.
# The following makes them accessible as package attributes:
from .dimensions_and_units import *
for k, o in DimensionsAndUnits.__dict__.items():
    if isinstance(o, (Dimension, Unit)):
        globals()[k] = o

from .environment import Environment as ENV
from .environment import Environment as Environment
from .environment import Environment
from .metabolism import Metabolism as MET
from .metabolism import Metabolism as Metabolism
from .metabolism import Metabolism
from .culture import Culture as CUL
from .culture import Culture as culture
from .culture import Culture

from .world import World as W
from .world import World as World
from .world import World
from .social_system import SocialSystem as S
from .social_system import SocialSystem as SocialSystem
from .social_system import SocialSystem
from .cell import Cell as C
from .cell import Cell as cell
from .cell import Cell
from .individual import Individual as I
from .individual import Individual as Individual
from .individual import Individual

from .. import unity
