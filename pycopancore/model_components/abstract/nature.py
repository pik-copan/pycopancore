from pycopancore.private import _AbstractDynamicsMixin


class Nature (_AbstractDynamicsMixin):
    """
    Abstract class all Nature mixin classes must implement.
    """
    def __init__(self):
        super().__init__()

    processes = []
