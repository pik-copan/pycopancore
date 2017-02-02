"""Interface module for the most_simple_vegetation component."""

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

from pycopancore import Variable

#
#  Define class Cell_
#


class Cell_(object):
    """Define Interface for Cell."""

    stock = Variable('current stock of resource')
    capacity = Variable('capacity of resource')
    growth_rate = Variable('growth rate of resource')
    # resource = Variable('current resource')
    # capacity = Variable('whole capacity')
    # step_resource = Variable('step resource')
    # event_value = Variable('event value')
    # explicit_value = Variable('explicit value')
    # step_width = Variable('time between two steps')
    # last_execution = Variable('last time step was executed')

#
#  Define class Individual_
#


class Individual_(object):
    """Define Interface for Individual."""

    strategy = Variable('harvesting strategy')
    imitation_tendency = Variable('imitation tendency (former rationality)')


#
#  Define class Model_
#


class Model_(object):
    """Define Interface for Model."""

    name = "most simple vegetation"
    description = "A most simple vegetation growth model"
    requires = []
