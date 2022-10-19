"""Individual entity type class for social movement growth"""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I
# from .... import master_data_model as D

# Import process types:
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
        print(f"Individual {self._uid} attempts to organize …")
        if uniform() < self.culture.organizing_success_probability:
            indifferent_inds = [
                ind for world in self.culture.worlds
                for ind in world.individuals
                if ind.engagement_level == 'indifferent']
            if indifferent_inds:
                max_degree = max(
                    self.culture.acquaintance_network.degree(
                        indifferent_inds
                        ),
                    key=lambda k:k[1]
                    )[1]
                core_candidates = [
                    ind for ind in indifferent_inds
                    if ind.culture.acquaintance_network.degree(ind)
                    == max_degree]
                other = choice(core_candidates)
                other.engagement_level = 'core'
                print(f"Individual {self._uid} wins new core member Individual {other._uid}")
        
    def mobilize(self):
        neighbors = list(self.culture.acquaintance_network.neighbors(self))
        print(f"Individual {self._uid} attempts to mobilize its neighbors Individuals", ", ".join(f'{other._uid}' for other in neighbors))
        for other in neighbors:
            if uniform() < self.culture.mobilizing_success_probability:
                if other.engagement_level == 'base':
                    print(f"Individual {self._uid} spreads the word to Individual {other._uid}")
                    other.is_mobilizing = True
                elif other.engagement_level == 'support':
                    print(f"Individual {self._uid} wins new base member Individual {other._uid}")
                    other.engagement_level = 'base'
                # TODO: maybe the following is a core super power or at least
                # it should happen with lower probabity
                elif other.engagement_level == 'indifferent':
                    print(f"Individual {self._uid} wins new support member Individual {other._uid}")
                    other.engagement_level = 'support'
        self.is_mobilizing = False

    processes = []
