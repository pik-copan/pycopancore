from .unit import Unit
from .base_dimensions_units import nondim

class DimensionalQuantity():
    
    @property
    def value(self):
        return self._value
        
    @property
    def unit(self):
        return self._unit
    
    _dimension = None
                
    def __init__(self, value, unit):
        self._value = value
        assert type(unit) == Unit, "unit must be a Unit object"
        self._unit = unit
        self._dimension = unit.dimension
        
    def __repr__(self):
        return str(self._value) + " " + self._unit.symbol
    
    def __hash__(self):
        return hash((self._value, self._unit))
    
    def reduce(self):
        """return simple number if nondimensional"""
        return self._value * self._unit.factor if self._dimension == nondim else self
    
    def __pow__(self, power):
        return DimensionalQuantity(self._value**power, self._unit**power).reduce()
        
    def __add__(self, other):
        if len(self._unit.exponents) > 0:
            assert type(other) == DimensionalQuantity, "can only add DimensionalQuantity to DimensionalQuantity"
        elif type(other) != DimensionalQuantity:
            other = DimensionalQuantity(other, unity)
        assert other._dimension == self._dimension, "different dimensions cannot be added"
        return DimensionalQuantity(self._value + other._value*other._unit.factor/self._unit.factor, self._unit).reduce()

    def __sub__(self, other):
        if len(self._unit.exponents) > 0:
            assert type(other) == DimensionalQuantity, "can only subtract DimensionalQuantity from DimensionalQuantity"
        elif type(other) != DimensionalQuantity:
            other = DimensionalQuantity(other, unity)
        assert other._dimension == self._dimension, "different dimensions cannot be subtracted"
        return DimensionalQuantity(self._value - other._value*other._unit.factor/self._unit.factor, self._unit).reduce()

    def __mul__(self, other):
        if type(other) == DimensionalQuantity:
            return DimensionalQuantity(self._value * other._value, self._unit * other._unit).reduce()
        else:
            return DimensionalQuantity(self._value * other, self._unit).reduce()
        
    def __truediv__(self, other):
        if type(other) == DimensionalQuantity:
            return DimensionalQuantity(self._value / other._value, self._unit / other._unit).reduce()
        else:
            return DimensionalQuantity(self._value / other, self._unit).reduce()
        
    def __radd__(self, other):
        return self + other
    
    def __rsub__(self, other):
        return -self + other
    
    def __rmul__(self, other):
        return self * other
    
    def __rtruediv__(self, other):
        return self**(-1) * other
    