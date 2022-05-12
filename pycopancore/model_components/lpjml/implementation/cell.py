"""Cell entity for LPJmL coupling component."""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from .. import interface as I
from ...base import interface as B

from .... import Explicit

import numpy as np

class Cell (I.Cell):
    """Cell entity type mixin implementation class."""

    # standard methods:
    # TODO: only uncomment when adding custom code inside!
    # NOTE: This can be used for initial coupling!

#     def __init__(self,
#                  # *,  # TODO: uncomment when adding named args behind here
#                  **kwargs):
#         """Initialize an instance of Cell."""
#         super().__init__(**kwargs)  # must be the first line
#         # TODO: add custom code here:
#         pass
# 
#     def deactivate(self):
#         """Deactivate a Cell."""
#         # TODO: add custom code here:
#         pass
#         super().deactivate()  # must be the last line
# 
#     def reactivate(self):
#         """Reactivate a Cell."""
#         super().reactivate()  # must be the first line
#         # TODO: add custom code here:
#         pass

    # process-related methods:
    def read_cftfrac(self, t):
        self.cftfrac = np.sum((np.ceil(t)-t)*self.social_system.world.environment.old_out_dict["cftfrac"][self.lpjml_grid_cell_ids] + (t-np.floor(t))*self.social_system.world.environment.out_dict["cftfrac"][self.lpjml_grid_cell_ids]) # extrapolation over the year and summation over grid cells
        # TODO: define lpjml_cell_ids, or do all cells in environment, double-think about dimensions, units and the points in time our data is about
    
    # TODO: if possible (and reasonable), make one method that loops over all keys (output variables) and reads them into the corresponding CORE variables
    
    def write_landuse(self, unused_t):
        for i in self.lpjml_grid_cell_ids:
            # self.environment.in_dict["landuse"][i] = self.landuse # TODO: move to become an environment step process because we only need to write this once a year
            self.environment.in_dict["with_tillage"][i] = self.with_tillage # TODO: move to become an environment step process because we only need to write this once a year


    processes = [
        Explicit("cftfrac",
                 [I.Cell.cftfrac],
                 read_cftfrac),
        # Explicit("landuse",
                 # [B.Cell.environment.in_dict],
                 # write_landuse)'''
        Explicit("with_tillage",
                 [B.Cell.environment.in_dict],
                 write_landuse)
        ]