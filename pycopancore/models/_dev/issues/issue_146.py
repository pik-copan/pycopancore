"""minimal model without odes."""

from .... import base  # all models must use the base component

from ....model_components import voting_on_climate_policy \
    as vote

# entity types:


class World(base.World):
    """World entity type."""
    pass


class SocialSystem(vote.SocialSystem,
                   base.SocialSystem):
    """SocialSystem entity type."""
    pass


class Cell(base.Cell):
    """Cell entity type."""
    pass


class Individual(vote.Individual,
                 base.Individual):
    """Individual entity type."""
    pass


# process taxa:


class Environment(base.Environment):
    """Environment process taxon."""
    pass


class Metabolism(base.Metabolism):
    """Metabolism process taxon."""
    pass


class Culture (base.Culture):
    """Culture process taxon"""
    pass


# Model class:


class Model(vote.Model,
            base.Model):
    """Class representing the whole model."""

    name = "Jobst's prototype 1"
    """Name of the model"""
    description = "(as presented internally at PIK in fall 2016)"
    """Longer description"""

    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""
    process_taxa = [Environment, Metabolism, Culture]
    """List of process taxa used in the model"""
