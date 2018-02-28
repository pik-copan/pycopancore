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

from .... import Explicit
from .. import interface as I
from ...base import interface as B
from sympy import ITE

# from .... import master_data_model as D


class SocialSystem (I.SocialSystem):
    """SocialSystem entity type mixin implementation class."""

    processes = [
        Explicit("biomass protection due to awareness",
#                 [I.SocialSystem.protected_terrestrial_carbon_share],
#                 [B.SocialSystem.culture.max_protected_terrestrial_carbon_share
#                  * B.SocialSystem.sum(
#                        ITE(B.SocialSystem.individuals.is_environmentally_friendly,
#                            B.SocialSystem.individuals.population_share, 0.0))]
                 [I.SocialSystem.protected_terrestrial_carbon],
                 [I.SocialSystem.max_protected_terrestrial_carbon
                  * B.SocialSystem.sum(
                        ITE(B.SocialSystem.individuals.is_environmentally_friendly,
                            B.SocialSystem.individuals.population_share, 0.0))]
                 )
    ]
