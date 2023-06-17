"""The reg decision making.world class.

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

from .. import interface as I
from random import sample


class World (I.World):
    """Define properties.
    Inherits from I.World as the interface with all necessary variables
    and parameters.
    """

    def __init__(self,
                 **kwargs
                 ):
        """Initialize an instance of World.
        Parameters
        ----------
        agent_list
        """
        super(World, self).__init__(**kwargs)

    processes = []

    def init_farmers(self, model, **kwargs):
        cells = self.init_cells(model, **kwargs)
        crop_idx = [
            i for i, item in enumerate(self.output.hdate.band.values)
            if any(x in item for x in self.lpjml.config.cftmap)
        ]
        farmers = []
        for cell in cells:
            if cell.output.cftfrac.sum("band") == 0:
                continue
            avg_hdate = np.average(
                cell.output.hdate,
                weights=cell.output.cftfrac.isel(band=crop_idx)
            )
            farmer = model.Individual(
                cell=cell,
                copan_config=self.lpjml.config.coupled_config,
                hdate=avg_hdate,
                **kwargs
            )
            farmers.append(farmer)

        farmers_sorted = sorted(farmers, key=lambda farmer: farmer.hdate)

        return farmers_sorted
