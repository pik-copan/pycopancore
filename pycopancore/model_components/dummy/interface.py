# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is the interface module for a dummy component to test the runner
"""

#
#  Imports
#

from pycopancore import Variable

#
#  Define class Cell_
#

class Cell_(object):
    """
    Interface for Cell.
    """

#
#  Define class Model_
#

class Model_(object):
    """
    Interface for Model.
    """

    name = "copan:CORE Dummy"
    description = "Dummy Model to test and develop the runner_prototype "
    requires = []