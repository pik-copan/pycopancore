from pycopancore.private import _AbstractEntityMixin


class Culture (_AbstractEntityMixin):
    """
    Abstract class all Culture mixin classes must implement.
    """
    def __init__(self):
        super(_AbstractEntityMixin, self).__init__()

    processes = []
