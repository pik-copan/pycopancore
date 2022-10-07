"""Group entity type of the component maxploit_group_layer."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from ...base import interface as B

from .. import interface as I
import numpy as np
from numpy.random import exponential, uniform

from .... import Explicit, Step

class Group(I.Group):
    """Define properties of maxploit_group_layer Group."""

    # process-related methods:

    def next_group_meeting_time(self, t):
        """Get the next meeting time"""
        return t + self.group_meeting_interval

    def update_group_opinion(self, unused_t):
        """Update a groups opinion based on the mean_group_behaviour."""
        if self.mean_group_behaviour <= self.culture.majority_threshold: # get the mean in terms of true/false for adjusting the global opinion later
            mean_group_opinion_binary = 0
        else:
            mean_group_opinion_binary = 1

        for g in self.world.groups:
            if uniform() <= self.group_update_probability: #groups consider updating only with certain probability
                if self.group_opinion != mean_group_opinion_binary:
                    if self.mean_group_behaviour > self.culture.majority_threshold or\
                            self.mean_group_behaviour < (1-self.culture.majority_threshold): # defines an interval to allow switching in both directions
                        self.group_opinion = mean_group_opinion_binary # switch group_opinion

    def get_mean_group_opinion(self, unused_t):
        """Calculate the mean opinion of individuals in a group."""
        n = 0
        for i in self.group_members:
            if i.opinion:
                n += 1
        N = len(list(self.group_members))
        self.mean_group_opinion = n/N

    def get_mean_group_behaviour(self, unused_t):
        """Calculate the mean behaviour of individuals in a group."""

        n = 0
        for i in self.group_members:
            if i.behaviour:
                n += 1
        N = len(list(self.group_members))
        self.mean_group_behaviour = n/N

    processes = [
        # Explicit("mean opinion in group", [I.Group.mean_group_opinion], get_mean_group_opinion),
        # Explicit("mean behaviour in group", [I.Group.mean_group_behaviour], get_mean_group_behaviour),
        # Step("update group opinion",
        #       [I.Group.group_opinion],
        #       [next_group_meeting_time,
        #        update_group_opinion])
    ]
