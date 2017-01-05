from pycopancore.private import _AbstractEntityMixin


class Individual (_AbstractEntityMixin):
    """
    Abstract class all Individual mixin classes must implement.
    """
    def __init__(self):
        super(_AbstractEntityMixin, self).__init__()

    processes = []
