"""Other model component to test LPJmL coupling"""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from .... import master_data_model as D
from ....model_components.lpjml import interface as L
from ....model_components.base import interface as B
from .... import Variable
from .... import Event

import numpy as np
from numpy.random import exponential, uniform

# INTERFACE

class ICell (object):
    # landuse = L.Cell.landuse
    # TODO is with_tillage really to be found in L.Cell?
    with_tillage = L.Cell.with_tillage
    cftfrac = L.Cell.cftfrac
    
class IMetabolism (object):
    # TODO check which rate is more fitting: once a year or multiple?
    # landuse_update_rate = Variable(
        # "landuse update rate",
        # """average number of time points per time where some cells
        # update their landuse""",
        # unit = D.years**(-1), 
        # default = 5 / D.years, lower_bound = 0)
    landuse_update_rate = Variable(
        "landuse update rate",
        """average number of time points per time where some cells
        update their landuse""",
        unit = D.unity,
        default = 1)
    landuse_update_prob = Variable(
        "fishing effort update probability",
        """probability that an individual updates their fishing effort at
        an update time point""",
        unit = D.unity,
        default = 1/2, lower_bound = 0, upper_bound = 1)


class IModel (object):
    name = "other component"
    description = "only for testing lpjml coupling"
    requires = []
            
class interface:
    Cell = ICell
    Metabolism = IMetabolism
    Model = IModel

# IMPLEMENTATION:

class Cell (ICell):
    
    def update_landuse(self, unused_t):
        # self.landuse = np.ones((1, 64))
        self.with_tillage = np.ones((1, 1))
    processes = []

class Metabolism (IMetabolism):
    def next_landuse_update_time(self, t):
        return t + exponential(1 / self.landuse_update_rate)


    def update_landuse(self, unused_t):
        for w in self.worlds:
            for c in w.cells:
                if uniform() < self.landuse_update_prob:
                    c.update_landuse(unused_t)

    processes = [
        Event("update landuse",
              # [B.Metabolism.worlds.cells.landuse],
              [B.Metabolism.worlds.cells.with_tillage],
              ["time",
              next_landuse_update_time,
              update_landuse])]

class Model (IModel):
    entity_types = [Cell]
    process_taxa = [Metabolism]
