# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# TODO: doc strings

from functools import reduce
import operator
from numpy import log10

from . import dimension, dimensional_quantity, nondim


class Unit (object):

    is_base = None
    """whether this is a base unit"""

    name = None
    """full name"""

    symbol = None
    """symbol"""

    desc = None
    """description"""

    factor = None
    """scalar factor in front of product of powers of base Units"""

    exponents = None
    """dict of base Unit: nonzero exponent"""

    _dimension = None

    _dimensional_quantity_class = None  # will be set in data_model.__init__

    @property
    def dimension(self):
        """corresponding Dimension"""
        if self.is_base:
            return self._dimension
        else:
            return reduce(operator.mul,
                          [unit.dimension**ex
                           for unit, ex in self.exponents.items()],
                          dimension.nondim)

    def __init__(self,
                 name="",
                 desc="",
                 *,
                 is_base=True,
                 symbol=None,
                 factor=1,
                 exponents=None,
                 dimension=None):
        assert factor > 0, "factor must be positive"
        self.factor = factor
        self.is_base = is_base
        if is_base:
            self.name = name
            self.symbol = symbol
            self.desc = name if desc is None else desc
            # don't use self as key before name has been assigned since name is
            # used as hash:
            self.exponents = {self: 1}
            if dimension is not None:
                assert dimension.is_base, \
                    "dimension of base unit must be base dimension"
            self._dimension = dimension
        else:
            self.exponents = exponents.copy()
            # TODO: use words "per", "square", "cubic" and sort be descending
            # exponents
            self.name = (str(self.factor) + " " if self.factor != 1 else "") \
                + " ".join([unit.name
                            + ("" if ex == 1
                               else "^" + str(ex) if ex >= 0
                               else "^(" + str(ex) + ")")
                            for unit, ex in exponents.items()]) \
                if name is None else name
            if symbol is not None:
                self.symbol = symbol
            else:
                # TODO: sort exponents.items by alphabetical unit.symbol
                items = sorted([(unit.symbol, ex) 
                                for unit, ex in exponents.items()], 
                               key=lambda i: (-i[1], i[0]))
                self.symbol = ("" if factor == 1 
                               else ("1e" + str(int(log10(factor))) 
                                                if log10(factor)%1 == 0
                                     else str(int(factor)) if factor%1 == 0 
                                     else str(factor)) 
                               + " ")
                self.symbol += " ".join([sym
                                        + ("" if ex == 1
                                           else "²" if ex == 2
                                           else "³" if ex == 3
                                           else "^" + str(int(ex)) if ex%1 == 0
                                           else "^" + str(ex)
                                           )
                                      for sym, ex in items])
            self.desc = "\n\n".join([unit.name + ": " + unit.desc
                                     for unit in exponents.keys()]) \
                        if desc is None else desc
            assert dimension is None, \
                "dimension of non-base unit is derived automatically"

    def named(self, name, desc=None, *, symbol=None):
        return Unit(is_base=self.is_base, name=name,
                    symbol=self.symbol if symbol is None else symbol,
                    desc=self.desc if desc is None else desc,
                    factor=self.factor, exponents=self.exponents.copy(),
                    dimension=self.dimension if self.is_base else None)

    def convert(self, number, unit):
        assert unit.dimension == self.dimension, \
            "can't convert from " + str(self) \
            + " to " + str(unit)
        if isinstance(number, list):
            return [i * self.factor / unit.factor for i in number]
        else:
            return number * self.factor / unit.factor

    # standard methods and operators:

    def __repr__(self):
        return ("" if self.name in (None, "") else self.name + " ") \
            + "[" + self.symbol + "]"

    def __hash__(self):
        return hash(self.name) if self.is_base else None

    def __eq__(self, other):
        if self.is_base:
            return other.is_base and other.dimension == self.dimension \
                and other.name == self.name
        else:
            return self.factor == other.factor \
                and self.exponents == other.exponents

    def __pow__(self, power):
        """exponentiation **"""
        return Unit(is_base=False,
                    factor=self.factor**power,
                    exponents={unit: ex * power
                               for unit, ex in self.exponents.items()})

    def __mul__(self, other):
        """unit * other returns a unit
        (while non-unit * unit would return a DimensionalQuantity)"""
        pex = self.exponents.copy()
        if isinstance(other, Unit):
            oex = other.exponents
            for unit, ex in oex.items():
                if unit in pex:
                    pex[unit] += ex
                    if pex[unit] == 0:
                        pex.pop(unit)
                else:
                    pex[unit] = ex
            return Unit(is_base=False,
                        factor=self.factor * other.factor, exponents=pex)
        else:
            return Unit(is_base=False, factor=self.factor * other,
                        exponents=pex)

    def __truediv__(self, other):
        """unit / other returns a unit
        (while non-unit / unit would return a DimensionalQuantity)"""
        qex = self.exponents.copy()
        if isinstance(other, Unit):
            oex = other.exponents
            for unit, ex in oex.items():
                if unit in qex:
                    qex[unit] -= ex
                    if qex[unit] == 0:
                        qex.pop(unit)
                else:
                    qex[unit] = -ex
            return Unit(is_base=False, factor=self.factor / other.factor,
                        exponents=qex)
        else:
            return Unit(is_base=False, factor=self.factor / other,
                        exponents=qex)

    def __rtruediv__(self, other):
        """non-unit / unit returns a DimensionalQuantity"""
        return dimensional_quantity.DimensionalQuantity(number=other,
                                                        unit=self**(-1))

    def __rmul__(self, other):
        """non-unit * unit returns a DimensionalQuantity"""
        return dimensional_quantity.DimensionalQuantity(number=other,
                                                        unit=self)


unity = Unit(name="unity", symbol="", desc="number of unity", exponents={}, is_base=False) # dimension=nondim,
