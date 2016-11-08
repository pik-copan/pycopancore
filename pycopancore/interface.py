from sympy import Symbol

# time:

t_ = Symbol("time")

# and simply unite all component's interfaces:

from pycopancore.individual.interface import *
from pycopancore.group.interface import *
from pycopancore.cell.interface import *
