from . import Variable
from ..private import _DotConstruct

# TODO: complete logics, set other Variable attributes, validate etc.


class SetVariable (Variable):
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
        """return an object representing a class attribute of the referenced class"""
        return _DotConstruct(self, [None, name])
