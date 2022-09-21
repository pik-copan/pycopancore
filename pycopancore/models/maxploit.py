"""
Exploit model.

The exploit model is including the modules base,
most_simple_vegetation, simple_extraction
and exploit_simple_learning.
It is based on the cython implementation cyexploit
(see https://github.com/wbarfuss/cyexploit )
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

#
#  Imports
#

import pycopancore.model_components.base as base
import pycopancore.model_components.maxploit_most_simple_vegetation as vegetation
import pycopancore.model_components.maxploit_simple_extraction as extraction
# import pycopancore.model_components.maxploit_individual_layer as individual_layer
import pycopancore.model_components.maxploit_social_norms as social_norms

#
#  Entity Types
#


class World(base.World):
    """Class to mix all World_mixins to create World class."""

    pass


class SocialSystem(base.SocialSystem):
    """Class to mix all SocialSystem_mixins to create SocialSystem class."""

    pass


class Cell(vegetation.Cell,
           extraction.Cell,
           base.Cell):
    """Class to mix all Cell_mixins to create Cell class."""

    pass


# Order is important: extraction.Individual before individual_layer.Individual
# because of the get_harvest_rate() method that should be overwritten.
class Individual(extraction.Individual,
                 social_norms.Individual,
                 base.Individual):
    """Class to mix all Individual_mixins to create Individual class."""

    pass

class Group(social_norms.Group,
            base.Group):

    """Class to mix all Group_mixins to create Group class."""

    pass

#
#  Dynamics
#


class Culture(social_norms.Culture,
              base.Culture):
    """Class to mix all Culture_mixins to create Culture class."""

    pass

#
# Models
#


class Model(vegetation.Model,
            extraction.Model,
            social_norms.Model,
            base.Model):
    """Class to mix all Model_mixins to create Model class."""

    name = "Maxploit model"
    description = "COPAN:Maxploit model"

    entity_types = [World, SocialSystem, Cell, Individual, Group]
    process_taxa = [Culture]
