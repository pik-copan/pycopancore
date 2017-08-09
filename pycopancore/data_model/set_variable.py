"""Module for SetVariable class."""

from . import Variable
from ..private import _DotConstruct

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
        return _DotConstruct(self, []).__getattr__(name)

    # validation:

    def _check_valid(self, v):
        """check validity of candidate value"""

        if v is None:
            if self.allow_none is False:
                return False, str(self) + " may not be None"
        else:
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
