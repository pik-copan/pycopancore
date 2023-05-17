"""Cell entity for LPJmL coupling component."""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from .. import interface as I


class Cell(I.Cell):
    """Cell entity type mixin implementation class."""

    def __init__(self,
                 input=None,
                 output=None,
                 network=None,
                 **kwargs):
        """Initialize an instance of Cell."""

        self.input = input
        self.output = output
        self.network = network

    def deactivate(self):
        """Deactivate a Cell."""
        # TODO: add custom code here:
        pass
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate a Cell."""
        super().reactivate()  # must be the first line
        # TODO: add custom code here:
        pass
