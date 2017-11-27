# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

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


class Environment(cc.Environment,
             base.Environment):
    """Environment process taxon."""

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
    process_taxa = [Environment, Metabolism, Culture]
    """List of process taxa used in the model"""
