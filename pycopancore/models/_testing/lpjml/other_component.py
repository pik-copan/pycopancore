from .... import master_data_model as D
from .lpjml import interface as L
from .... import Variable
from .... import Explicit

import numpy as np

# INTERFACE

class ICell (object):
    landuse = L.Cell.landuse
    cftfrac = L.Cell.cftfrac
    
class IEnvironment (object):
    landuse_update_rate = Variable(
        "landuse update rate",
        """average number of time points per time where some cells
        update their landuse""",
        unit = D.years**(-1), 
        default = 5 / D.years, lower_bound = 0)
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
    Environment = IEnvironment
    Model = IModel

# IMPLEMENTATION:

class Cell (ICell):
    
    def update_landuse(self, unused_t):
        self.landuse = self.cftfrac * self.landuse
    processes = []

class Environment (IEnvironment):
    def next_landuse_update_time(self, t):
        return t + exponential(1 / self.landuse_update_rate)

    def update_landuse(self, unused_t):
        for w in self.worlds:
            for c in w.cells:
                if uniform() < self.landuse_update_prob:
                    c.update_landuse()

    processes = [
        Event("update fishing efforts",
               [B.Environment.worlds.individuals.landuse],
               ["time",
                next_landuse_update_time,
                update_landuse])

class Model (IModel):
    entity_types = [Cell]
    process_taxa = [Environment]
