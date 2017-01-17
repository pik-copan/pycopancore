# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is a template to create model modules
"""

#
#  Imports
#

import pycopancore.model_components.base as base
import pycopancore.model_components.COMPONENT as COMPONENT

#
# Entity Types
#


class Cell (base.Cell, COMPONENT.Cell):
    """
    Class to mix all Cell_mixins to create Cell class
    """
    pass


class Individual (base.Individual, COMPONENT.Individual):
    """
    Class to mix all Individual_mixins to create Individual class
    """
    pass


class Society (base.Society, COMPONENT.Society):
    """
    Class to mix all Society_mixins to create Society class
    """
    pass

#
# Dynamics
#


class Culture(base.Culture, COMPONENT.Culture):
    """
    Class to mix all Culture_mixins to create Culture class
    """
    pass


class Metabolism(base.Metabolism, COMPONENT.Metabolism):
    """
    Class to mix all Metabolism_mixins to create Metabolism class
    """
    pass


class Nature(base.Nature, COMPONENT.Nature):
    """
    Class to mix all Nature_mixins to create Nature class
    """
    pass

#
# Models
#


class Model(base.Model, COMPONENT.Model):
    """
    Class to mix all Model_mixins to create Model class
    """
    name = "This model's name"
    description = "Description of the model"
    # Make a list of all Entity Types:
    entity_types = [Cell, Individual, Society]
    # Make a list of all Process taxons/taxa:
    process_taxa = [Culture, Metabolism, Nature]