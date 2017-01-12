from pycopancore.private import _AbstractDynamicsMixin


class Culture (_AbstractDynamicsMixin):
    """
    Abstract class all Culture mixin classes must implement.
    """
    def __init__(self):
        super().__init__()

    processes = []
