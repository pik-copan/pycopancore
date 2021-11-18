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
from numpy import inf
from numpy.random import exponential

# TODO: uncomment this if you need ref. variables such as B.Culture.individuals:
from ...base import interface as B

# TODO: import those process types you need:
from .... import Explicit, Event

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

    def next_activity_update_time(self, t):
        """time of next activity update"""
        return (inf if self.activity_update_rate == 0
                else t + exponential(1. / self.activity_update_rate))

    def update_individuals_activity(self, t):
        """let some individuals update their activity"""
        for w in self.worlds:
            for i in w.individuals:
                if i.is_influencable:
                    i.update_activity(t)
    
    def set_number_of_active_individuals(self, unused_t):
        """get the number of active individuals"""
        # JH: the following does not work since you are attempting to use a symbolic expression (B.Culture.worlds.individuals) in a method.
        # symbolic expressions are only allowed when specifying formulae directly in processes = [...], not in methods.
        # Technically, B.Culture.worlds.individuals is not a value but an abstract object of class _DotConstruct, representing a variable.
        # Instead, you need to access the variable values directly as follows (note the 'self'!):
#        self.number_of_active_individuals = sum([ind.is_active for ind in [B.Culture.worlds.individuals]]) # ATTENTION: only works if we have one world I think
        self.number_of_active_individuals = sum([ind.is_active for w in self.worlds for ind in w.individuals]) # ATTENTION: only works if we have one world I think
        # (alternatively, you could have specified the whole process with a symbolic expression as indicated below)
        print(self.number_of_active_individuals)

    processes = [
                 Explicit("update number of active individuals",
                          [I.Culture.number_of_active_individuals],
                          # JH: your original specification, using a method:
                          set_number_of_active_individuals
                          # JH: equivalent and simpler specification, using a symbolic expression:
                          #[B.Culture.worlds.individuals.sum.is_active]
                          ),
                 Event("update individuals' activity",
                       [B.Culture.worlds.individuals.is_active],
                       ["time",
                        next_activity_update_time,
                        update_individuals_activity]
                       )
                 ]
