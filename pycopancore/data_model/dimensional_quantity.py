from . import dimension
from . import unit as U


class DimensionalQuantity (object):
    """Physical or other dimensional quantity given by
    a number of some unit"""

    # Note: we avoid the word "value" in this code since
    # it is ambiguous (may refer to the whole quantity or just
    # the number)

    # basic data:
    _number = None
    _unit = None

    _dimension = None

    def number(self, unit=None):
        """return number in some (or the default) unit"""
        if unit is None:
            return self._number
        else:
            return self._unit.convert(self._number, unit)

    @property  # read-only
    def unit(self):
        return self._unit

    @property  # read-only
    def dimension(self):
        return self._dimension

    def __init__(self, number, unit):
        assert not isinstance(number, DimensionalQuantity), \
            "number must be a non-dimensional number or vector"
        self._number = number
        assert isinstance(unit, U.Unit), "unit must be a Unit object" # would require circular import...
        self._unit = unit
        self._dimension = unit.dimension

    def __repr__(self):
        return str(self._number) + " " + self._unit.symbol

    def __hash__(self):
        return hash((self._number, self._unit))

    def reduce(self):
        """return simple number if nondimensional"""
        return self._number * self._unit.factor \
            if self._dimension == dimension.nondim else self

    def __pow__(self, power):
        return DimensionalQuantity(self._number**power, self._unit**power) \
            .reduce()

    def __add__(self, other):
        if len(self._unit.exponents) > 0:
            assert isinstance(other, DimensionalQuantity), \
                "can only add DimensionalQuantity to DimensionalQuantity"
        elif not isinstance(other, DimensionalQuantity):
            other = DimensionalQuantity(other, U.unity)
        assert other._dimension == self._dimension, \
            "different dimensions cannot be added"
        return DimensionalQuantity(self._number
                + other._number*other._unit.factor/self._unit.factor,
                self._unit).reduce()

    def __sub__(self, other):
        if len(self._unit.exponents) > 0:
            assert isinstance(other, DimensionalQuantity), \
                "can only subtract DimensionalQuantity from DimensionalQuantity"
        elif not isinstance(other, DimensionalQuantity):
            other = DimensionalQuantity(other, U.unity)
        assert other._dimension == self._dimension, \
            "different dimensions cannot be subtracted"
        return DimensionalQuantity(self._number 
                - other._number*other._unit.factor/self._unit.factor,
                self._unit).reduce()

    def __mul__(self, other):
        # TODO: improve the following dirty fix:
        if hasattr(other, 'exponents'): # then it is probably a Unit
            return DimensionalQuantity(self._number,
                                       self._unit * other).reduce()
        elif isinstance(other, DimensionalQuantity):
            return DimensionalQuantity(self._number * other._number, 
                                       self._unit * other._unit).reduce()
        else:
            return DimensionalQuantity(self._number * other, self._unit)\
                        .reduce()

    def __truediv__(self, other):
        # TODO: improve the following dirty fix:
        if hasattr(other, 'exponents'): # then it is probably a Unit
            return DimensionalQuantity(self._number,
                                       self._unit / other).reduce()
        elif isinstance(other, DimensionalQuantity):
            return DimensionalQuantity(self._number / other._number,
                                       self._unit / other._unit).reduce()
        else:
            return DimensionalQuantity(self._number / other, self._unit)\
                        .reduce()

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return self**(-1) * other
