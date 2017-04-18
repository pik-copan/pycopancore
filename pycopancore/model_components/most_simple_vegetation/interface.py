"""Interface module for the most_simple_vegetation component."""

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
    capacity = Variable('capacity', 'capacity of resource')
    growth_rate = Variable('growth rate', 'growth rate of resource')


class Model(object):
    """Interface for Model."""

    name = "most simple vegetation"
    description = "A most simple vegetation growth model"
    requires = []
