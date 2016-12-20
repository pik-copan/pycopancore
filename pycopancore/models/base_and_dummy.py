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
import pycopancore.model_components.dummy as dummy

#
# Entity Types
#


class Cell (dummy.Cell, base.Cell):
    """
    Class to mix all Cell_mixins to create Cell class
    """
    pass


class Individual (base.Individual):
    """
    Class to mix all Individual_mixins to create Individual class
    """
    pass


class Society (base.Society):
    """
    Class to mix all Society_mixins to create Society class
    """
    pass

#
# Dynamics
#


class Culture(base.Culture):
    """
    Class to mix all Culture_mixins to create Culture class
    """
    pass


class Metabolism(base.Metabolism):
    """
    Class to mix all Metabolism_mixins to create Metabolism class
    """
    pass


class Nature(base.Nature):
    """
    Class to mix all Nature_mixins to create Nature class
    """
    pass

#
# Models
#


class Model(dummy.Model, base.Model):
    """
    Class to mix all Model_mixins to create Model class
    """
    name = "This model's name"
    description = "Description of the model"
    entity_types = [Cell, Individual, Society]
    process_taxa = [Culture, Metabolism, Nature]
