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

    def mean_group_opinion(self):
        """Calculate the mean opinion of individuals in a group."""
        N = 0
        n = 0
        for N, i in enumerate(B.Group.group_members):
            if i.opinion:
                n += 1
        mean_opinion = n/N
        return mean_opinion

    processes = [
        Explicit("mean opinion in group", [I.Group.mean_group_opinion], mean_group_opinion)
    ]
