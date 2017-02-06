"""Interface module for a dummy component."""

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

    resource = Variable('current resource')
    resource2 = Variable('current resource2')
    capacity = Variable('whole capacity')
    step_resource = Variable('step resource')
    event_value = Variable('event value')
    explicit_value = Variable('explicit value')
    step_width = Variable('time between two steps')
    last_execution = Variable('last time step was executed')


#
#  Define class Model_
#


class Model_(object):
    """Define Interface for Model."""

    name = "copan:CORE Dummy"
    description = "Dummy Model to test and develop the runner_prototype "
    requires = []
