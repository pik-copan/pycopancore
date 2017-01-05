from pycopancore.private import _AbstractEntityMixin


class Society (_AbstractEntityMixin):
    """
    Abstract class all Soiety mixin classes must implement.
    """
    def __init__(self):
        super(_AbstractEntityMixin, self).__init__()

    processes = []

