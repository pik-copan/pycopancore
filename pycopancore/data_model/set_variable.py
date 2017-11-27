"""Module for SetVariable class."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from . import Variable
from ..private import _DotConstruct, unknown

# TODO: complete logics, set other Variable attributes, validate etc.


class SetVariable(Variable):
    """
    reference to a set of entities
    """

    type = None
    """required type of referred entities
    (will be adjusted by model.configure to point to composite class
    instead of mixin class)"""

    def __init__(self,
                 name,
                 desc,
                 *,
                 type=object,
                 **kwargs):
        super().__init__(name, desc, **kwargs)
        self.type = type

    def __getattr__(self, name):
        """return a _DotConstruct representing a variable of the referenced class"""
        if name == "__qualname__":  # needed to make sphinx happy
            return "DUMMY"  # FIXME!
        return _DotConstruct(self, []).__getattr__(name)

    # validation:

    def _check_valid(self, v):
        """check validity of candidate value"""

        if v is None:
            if self.allow_none is False:
                return False, str(self) + " may not be None"
        elif v is not unknown:
            # TODO: assert v is iterable!
            for i in v:
                if self.type is not None:
                    if not isinstance(i, self.type):
                        return False, \
                            str(self) + " must consist of instances of " \
                            + str(self.type)
                res = super()._check_valid(i)
                if res is not True:
                    return res

        return True

    def __str__(self):
        return (self.owning_class.__name__ + "." + self.codename) \
                if self.owning_class \
                else self.name + "(uid=" + self._uid + ")"

    def __repr__(self):
        if self.owning_class:
            return self.owning_class.__name__ + "." + self.codename
        r = "read-only " if self.readonly else ""
        r += "extensive " if self.is_extensive else ""
        r += "intensive " if self.is_intensive else ""
        r += "set variable '" + self.name + "'"
        if self.desc not in ("", None):
            r += " (" + self.desc + ")"
        if self.ref is not None:
            r += ", ref=" + self.ref
        if self.CF is not None:
            r += ", CF=" + self.CF
        if self.AMIP is not None:
            r += ", AMIP=" + self.AMIP
        if self.IAMC is not None:
            r += ", IAMC=" + self.IAMC
        if self.CETS is not None:
            r += ", CETS=" + self.CETS
        if self.symbol not in ("", None):
            r += ", symbol=" + self.symbol
        if self.allow_none is False:
            r += ", not None"
        if self.scale not in ("", None):
            r += ", scale=" + self.scale
        if self.type is not None:
            r += ", type=" + str(self.datatype)
        return r # + " (uid=" + str(self._uid) + ")"
