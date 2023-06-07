"""World entity type mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I
import networkx as nx

from pycopancore.process_types import Step


class World(I.World):
    """World entity type mixin implementation class."""

    def __init__(self,
                 lpjml,
                 **kwargs):
        """Initialize an instance of World."""
        super().__init__(**kwargs)

        self.lpjml = lpjml
        self.input = self.lpjml.read_input()
        self.output = self.lpjml.read_historic_output()
        self.neighbourhood = nx.Graph()

    # process-related methods:
    def update(self, time):
        return time + self.delta_t

    def interact(self, time):

        # TODO: workarounds for now, check if this is the right way to do it
        year = time-1

        self.lpjml.send_input(self.input, year)
        # read output data from lpjml
        self.output = self.lpjml.read_output(year)

        if year == self.lpjml.config.lastyear:
            self.lpjml.close()

    def init_cells(self, model, **kwargs):
        """Init cell instances for each corresponding cell via numpy views"""
        # https://docs.xarray.dev/en/stable/user-guide/indexing.html#copies-vs-views

        # Get neighbourhood of surrounding cells as matrix
        #   (cell, neighbour cells)
        neighbour_matrix = self.lpjml.grid.get_neighbourhood(id=False)

        # Create cell instances
        cells = [model.Cell(input=self.input.isel(cell=icell),
                            output=self.output.isel(cell=icell),
                            **kwargs)  # world = self
                 for icell in self.lpjml.get_cells(id=False)]

        # Build neighbourhood graph nodes from cells
        self.neighbourhood.add_nodes_from(cells)

        # Create neighbourhood graph edges from neighbour matrix
        for icell in self.lpjml.get_cells(id=False):
            for neighbour in neighbour_matrix.isel(cell=icell).values:
                if neighbour >= 0:  # Ignore negative values (-1 or NaN)
                    self.neighbourhood.add_edge(cells[icell], cells[neighbour])

        # Add neighbourhood subgraph for each cell
        for icell in self.lpjml.get_cells(id=False):
            cells[icell].neighbourhood = self.neighbourhood.neighbors(
                cells[icell]
            )

        return cells

    processes = [
        Step("lpjml step",
             [I.World.output],
             [update, interact])
    ]
