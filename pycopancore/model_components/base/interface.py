"""Base model component interface

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

from pycopancore import Variable, ReferenceVariable
from pycopancore.base_dimensions_units import gigatons_carbon, square_kilometers, years, kelvins


# entity types:


class World_(object):
    """
    Basic World interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    contact_network = Variable("contact network")

    # attributes storing redundant information (backward references):
    societies = set() # set of Societies
    cells = set() # set of Cells


class Society_(object):
    """
    Basic Society interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    world = ReferenceVariable("world", entity_type=World_)
    territory = SetVariable("territory") # set of Cells
    
    # other variables:
    population = Variable("population")


class Cell_(object):
    """
    Basic Cell interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    world = ReferenceVariable("world", entity_type=World_)
    
    # other variables:
    location = Variable("location")
    area = Variable("area", unit=square_kilometers)

    # attributes storing redundant information (backward references):
    residents = set() # set of resident Individuals

Society_.territory.entity_type = Cell_


class Individual_(object):
    """
    Basic Individual interface.
    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    residence = ReferenceVariable("residence", entity_type=Cell_)
    
    # other variables:
    pass

# process taxa:

class Nature_(object):
    """
    Basic Nature interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    pass

class Metabolism_(object):
    """
    Basic Metabolism interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    pass

class Culture_(object):
    """
    Basic Culture interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    pass


# basic model component:

class Model_(object):
    """
    Basic Model interface
    """

    # metadata:
    name = "copan:CORE Base"
    description = "Basic model only providing basic relationships between " \
                  "entity types."
    requires = []

    # additional attributes for internal logics:
    
    components = None

    ODE_variables = None

    variables = None
    processes = None
