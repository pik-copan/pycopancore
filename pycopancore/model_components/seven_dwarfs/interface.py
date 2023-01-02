"""model component Interface template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:", then
remove these instructions.
"""

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
from ... import master_data_model as D
from ...data_model.master_data_model import CUL



class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "..."
    """a unique name for the model component"""
    description = "..."
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


# entity types:


class World (object):
    """Interface for World mixin."""

    # endogenous variables:
    # wherever possible!:
    # X = D.X
    # model component:
    # Z = BBB.Z
    # W = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:


class Cell (object):
    """Interface for Cell entity type mixin."""

    # endogenous variables:
    eating_stock = Variable("eating stock",
                            "the eating stock",
                            unit=D.kilograms,
                            lower_bound=0,
                            default=100)
    # exogenous variables / parameters:


class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
    age = Variable("age",
                   "dwarf's age",
                   unit=D.years,
                   default=0)
    beard_length = Variable("beard length",
                            "length of beard",
                            unit=D.meters,
                            default=0)
    beard_growth_parameter = Variable("beard growth parameter",
                                      "growth speed of dwarf beard",
                                      default=0.1)
    eating_parameter = Variable("eating parameter",
                                "eating speed of dwarf",
                                default=1)

class SocialSystem(object):
    """Interface for SocialSystem mixin"""
    pass

class Culture (object):
    """Interface for Culture mixin"""

    some_array = Variable("array",
                          """Read in some array""")

    pass

class Group(object):
    """Interface for Group mixin"""

    having_members = Variable("test",
                      "test",
                      default=True)

    pass
