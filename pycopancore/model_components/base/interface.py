# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this base interface module, variables for each entity are defined in
corresponding class as sympy objects . The corresponding classes are Cell_,
Nature_, Individual_, Culture_, Society_, Metabolism_ and Model_.
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
    Basic Cell interface. It contains all variables specified as mandatory
    ("base variables").
    """

    location = Variable("location")
    area = Variable("area")
    geometry = Variable("geometry")
    society = Variable("society")


#
#  Define class Nature_
#


class Nature_(object):
    """
    Basic Nature interface. It contains all variables specified as mandatory
    ("base variables").
    """
    pass

#
#  Define class Individual_
#


class Individual_(object):
    """
    Basic Individual interface. It contains all variables specified as
    mandatory ("base variables").
    """

    cell = Variable("cell")

#
#  Define class Culture_
#


class Culture_(object):
    """
    Basic Culture interface. It contains all variables specified as mandatory
    ("base variables").
    """
    pass

#
#  Define class Society_
#


class Society_(object):
    """
    Basic Society interface. It contains all variables specified as mandatory
    ("base variables").
    """

    population = Variable("population")

#
#  Define class Metabolism_
#


class Metabolism_(object):
    """
    Basic Metabolism interface. It contains all variables specified as
    mandatory ("base variables").
    """
    pass

#
#  Define class Model_
#


class Model_(object):
    """
    Basic Model interface. It contains all variables specified as mandatory
    ("base variables").
    """

    name = "copan:CORE Base"
    description = "Basic model only providing basic relationships between entity types."
    requires = []

    components = None


    cells = []
    cell_variables_dict = None
    cell_processes = None

    Nature = None
    Nature_processes = None
    Nature_parameters_dict = None

    individuals = []
    individual_variables_dict = None
    individual_processes = None

    Culture = None
    Culture_processes = None
    Culture_parameters_dict = None

    societies = []
    society_variables_dict = None
    society_processes = None

    Metabolism = None
    Metabolism_processes = None
    Metabolism_parameters_dict = None

    other_parameters_dict = None

    ODE_variables = None


    variables = None
    processes = None