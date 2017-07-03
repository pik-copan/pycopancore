from . import Variable
from ..private import _DotConstruct

# TODO: complete logics, set other Variable attributes, validate etc.


class ReferenceVariable (Variable):
    """
    reference to another entity or process taxon
    """

    type = None
    """required type of referred entity or taxon
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
        """return an object representing a class attribute of the referenced class"""
        return _DotConstruct(self, [None, name])

    # validation:

    def _check_valid(self, v):
        """check validity of candidate value"""

        if v is None:
            if self.allow_none is False:
                return False, str(self) + " may not be None"
        else:
            if self.type is not None:
                if not isinstance(v, self.type):
                    return False, \
                        str(self) + " must be instance of " + str(self.type)

        return super()._check_valid(v)
