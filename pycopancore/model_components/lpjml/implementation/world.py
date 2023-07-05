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
import numpy as np
import networkx as nx

from .. import interface as I

from pycopancore.process_types import Step


class World(I.World):
    """World entity type mixin implementation class."""

    def __init__(self,
                 model=None,
                 lpjml=None,
                 **kwargs):
        """Initialize an instance of World.
        """
        super().__init__(**kwargs)
        if model:
            self.model = model
        else:
            self.model = None

        if lpjml:
            self.lpjml = lpjml
            self.input = self.lpjml.read_input()
            self.output = self.lpjml.read_historic_output()
        else:
            self.lpjml = None
            self.input = None
            self.output = None

        self.neighbourhood = nx.Graph()

        if self.lpjml.config.coupled_config.lpjml_settings.country_code_to_name:  # noqa
            self.lpjml.code_to_name(
                self.lpjml.config.coupled_config.lpjml_settings.iso_country_code  # noqa
            )

    def update_lpjml(self, t):
        """ Exchange input and output data with LPJmL
        """
        self.input.time.values[0] = np.datetime64(f"{t}-12-31")
        # send input data to lpjml
        self.lpjml.send_input(self.input, t)
        # read output data from lpjml
        self.output = self.lpjml.read_output(t)

        if t == self.lpjml.config.lastyear:
            self.lpjml.close()

    def init_cells(self, **kwargs):
        """Init cell instances for each corresponding cell via numpy views"""
        # https://docs.xarray.dev/en/stable/user-guide/indexing.html#copies-vs-views

        # Get neighbourhood of surrounding cells as matrix
        #   (cell, neighbour cells)
        neighbour_matrix = self.lpjml.grid.get_neighbourhood(id=False)

        # Create cell instances
        cells = [
            self.model.Cell(
                world=self,
                input=self.input.isel(cell=icell),
                output=self.output.isel(cell=icell),
                grid=self.lpjml.grid.isel(cell=icell),
                country=self.lpjml.country.isel(cell=icell) if hasattr(self.lpjml, "country") else None,  # noqa
                region=self.lpjml.region.isel(cell=icell) if hasattr(self.lpjml, "region") else None,  # noqa
                **kwargs
            ) for icell in self.lpjml.get_cells(id=False)
        ]

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

    processes = []
