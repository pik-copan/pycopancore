"""Interface module for the simple_extraction module."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore import Variable


class Individual(object):
    """Interface for Individual."""

    strategy = Variable('harvesting strategy', 'harvesting strategy indiv.')


class Cell(object):
    """Interface for Cell."""

    stock = Variable('current stock', 'current stock of resource')
    growth_rate = Variable('growth rate', 'growth rate of resource')
    individual = None


class Model(object):
    """Interface for Model."""

    name = "simple extraction"
    description = "A simple extraction model"
    requires = []
