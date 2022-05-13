"""Culture process taxon mixing class template.

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

# TODO: uncomment this if you need ref. variables such as B.Culture.individuals:
from ...base import interface as B

# TODO: import those process types you need:
from .... import Event

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
        return t + exponential(1 / self.meeting_rate)

    def do_meeting(self, unused_t):
        """In the current setup, each core member decides individually wether
        to organize or mobilize, another option could be to let all core
        members focus on the same task
        """
        for w in self.worlds:
            for i in w.individuals:
                i.is_mobilizing = False
                if i.engagement_level == 'core':
                    if uniform() < self.growth_strategy:
                        print("organizing …")
                        i.organize()
                    elif uniform() > self.growth_strategy:
                        print("mobilizing …")
                        i.is_mobilizing = True

    processes = [
        Event("do meeting",
              [B.Culture.worlds.individuals.engagement_level],
              ["time",
               next_meeting_time,
               do_meeting
               ]
              )
        ]  # TODO: instantiate and list process objects here
