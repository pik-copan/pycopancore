"""Individual entity type class template.

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
import numpy as np
# from .... import master_data_model as D

# TODO: uncomment this if you need ref. variables such as B.Individual.cell:
#from ...base import interface as B

# TODO: import those process types you need:
# from .... import Explicit, ODE, Event, Step

class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    # aufgeführt: alle allgemeinen parameter, und AFT-spezifische parameter
    # für den "traditionalist" type
    def __init__(self,
                 *,  # TODO: how to assign AFT to individual?
                 aft = 1,
                 behaviour = 0,
                 past_behaviour = 0,
                 attitude = 0,
                 subjective_norm = 0,  #TODO maybe adapt this name or check in culture
                 pbc = 0,
                 average_waiting_time = 1,

                # TODO implement weights in a way that makes sure they add up to 1
                   w_trad_attitude = 1/2,
                   w_trad_yield = 2/3,
                   w_trad_soil = 1/3,
                   w_trad_norm = 1/2,
                   trad_pbc = 1/2,
                   w_trad_social_learning = 1/2,
                   w_sust_social_learning = 1/2,
                   w_trad_own_land = 1/2,
                   w_sust_own_land = 1/2,
                   w_sust_attitude = 2/3,
                   w_sust_yield = 1/3,
                   w_sust_soil = 2/3,
                   w_sust_norm = 1/3,
                   sust_pbc = 1/2,
                   # how to bring diff pbc vals to AFTs? 
                   # in all other cases, weighting was necessary because one had
                   # 2 values (i.e., soil and yield), hw to do this now as it
                   # is just a parameter to multiply?

                  **kwargs):
         """Initialize an instance of Individual."""
         super().__init__(**kwargs)  # must be the first line
         self.aft = aft
         self.behaviour = behaviour
         self.past_behaviour = past_behaviour
         self.attitude = attitude
         self.subjective_norm = subjective_norm
         self.pbc = pbc
         self.average_waiting_time = average_waiting_time
         
         # trad and sust aft
         self.w_social_learning = [w_trad_social_learning,
                                   w_sust_social_learning]
         self.w_own_land = [w_trad_own_land, w_sust_own_land]
         self.w_attitude = [w_trad_attitude, w_sust_attitude]
         self.w_yield = [w_trad_yield, w_sust_yield]
         self.w_soil = [w_trad_soil, w_sust_soil]
         self.w_norm = [w_trad_norm, w_sust_norm]
         self.pbc = [trad_pbc, sust_pbc]
         self.update_time = np.random.exponential(self.average_waiting_time)

         pass

    def __lt__(self, other):
        """Make objects sortable."""
        return self._uid < other._uid

    def deactivate(self):
        """Deactivate an Individual."""
        # TODO: add custom code here:
        pass
        super().deactivate()  # must be the last line
 
    def reactivate(self):
        """Reactivate an Individual."""
        super().reactivate()  # must be the first line
        # TODO: add custom code here:
        pass

    # process-related methods:
    # TODO: how to do this for the two AFTs?
    def get_behaviour(self):
        """compute a random farming behaviour of individual"""
        return np.random.rand()

    processes = []  # TODO: instantiate and list process objects here
