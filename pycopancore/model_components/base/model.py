"""base component's Model component mixin class and essential framework logics.

This class is the Model component mixin of the base model component and also
owns the configure method. This method is central to the framework since it
fuses together the used classes and puts information about process types and
variables in special list to be accessed by the runner.
"""

# TODO: for clarity, move framework logics into separate class this class
# inherits from

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .model_logics import ModelLogics  # only in base component

from .. import abstract
from . import interface as I
from . import World, Cell, Nature, Individual, Culture, Society, \
    Metabolism


class Model (I.Model, abstract.Model, ModelLogics):
    """base model component mixin class.

    This is the base.model file. It serves two purposes:
    1. Be a the model class of the base component, providing the information
    about which mixins are to be used of the component AND:
    2. Provide the configure method.
    The configure method has a very central role in the COPAN:core framework,
    it is called before letting run a model. It then searches which model class
    is used from the model module. It will then go through all components
    listed there and collect all variables and processes of said components.
    """

    entity_types = [World, Cell, Individual, Society]
    process_taxa = [Nature, Culture, Metabolism]
