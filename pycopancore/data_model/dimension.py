"""Module for Dimension class."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# TODO: doc strings


class Dimension(object):
    """Dimension class."""

    # TODO: make read-only:

    is_base = None
    """whether this is a base dimension"""

    name = None
    """full name"""

    desc = None
    """description"""

    exponents = None
    """dict of base Dimension: nonzero exponent"""

    @property
    def default_unit(self):
        """default Unit"""
        return self._default_unit

    @default_unit.setter
    def default_unit(self, unit):
        assert self.is_base, "non-base dimensions inherit default units"
        self._default_unit = unit
        if unit._dimension is None:
            unit._dimension = self
#        assert unit.dimension == self  # FIXME: fails

    def __init__(self, is_base=True, name=None, desc=None,
                 exponents=None, default_unit=None):
        self.is_base = is_base
        if is_base:
            self.name = name
            self.desc = name if desc is None else desc
            # don't use self as key before name has been assigned since name is
            # used as hash:
            self.exponents = {self: 1}
        else:
            self.exponents = exponents
            # TODO: use words "per", "square", "cubic" and sort be descending
            # exponents
            self.name = " ".join([dim.name + ("" if ex == 1 else "^" + str(ex) if ex >= 0 else "^(" + str(ex) + ")")
                                  for dim, ex in exponents.items()]) if name is None else name
            self.desc = "\n\n".join(
                [dim.name + ": " + dim.desc for dim in exponents.keys()]) if desc is None else desc
        self._default_unit = default_unit

    def named(self, name, desc=None):
        """Named."""
        return Dimension(is_base=self.is_base, name=name, desc=self.desc if desc is None else desc,
                         exponents=self.exponents, default_unit=self.default_unit)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name + " (dimension)"

    def __hash__(self):
        return hash(self.name) if self.is_base else None

    def __eq__(self, other):
        return self.exponents == other.exponents

    def __pow__(self, power):
        """exponentiation **"""
        return Dimension(is_base=False,
                         exponents={dim: ex * power for dim,
                                    ex in self.exponents.items()},
                         default_unit=self.default_unit**power
                         if self.default_unit is not None else None)

    def __mul__(self, other):
        """multiplication *"""
        pex = self.exponents.copy()
        oex = other.exponents
        for dim, ex in oex.items():
            if dim in pex:
                pex[dim] += ex
                if pex[dim] == 0:
                    pex.pop(dim)
            else:
                pex[dim] = ex
        return Dimension(is_base=False,
                         exponents=pex,
                         default_unit=self.default_unit * other.default_unit
                         if self.default_unit is not None
                         and other.default_unit is not None
                         else None)

    def __truediv__(self, other):
        """division /"""
        qex = self.exponents.copy()
        oex = other.exponents
        for dim, ex in oex.items():
            if dim in qex:
                qex[dim] -= ex
                if qex[dim] == 0:
                    qex.pop(dim)
            else:
                qex[dim] = -ex
        return Dimension(is_base=False,
                         exponents=qex,
                         default_unit=self.default_unit / other.default_unit)


nondim = Dimension(name="non-dimensional", desc="non-dimensional",
                   exponents={}, is_base=False)
