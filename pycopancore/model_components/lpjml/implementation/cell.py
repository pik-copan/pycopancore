"""Cell entity for LPJmL coupling component."""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from .. import interface as I
import networkx as nx


class Cell(I.Cell):
    """Cell entity type mixin implementation class."""

    def __init__(self,
                 input=None,
                 output=None,
                 grid=None,
                 country=None,
                 region=None,
                 **kwargs):
        """Initialize an instance of Cell."""

        self.input = input
        self.output = output
        self.neighbourhood = list()
        self.grid = grid
        if country is not None:
            self.country = country
        if region is not None:
            self.region = region

    def __lt__(self, other):
        return self.input.cell.values < other.input.cell.values

    def __eq__(self, other):
        return self.input.cell.values == other.input.cell.values

    def __hash__(self):
        return hash(self.input.cell.values.tolist())

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

    processes = []