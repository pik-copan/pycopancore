from .variable import Variable

# TODO: complete logics, set other Variable attributes, validate etc.


class ReferenceVariable (Variable):
    """
    reference to another entity or process taxon
    """

    type = None
    """required type of referred entity or taxon"""

    def __init__(self,
                 name,
                 desc,
                 *,
                 type=object,
                 **kwargs):
        super().__init__(name, desc, **kwargs)
        self.type = type
