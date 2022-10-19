"""Culture process taxon mixing class for social movement growth"""

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

# import reference variables from the base component:
from ...base import interface as B

# import process types:
from .... import Step

from numpy.random import exponential, choice, uniform

class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:
    # TODO: only uncomment when adding custom code!

#     def __init__(self,
#                  # *,  # TODO: uncomment when adding named args behind here
#                  **kwargs):
#         """Initialize the unique instance of Culture."""
#         super().__init__(**kwargs)  # must be the first line
#         # TODO: add custom code here:
#         pass

    # process-related methods:
    def next_meeting_time(self, t):
        return t + 1/self.meeting_rate
    
    def next_interaction_time(self, t):
        return t + 1/self.interaction_rate

    def do_meeting(self, unused_t):
        """In the current setup, each core member decides individually
        wether to organize or mobilize, another option could be to let
        all core members focus on the same task
        """
        for w in self.worlds:
            for i in w.individuals:
                i.is_mobilizing = False
            for i in w.individuals:
                if i.engagement_level == 'core':
                    if uniform() < self.growth_strategy:
                        print(f"Individual {i._uid} is going to spend its time organizing.")
                        i.organize()
                    else:
                        print(f"Individual {i._uid} is going to spend its time mobilizing.")
                        i.mobilize()
    
    def do_interaction(self, unused_t):
        """Have each mobilizing individual spread the word to their 
        neighbors or attempt to mobilize them
        """
        for w in self.worlds:
            for i in w.individuals:
                if i.is_mobilizing == True:
                    i.mobilize()

    processes = [
        Step("do meeting",
              [B.Culture.worlds.individuals.engagement_level],
              [next_meeting_time,
               do_meeting
               ]
              ),
        Step("do interaction",
              [B.Culture.worlds.individuals.is_mobilizing, B.Culture.worlds.individuals.engagement_level],
              [next_interaction_time,
               do_interaction
               ]
              )
        ]
