"""model component Interface maxploit_most_simple_vegetation."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# TODO: use variables from the master data model wherever possible:
# from ... import master_data_model as D
# TODO: uncomment and adjust of you need further variables from another
# model component:
# import ..BBB.interface as BBB
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable


class Model(object):
    """Interface for Model mixin."""

    # metadata:
    name = "..."
    """most simple vegetation"""
    description = "..."
    """A most simple vegetation growth model"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:
class Cell(object):
    """Interface for Cell."""

    stock = Variable('current stock', 'current stock of resource')
    capacity = Variable('capacity', 'capacity of resource', default=1)
    growth_rate = Variable('growth rate', 'growth rate of resource', default=1) # could add this to environment
