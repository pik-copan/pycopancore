from ... import base  # all models must use the base component

from ...model_components import copan_global_like_carbon_cycle \
    as cc
from ...model_components import copan_global_like_production \
    as prod
from ...model_components import copan_global_like_economic_growth \
    as growth
from ...model_components import copan_global_like_population_growth \
    as pop
from ...model_components import wellbeing_driven_migration \
    as mig
from ...model_components import environmental_awareness \
    as aware
from ...model_components import social_learning_of_environmental_friendliness \
    as learn
from ...model_components import voting_on_climate_policy \
    as vote


# entity types:


class World(cc.World,
            prod.World,
            growth.World,
            base.World):
    """World entity type."""

    pass


class SocialSystem(
              prod.SocialSystem,
              growth.SocialSystem,
              pop.SocialSystem,
              mig.SocialSystem,
              aware.SocialSystem,
              vote.SocialSystem,
              base.SocialSystem):
    """SocialSystem entity type."""

    pass


class Cell(cc.Cell,
           prod.Cell,
           base.Cell):
    """Cell entity type."""

    pass


class Individual(
                 aware.Individual,
                 learn.Individual,
                 base.Individual):
    """Individual entity type."""
    pass


# process taxa:


class Nature(cc.Nature,
             base.Nature):
    """Nature process taxon."""

    pass


class Metabolism(
                 prod.Metabolism,
                 growth.Metabolism,
                 pop.Metabolism,
                 mig.Metabolism,
                 base.Metabolism):
    """Metabolism process taxon."""

    pass


class Culture (
               aware.Culture,
               learn.Culture,
               base.Culture):
    """Culture process taxon"""
    pass


# Model class:


class Model(cc.Model,
            prod.Model,
            growth.Model,
            pop.Model,
            mig.Model,
            aware.Model,
            learn.Model,
            vote.Model,
            base.Model):
    """Class representing the whole model."""

    name = "CoCCoN tutorial model"
    """Name of the model"""
    description = "(as presented at PIK in fall 2017)"
    """Longer description"""

    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""
    process_taxa = [Nature, Metabolism, Culture]
    """List of process taxa used in the model"""
