"""Base model module.

It only import components of the base mixins
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

#
#  Imports
#

import pycopancore.model_components.base as base

#
# Entity Types
#


class World(base.World):
    """Class to mix all World_mixins to create World clas."""

    pass


class Cell(base.Cell):
    """Class to mix all Cell_mixins to create Cell class."""

    pass


class Individual(base.Individual):
    """Class to mix all Individual_mixins to create Individual class."""

    pass


class SocialSystem(base.SocialSystem):
    """Class to mix all SocialSystem_mixins to create SocialSystem class."""

    pass

#
# Dynamics
#


class Culture(base.Culture):
    """Class to mix all Culture_mixins to create Culture class."""

    pass


class Metabolism(base.Metabolism):
    """Class to mix all Metabolism_mixins to create Metabolism class."""

    pass


class Environment(base.Environment):
    """Class to mix all Environment_mixins to create Environment class."""

    pass

#
# Models
#


class Model(base.Model):
    """Class to mix all Model_mixins to create Model class."""

    name = "Base Only"
    description = "Model to test Framwork and base-modules"
