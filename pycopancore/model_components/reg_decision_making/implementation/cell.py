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
import numpy as np
# from .... import master_data_model as D

# TODO: uncomment this if you need ref. variables such as B.Cell.individuals:
# from ...base import interface as B

# TODO: import those process types you need:
# from .... import Explicit, ODE, Event, Step


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

    # TODO "import" coupler component
    # TODO: check how to connecto to LPJmL cells
    def get_yield():
        # import "outputs variable" from CORE-coupler side and split into
        # yields and soil by accessing keys ["pft_harvestc"] ect.
        crop_yield = 2
        return crop_yield

    def get_soil_carbon():
        soil_carbon = 1
        return soil_carbon
    
    landuse_decisions = np.array

    # lpjml_cell_id = Variable('lpjml cell id', 'given by lpjml')
    # in case we want to use different cells than the ones from lpjml
    # core_cell_id = Variable('core cell id', 'lpjml cell mapped to core')

    processes = []  # TODO: instantiate and list process objects here
