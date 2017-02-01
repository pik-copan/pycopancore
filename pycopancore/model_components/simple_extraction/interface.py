"""Interface module for the simple_extraction module."""

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
    """Interface for Cell."""

    stock = Variable('current stock of resource')

#
#  Define class Individual_
#


class Individual_(object):
    """Interface for Individual."""

    strategy = Variable('harvesting strategy')


#
#  Define class Metabolism_
#


class Metabolism_(object):
    """Interface for Metabolism."""

#
#  Define class Model_
#


class Model_(object):
    """Interface for Model."""

    name = "simple extraction"
    description = "A simple extraction model"
    requires = []
