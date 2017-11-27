"""SocialSystem entity type mixing class template.

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
from .... import Event
from numpy import array
from numpy.random import uniform

class SocialSystem (I.SocialSystem):
    """SocialSystem entity type mixin implementation class."""

    voting_time_offset = None
    
    def next_voting_time(self, t):
        if not self.voting_time_offset:
            self.voting_time_offset = uniform() * self.time_between_votes
        return (self.voting_time_offset 
                + self.time_between_votes
                * ((t - self.voting_time_offset + 1e-10) // self.time_between_votes 
                   + 1)) 
    
    def take_a_vote(self, unused_t):
        share = sum([i.population_share for i in self.individuals
                     if i.is_environmentally_friendly])
        self.has_renewable_subsidy = (
            (share > self.renewable_subsidy_intro_threshold)
                if not self.has_renewable_subsidy
            else (share > self.renewable_subsidy_keeping_threshold))
        self.has_emissions_tax = (
            (share > self.emissions_tax_intro_threshold)
                if not self.has_emissions_tax
            else (share > self.emissions_tax_keeping_threshold))
        self.has_fossil_ban = (
            (share > self.fossil_ban_intro_threshold)
                if not self.has_fossil_ban
            else (share > self.fossil_ban_keeping_threshold))

    processes = [
        Event("voting",
              [I.SocialSystem.has_renewable_subsidy,
               I.SocialSystem.has_emissions_tax,
               I.SocialSystem.has_fossil_ban],
              ["time", next_voting_time, take_a_vote])
    ]
