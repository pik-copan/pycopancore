"""Template to create model class modules."""
# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
#  Imports
#

import pycopancore.model_components.base as base
import pycopancore.model_components.COMPONENT as COMPONENT

#
# Entity Types
#


class Cell (COMPONENT.Cell, base.Cell):
    """Define Class by mixing all Cell_mixins to create Cell class."""

    pass


class Individual (COMPONENT.Individual, base.Individual):
    """Define Class by mixing all Individual_mixins to create Individual class.

    Always put base.Individual last.
    """

    pass


class Society (COMPONENT.Society, base.Society):
    """Define Class by mixing all Society_mixins to create Society class.

    Always put base.Society last.
    """

    pass

#
# Dynamics
#


class Culture(COMPONENT.Culture, base.Culture):
    """Define Class by mixing all Culture_mixins to create Culture class.

    Always put base.Culture last.
    """

    pass


class Metabolism(COMPONENT.Metabolism, base.Metabolism):
    """Define Class by mixing all Metabolism_mixins to create Metabolism class.

    Always put base.Metabolism last.
    """

    pass


class Nature(COMPONENT.Nature, base.Nature):
    """Define Class by mixing all Nature_mixins to create Nature class.

    Always put base.Nature last.
    """

    pass

#
# Models
#


class Model(base.Model, COMPONENT.Model):
    """Define Model Class by mixing all Model_mixins."""

    name = "This model's name"
    description = "Description of the model"
    # Make a list of all Entity Types:
    entity_types = [Cell, Individual, Society]
    # Make a list of all Process taxons/taxa:
    process_taxa = [Culture, Metabolism, Nature]
