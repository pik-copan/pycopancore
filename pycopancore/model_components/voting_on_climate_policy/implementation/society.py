"""Society entity type mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
# from .... import master_data_model as D
from .... import Event
from numpy import array

class Society (I.Society):
    """Society entity type mixin implementation class."""

    def next_voting_time(self, t):
        return t + self.time_between_votes
    
    def take_a_vote(self, unused_t):
        share = sum([i.population_share for i in self.individuals
                     if i.is_environmentally_friendly])
        self.has_renewable_subsidy = (share > self.renewable_subsidy_threshold)
        self.has_emissions_tax = (share > self.emissions_tax_threshold)
        self.has_fossil_ban = (share > self.fossil_ban_threshold)

    processes = [
        Event("voting",
              [I.Society.has_renewable_subsidy,
               I.Society.has_emissions_tax,
               I.Society.has_fossil_ban],
              [next_voting_time, take_a_vote])
    ]
