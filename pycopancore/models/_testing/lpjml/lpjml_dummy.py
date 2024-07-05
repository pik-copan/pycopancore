"""Dummy model for LPJmL coupling"""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# all models must use the base component
from .... import base
from ....model_components import lpjml as lpj
from . import other_component as other


# entity types:

class World(base.World):
    """World entity type."""
    pass

class SocialSystem(base.SocialSystem):
    """SocialSystem entity type."""
    pass

class Cell(lpj.Cell,
           other.Cell,
           base.Cell):
    """Cell entity type."""
    pass

class Individual(base.Individual):
    """Individual entity type."""
    pass


# process taxa:

class Environment(lpj.Environment,
                  base.Environment):
    """Environment process taxon."""
    pass

class Metabolism(other.Metabolism,
                 base.Metabolism):
    """Metabolism process taxon."""
    pass

class Culture(base.Culture):
    """Culture process taxon."""
    pass


# Model class:

class Model(lpj.Model,
            other.Model,
            base.Model):
    """Class representing the whole model."""

    name = "Dummy model to test LPJmL coupling"
    """Name of the model"""
    description = "Couples LPJmL component to some other component"
    """Longer description"""
    
    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""

    process_taxa = [Environment, Metabolism, Culture]
    """List of process taxa used in the model"""
