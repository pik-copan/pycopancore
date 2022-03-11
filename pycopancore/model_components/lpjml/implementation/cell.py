"""
Cell entity type mixing class template.

TODO: adjust, uncomment or fill in code and documentation wherever marked by
the "TODO" flag.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from .. import interface as I
# from .... import master_data_model as D

# TODO: uncomment this if you need ref. variables such as B.Cell.individuals:
from ...base import interface as B

# TODO: import those process types you need:
from .... import Explicit

import numpy as np

class Cell (I.Cell):
    """Cell entity type mixin implementation class."""

    # standard methods:
    # TODO: only uncomment when adding custom code inside!

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
        self.cftfrac = np.sum((np.ceil(t)-t)*self.social_system.world.environment.old_out_dict["cftfrac"][self.lpjml_grid_cell_ids] + (t-np.floor(t))*self.social_system.world.environment.out_dict["cftfrac"][self.lpjml_grid_cell_ids]) # TODO: define lpjml_cell_id, or do all cells in environment, double-think about dimensions and units
    
    def write_landuse(self, unused_t):
        for i in self.lpjml_grid_cell_ids:
            self.environment.in_dict["landuse"][i] = self.landuse # TODO: move to environment loop because we don't need to do this continuosly

    # TODO: add some if needed...

    processes = [
        Explicit("cftfrac",
                 [I.Cell.cftfrac],
                 read_cftfrac),
        Explicit("landuse",
                 [B.Cell.environment.in_dict],
                 write_landuse)
        ]# TODO: instantiate and list process objects here
