"""Interface module for the simple_extraction module."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore import Variable


class Cell(object):
    """Interface for Cell."""

    stock = Variable('current stock', 'current stock of resource')


class Individual(object):
    """Interface for Individual."""

    strategy = Variable('harvesting strategy', 'harvesting strategy indiv.')


class Metabolism(object):
    """Interface for Metabolism."""


class Model(object):
    """Interface for Model."""

    name = "simple extraction"
    description = "A simple extraction model"
    requires = []
