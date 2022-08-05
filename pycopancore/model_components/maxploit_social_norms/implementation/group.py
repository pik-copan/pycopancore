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

from .... import Explicit

class Group(I.Group):
    """Define properties of maxploit_group_layer Group."""

    # process-related methods:

    def get_mean_group_opinion(self, unused_t):
        """Calculate the mean opinion of individuals in a group."""
        n = 0
        for i in self.group_members:
            if i.opinion:
                n += 1
        N = len(list(self.group_members))
        mean_group_opinion = n/N
        return mean_group_opinion

    def get_mean_group_behaviour(self, unused_t):
        """Calculate the mean behaviour of individuals in a group."""
        n = 0
        for i in self.group_members:
            if i.behaviour:
                n += 1
        N = len(list(self.group_members))
        mean_group_behaviour = n/N
        return mean_group_behaviour

    processes = [
        Explicit("mean opinion in group", [I.Group.mean_group_opinion], get_mean_group_opinion),
        Explicit("mean behaviour in group", [I.Group.mean_group_behaviour], get_mean_group_behaviour),
    ]
