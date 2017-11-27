from ... import base  # all models must use the base component

from ...model_components import copan_global_like_carbon_cycle \
    as cc


# entity types:


class World(cc.World,
            base.World):
    """World entity type."""

    pass


class SocialSystem(base.SocialSystem):
    """SocialSystem entity type."""

    pass


class Cell(cc.Cell,
           base.Cell):
    """Cell entity type."""

    pass


class Individual(base.Individual):
    """Individual entity type."""
    pass


# process taxa:


class Nature(cc.Nature,
             base.Nature):
    """Nature process taxon."""

    pass


class Metabolism(base.Metabolism):
    """Metabolism process taxon."""

    pass


class Culture (base.Culture):
    """Culture process taxon"""
    pass


# Model class:


class Model(cc.Model,
            base.Model):
    """Class representing the whole model."""

    name = "CoCCoN tutorial model, only carbon cycle"
    """Name of the model"""
    description = "(as presented at PIK in fall 2017)"
    """Longer description"""

    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""
    process_taxa = [Nature, Metabolism, Culture]
    """List of process taxa used in the model"""
