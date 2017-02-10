"""Define variables of the base components.

In this base interface module, variables for each entity are defined in
corresponding class as sympy objects . The corresponding classes are World_,
Cell_, Nature_, Individual_, Culture_, Society_, Metabolism_ and Model_.
"""

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
# Define class World_
#


class World_(object):
    """Define variables of world.

    Basic World interface. It contains all variables specified as mandatory
    ("base variables").
    """

    contact_network = Variable("contact network")


#
#  Define class Cell_
#


class Cell_(object):
    """Define variables of cell.

    Basic Cell interface. It contains all variables specified as mandatory
    ("base variables").
    """

    location = Variable("location")
    area = Variable("area")
    geometry = Variable("geometry")
    society = Variable("society")
    world = Variable("world")


#
#  Define class Nature_
#


class Nature_(object):
    """Define variables of nature.

    Basic Nature interface. It contains all variables specified as mandatory
    ("base variables").
    """

    pass

#
#  Define class Individual_
#


class Individual_(object):
    """Define variables of individual.

    Basic Individual interface. It contains all variables specified as
    mandatory ("base variables").
    """

    cell = Variable("cell")

#
#  Define class Culture_
#


class Culture_(object):
    """Define variables of culture.

    Basic Culture interface. It contains all variables specified as mandatory
    ("base variables").
    """

    pass

#
#  Define class Society_
#


class Society_(object):
    """Define variables of society.

    Basic Society interface. It contains all variables specified as mandatory
    ("base variables").
    """

    population = Variable("population")

#
#  Define class Metabolism_
#


class Metabolism_(object):
    """Define variables of metabolism.

    Basic Metabolism interface. It contains all variables specified as
    mandatory ("base variables").
    """

    pass

#
#  Define class Model_
#


class Model_(object):
    """Define variables of model.

    Basic Model interface. It contains all variables specified as mandatory
    ("base variables").
    """

    name = "copan:CORE Base"
    description = "Basic model only providing basic relationships between " \
                  "entity types."
    requires = []

    components = None

    worlds = []
    world_variables_dict = None
    world_processes = None

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
