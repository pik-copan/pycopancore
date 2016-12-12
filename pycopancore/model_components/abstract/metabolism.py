from pycopancore.private import _AbstractEntityMixin


class Metabolism (_AbstractEntityMixin):
    """
    Abstract class all Metabolism mixin classes must implement.
    """
    def __init__(self):
        super(_AbstractEntityMixin, self).__init__()