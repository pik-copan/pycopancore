"""model component Interface template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:", then
remove these instructions.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from ... import master_data_model as D
# TODO: uncomment and adjust of you need further variables from another
# model component:
# import ..BBB.interface as BBB
from ... import Variable


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
    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # X = D.X
    # TODO: uncomment and adjust of you need further variables from another
    # model component:
    # Z = BBB.Z
    # TODO: uncomment and adjust only if you really need other variables:
    # W = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:
    # TODO: similarly


class Society (object):
    """Interface for Society entity type mixin."""

    # endogenous variables:
    district_type = Variable("district type",
                             "type of the society, e.g. County or "
                             "Municipality")

    # exogenous variables / parameters:


class Cell (object):
    """Interface for Cell entity type mixin."""

    # endogenous variables:

    characteristic = Variable("characteristic",
                              "sort of cell, e.g farmland or city")
    average_precipitation = Variable("average precipitation",
                                     "average precipitation per square meter "
                                     "of cell's area",
                                     lower_bound=0,
                                     dimension=D.volume/D.area)

    # exogenous variables / parameters:


class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
    profession = Variable("profession",
                          "profession of an Individual, eg. farmer or townsman")
    subjective_income_ranke = Variable("subjective income rank",
                                       "ranking of an individual by income"
                                       "in its cell",
                                       lower_bound=0,
                                       upper_bound=1)
    farm_size = Variable("farm size",
                         "Size of the farm of an individual, if his "
                         "profession is farmer",
                         lower_bound=0,
                         unit=D.square_kilometers)
    base_income = Variable("base income",
                           "Income before trade, distributed by society if "
                           "society is a municipality",
                           lower_bound=0,
                           unit=D.dollars)
    base_water = Variable("base water",
                          "Water before trade, calculated by farm size and "
                          "average farmland precipitation",
                          lower_bound=0,
                          dimension=D.volume)
    liquidity = Variable("liquidity",
                         "income after trade",
                         lower_bound=0,
                         unit=D.dollars)
    food = Variable("food",
                    "water after trade. Since it is virtual water, it can be "
                    "subsumed into food.",
                    lower_bound=0,
                    dimension=D.volume)

    # exogenous variables / parameters:


# process taxa:


class Metabolism (object):
    """Interface for Metabolism process taxon mixin."""

    # endogenous variables:
    water_price = Variable("waer price",
                           "price of water that is calculated by market "
                           "clearing",
                           lower_bound=0,
                           unit=D.dollars)

    # exogenous variables / parameters:
