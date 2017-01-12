from pycopancore.private import _AbstractDynamicsMixin


class Metabolism (_AbstractDynamicsMixin):
    """
    Abstract class all Metabolism mixin classes must implement.
    """
    def __init__(self):
        super().__init__()

    processes = []
