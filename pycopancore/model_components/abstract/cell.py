from pycopancore.private import _AbstractEntityMixin


class Cell (_AbstractEntityMixin):
    """
    Abstract class all Cell mixin classes must implement.
    """
    def __init__(self):
        super(_AbstractEntityMixin, self).__init__()

    processes = []
