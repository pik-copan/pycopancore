from . import nondim, unity
#from . import Unit # would cause a circular import...


class DimensionalQuantity (object):
    """Physical or other dimensional quantity given by
    a multiple of some unit"""

    # Note: we avoid the word "value" in this code since
    # it is ambiguous (may refer to the whole quantity or just
    # the multiple)

    # basic data:
    _multiple = None
    _unit = None

    _dimension = None

    def multiple(self, unit=None):
        """return multiple in some (or the default) unit"""
        if unit is None:
            return self._multiple
        else:
            return self._unit.convert(self._multiple, unit)

    @property  # read-only
    def unit(self):
        return self._unit

    @property  # read-only
    def dimension(self):
        return self._dimension

    def __init__(self, multiple, unit):
        self._multiple = multiple
#        assert isinstance(unit, Unit), "unit must be a Unit object" # would require circular import...
        self._unit = unit
        self._dimension = unit.dimension

    def __repr__(self):
        return str(self._multiple) + " " + self._unit.symbol

    def __hash__(self):
        return hash((self._multiple, self._unit))

    def reduce(self):
        """return simple number if nondimensional"""
        return self._multiple * self._unit.factor \
            if self._dimension == nondim else self

    def __pow__(self, power):
        return DimensionalQuantity(self._multiple**power, self._unit**power) \
            .reduce()

    def __add__(self, other):
        if len(self._unit.exponents) > 0:
            assert isinstance(other, DimensionalQuantity), \
                "can only add DimensionalQuantity to DimensionalQuantity"
        elif not isinstance(other, DimensionalQuantity):
            other = DimensionalQuantity(other, unity)
        assert other._dimension == self._dimension, \
            "different dimensions cannot be added"
        return DimensionalQuantity(self._multiple
                + other._multiple*other._unit.factor/self._unit.factor,
                self._unit).reduce()

    def __sub__(self, other):
        if len(self._unit.exponents) > 0:
            assert isinstance(other, DimensionalQuantity), \
                "can only subtract DimensionalQuantity from DimensionalQuantity"
        elif not isinstance(other, DimensionalQuantity):
            other = DimensionalQuantity(other, unity)
        assert other._dimension == self._dimension, \
            "different dimensions cannot be subtracted"
        return DimensionalQuantity(self._multiple 
                - other._multiple*other._unit.factor/self._unit.factor,
                self._unit).reduce()

    def __mul__(self, other):
        if isinstance(other, DimensionalQuantity):
            return DimensionalQuantity(self._multiple * other._multiple, 
                                       self._unit * other._unit).reduce()
        else:
            return DimensionalQuantity(self._multiple * other, self._unit)\
                        .reduce()

    def __truediv__(self, other):
        if isinstance(other, DimensionalQuantity):
            return DimensionalQuantity(self._multiple / other._multiple, 
                                       self._unit / other._unit).reduce()
        else:
            return DimensionalQuantity(self._multiple / other, self._unit)\
                        .reduce()

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return self**(-1) * other
