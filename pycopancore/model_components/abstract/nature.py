from pycopancore.private import _AbstractEntityMixin


class Nature (_AbstractEntityMixin):
    """
    Abstract class all Nature mixin classes must implement.
    """
    def __init__(self):
        super(_AbstractEntityMixin, self).__init__()