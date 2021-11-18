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
from numpy.random import uniform
# from .... import master_data_model as D

# TODO: uncomment this if you need ref. variables such as B.Individual.cell:
from ...base import interface as B

# TODO: import those process types you need:
from .... import Explicit

class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:
    # TODO: only uncomment when adding custom code!

#     def __init__(self,
#                  # *,  # TODO: uncomment when adding named args behind here
#                  **kwargs):
#         """Initialize an instance of Individual."""
#         super().__init__(**kwargs)  # must be the first line
#         # TODO: add custom code here:
#         pass
# 
#     def deactivate(self):
#         """Deactivate an Individual."""
#         # TODO: add custom code here:
#         pass
#         super().deactivate()  # must be the last line
# 
#     def reactivate(self):
#         """Reactivate an Individual."""
#         super().reactivate()  # must be the first line
#         # TODO: add custom code here:
#         pass

    def set_share_of_active_neighbors(self, unused_t):
        self.share_of_active_neighbors = sum([other.is_active for other in self.culture.acquaintance_network.neighbors(self)]) / self.culture.acquaintance_network.degree(self)
    
    def update_activity(self, unused_t):
        """stochastically change activity status.
        
        This method is called by Culture's activity updating process
        """
        if len(list(self.culture.acquaintance_network.neighbors(self))) > 0:
            r = uniform()
            if self.is_active:
                if self.share_of_active_neighbors < self.deactivation_threshold:
                    if r < self.deactivation_probability:
                        self.is_active = False
            else:
                if self.share_of_active_neighbors > self.activation_threshold:
                    if r < self.activation_probability:
                        self.is_active = True
    
    # process-related methods:
    processes = [
                 Explicit("share of active neighbors",
                          [I.Individual.share_of_active_neighbors],
                          set_share_of_active_neighbors
                          )
                 ]
    # NOTE: Explicit is called before others, right?
