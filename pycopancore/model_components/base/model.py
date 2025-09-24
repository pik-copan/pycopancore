"""base component's Model component mixin class and essential framework logics.

This class is the Model component mixin of the base model component and also
derives from ModelLogics.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import abstract
from . import interface
from . import (
    Cell,
    Culture,
    Environment,
    Group,
    Individual,
    Metabolism,
    SocialSystem,
    World,
)

# import essential framework logics
# (this import occurs ONLY in the base component):
from .model_logics import ModelLogics


class Model(interface.Model, abstract.Model, ModelLogics):
    """base model component mixin class.

    This is the base.Model class. It serves two purposes:
    1. Be the model class of the base component, providing the information
    about which mixins are to be used of the component AND:
    2. Provide the configure method via the parent class ModelLogics.
    """

    # specify entity types and process taxon classes
    # defined in the base component:
    entity_types = [World, Cell, Individual, SocialSystem, Group]
    process_taxa = [Environment, Culture, Metabolism]
