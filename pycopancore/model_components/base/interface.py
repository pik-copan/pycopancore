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
from pycopancore import master_data_model as MDM
from pycopancore.base_dimensions_units import \
    gigatons_carbon, square_kilometers, years, kelvins, people


# process taxa:


class Nature (object):
    """
    Basic Nature interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    pass


class Metabolism (object):
    """
    Basic Metabolism interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    pass


class Culture (object):
    """
    Basic Culture interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    basic_social_network = MDM.basic_social_network
    # Note: don't forget to add and remove nodes in __init__, !


# entity types:


class World (object):
    """
    Basic World interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    # attributes storing redundant information (backward references):
    societies = None # set of Societies
    cells = None # set of Cells

    # references:
    nature = ReferenceVariable("nature", type=Nature)
    metabolism = ReferenceVariable("metabolism", type=Metabolism)
    culture = ReferenceVariable("culture", type=Culture)


class Society (object):
    """
    Basic Society interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    world = ReferenceVariable("world", type=World)
    next_higher_society = ReferenceVariable("next higher society")
    
    # other variables:
    population = Variable("population", unit=people)

    # read-only attributes storing redundant information (backward references):
    next_lower_societies = None # set of sub-Societies of next lower level
    direct_cells = None # set of direct territory Cells
    cells = None # set of direct and indirect territory Cells

Society.next_higher_society.type = Society # specified only now to avoid recursion


class Cell (object):
    """
    Basic Cell interface. 
    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    world = ReferenceVariable("world", type=World)
    society = ReferenceVariable("society", type=Society,
                    desc="lowest-level society this cell is a cells of")
    
    # other variables:
    location = Variable("location")
    area = Variable("area", unit=square_kilometers)
    geometry = Variable("geometry")

    # attributes storing redundant information (backward references):
    individuals = None # set of resident Individuals

Society.cells.type = Cell # specified only now to avoid recursion


class Individual (object):
    """
    Basic Individual interface.
    It contains all variables specified as mandatory ("base variables").
    """

    # references:    
    cell = ReferenceVariable("cell", desc="cell of residence", type=Cell)
    
    # other variables:
    relative_weight = Variable("relative representation weight", 
                unit=unity, lower_bound=0, default=1,
                desc="relative weight ")

    # attributes storing redundant information (aggregate information):
    
    # share of society's direct population represented by this individual:
    population_share = None 
    # absolute population represented by this individual:
    represented_population = None
    

# basic model component:


class Model (object):
    """
    Basic Model interface
    """

    # metadata:
    name = "copan:CORE Base"
    description = "Basic model only providing basic relationships between " \
                  "entity types."
    requires = []

    # references of base component:
    nature = ReferenceVariable("nature", type=Nature)
    metabolism = ReferenceVariable("metabolism", type=Metabolism)
    culture = ReferenceVariable("culture", type=Culture)
