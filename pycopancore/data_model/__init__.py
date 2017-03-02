from .dimension import Dimension
from .unit import Unit

nondim = Dimension(name="non-dimensional", desc="non-dimensional",
                   exponents={})
nondim.default_unit = unity = Unit(name="unity", symbol="",
                                   desc="number of unity", exponents={})

from .dimensional_quantity import DimensionalQuantity

from .variable import Variable
from .reference_variable import ReferenceVariable
#from .set_variable import SetVariable

from . import master_data_model
