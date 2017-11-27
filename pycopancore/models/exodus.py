"""Model class of model Exodus."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import base  # all models must use the base component
from ..model_components import exodus as ex


class World(ex.World,
            base.World):
    """World entity type."""

    pass


class SocialSystem(ex.SocialSystem,
              base.SocialSystem):
    """SocialSystem entity type."""

    pass


class Cell(ex.Cell,
           base.Cell):
    """Cell entity type."""

    pass


class Individual(ex.Individual,
                 base.Individual):
    """Individual entity type."""

    pass


# process taxa:
class Metabolism(ex.Metabolism,
                 base.Metabolism):
    """Metabolism process taxon."""

    pass


class Culture(ex.Culture,
              base.Culture):
    """Culture process taxon."""

    pass


# Model class:

# NEED TO: list all used model components:
class Model(ex.Model,
            base.Model):
    """Class representing the whole model."""

    name = "Exodus"
    description = "Model describing rural-urban migration."

    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""
    process_taxa = [Metabolism, Culture]
    """List of process taxa used in the model"""
