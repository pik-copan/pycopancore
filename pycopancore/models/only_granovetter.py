"""simple Granovetter test"""

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

from .. import base  # all models must use the base component

from ..model_components import granovetter_social_dynamics \
    as gv

# entity types:


class World(
            # prod.World,
            base.World):
    """World entity type."""

    pass


class SocialSystem(base.SocialSystem):
              # prod.SocialSystem,
              # growth.SocialSystem):
    """SocialSystem entity type."""

    pass


class Cell(
           # prod.Cell,
           base.Cell):
    """Cell entity type."""

    pass

class Individual (gv.Individual,
                  base.Individual):
   """Individual entity type."""

   pass


# process taxa:


class Environment(
             base.Environment):
    """Environment process taxon."""

    pass


class Metabolism(base.Metabolism):
                # , prod.Metabolism):
    """Metabolism process taxon."""

    pass

class Culture (gv.Culture,
              base.Culture):
   """Culture process taxon."""

   pass


# Model class:


class Model(gv.Model,
            # prod.Model,
            # growth.Model,
            base.Model):
    """Class representing the whole model."""

    name = "Leander's granovetter prototype"
    """Name of the model"""
    description = "to test network dynamics first"
    """Longer description"""

    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""
    process_taxa = [Environment, Metabolism, Culture]
    """List of process taxa used in the model"""
