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

from .... import Explicit
from .. import interface as I
from ...base import interface as B
from sympy import ITE

# from .... import master_data_model as D


class Society (I.Society):
    """Society entity type mixin implementation class."""

    processes = [
        Explicit("biomass protection due to awareness",
#                 [I.Society.protected_terrestrial_carbon_share],
#                 [B.Society.culture.max_protected_terrestrial_carbon_share
#                  * B.Society.sum(
#                        ITE(B.Society.individuals.is_environmentally_friendly,
#                            B.Society.individuals.population_share, 0.0))]
                 [I.Society.protected_terrestrial_carbon],
                 [I.Society.max_protected_terrestrial_carbon
                  * B.Society.sum(
                        ITE(B.Society.individuals.is_environmentally_friendly,
                            B.Society.individuals.population_share, 0.0))]
                 )
    ]
