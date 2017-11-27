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
from .... import Explicit
import sympy as sp
import random


class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 impact_scaling_factor=5,
                 no_impact_atmospheric_carbon_level=0.15,
                 no_impact_opinion_change=0.5,
                 **kwargs):
        """Initialize the unique instance of Culture."""
        super().__init__(**kwargs)  # must be the first line

        self.impact_scaling_factor = impact_scaling_factor
        self.no_impact_atmospheric_carbon_level = no_impact_atmospheric_carbon_level
        self.no_impact_opinion_change = no_impact_opinion_change

    # process-related methods:
    def opinion_change_function(self, x, y):
        if self.impact > 0:
            _opinion_change_to_awareness = self.no_impact_opinion_change + (1 - self.no_impact_opinion_change) \
                * (1 - sp.exp(- self.impact))
            if x.opinion == 0 and y.opinion == 1:
                return random.random() < _opinion_change_to_awareness
            elif x.opinion == 1 and y.opinion == 0:
                return random.random() < (1 - _opinion_change_to_awareness)
        else:
            return random.random() < self.no_impact_opinion_change

    def set_opinion_change(self, t):
        self.opinion_change = \
            self.opinion_change_function

    processes = [

        Explicit(
            "atmospheric carbon impact",
            [I.Culture.impact],
            [I.Culture.impact_scaling_factor
             * (I.World.atmospheric_carbon - I.Culture.no_impact_atmospheric_carbon_level)]
        ),

        Explicit("set probability of opinion adoption",
                 [I.Culture.opinion_change],
                 set_opinion_change)
    ]  # TODO: instantiate and list process objects here
