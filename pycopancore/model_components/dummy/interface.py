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

    resource = Variable('current resource', 'resource of dummy.cell')
    resource2 = Variable('current resource2', 'second resource of dummy cell')
    capacity = Variable('whole capacity', 'capacity of resource of dummy.cell')
    step_resource = Variable('step resource', 'resource for step process')
    event_value = Variable('event value', 'value for event process')
    explicit_value = Variable('explicit value', 'value for explicit process')
    step_width = Variable('time between two steps', 'step width in dummy.cell')
    last_execution = Variable('last time step was executed', 'last ex. time')


#
#  Define class Model_
#


class Model_(object):
    """Define Interface for Model."""

    name = "copan:CORE Dummy"
    description = "Dummy Model to test and develop the runner_prototype "
    requires = []
