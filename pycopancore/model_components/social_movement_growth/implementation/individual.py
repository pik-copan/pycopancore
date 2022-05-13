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
# from .... import master_data_model as D

# TODO: uncomment this if you need ref. variables such as B.Individual.cell:
# from ...base import interface as B

# TODO: import those process types you need:
from .... import Event

from numpy.random import choice, uniform, exponential

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

    # process-related methods:

    def organize(self):
        if uniform() < self.culture.organizing_success_probability:
            inactive_inds = [ind for world in self.culture.worlds for ind in world.individuals if ind.engagement_level == 'inactive']
            if inactive_inds:
                print("winning a new core member")
                max_degree = max(self.culture.acquaintance_network.degree(inactive_inds), key=lambda k:k[1])[1]
                core_candidates = [ind for ind in inactive_inds if ind.culture.acquaintance_network.degree(ind) == max_degree]
                other = choice(core_candidates)
                other.engagement_level = 'core'
                print(other.culture.acquaintance_network.degree(other))
    
    def next_interaction_time(self, t):
        return t + exponential(1 / self.interaction_rate)
        
    def mobilize(self, unused_t):
        if self.is_mobilizing:
            for other in list(self.culture.acquaintance_network.neighbors(self)):
                if uniform() < self.culture.mobilizing_success_probability:
                    if other.engagement_level == 'base':
                        print("spreading the word")
                        other.is_mobilizing = True
                    elif other.engagement_level == 'support':
                        print("winning a new base member")
                        other.engagement_level = 'base'
            self.is_mobilizing = False

    processes = [
        Event("do interaction",
              [I.Individual.is_mobilizing, I.Individual.engagement_level],
              ["time",
               next_interaction_time,
               mobilize
               ]
              )
        ]
