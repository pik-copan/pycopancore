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

from pycopancore.process_types import Step


class Earth:
    """Earth entity type mixin implementation class."""

    def __init__(self, lpjml):
        self.lpjml = lpjml
        self.input = self.lpjml.read_input()
        self.output = self.lpjml.read_historic_output()
        self.neighbourhood = self.lpjml.grid.get_neighbourhood()

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

    def get_cells(self, model, **kwargs):
        """get cell instances for each corresponding cell via numpy views"""
        return [model.Cell(**kwargs,
                           input=self.input.sel(cell=cell),
                           output=self.output.sel(cell=cell),
                           neighbourhood=self.neighbourhood.sel(cell=cell))
                for cell in (self.lpjml.get_cells(id=True))]

    processes = [
        Step("lpjml step",
             [I.Earth.output],
             [update, interact])
    ]
