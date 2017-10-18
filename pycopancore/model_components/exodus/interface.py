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
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "Exodus"
    description = "..."
    """A migration model in the urban rural space."""
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

    total_gross_income = Variable("total gross income",
                                  "Total income generated in the world.",
                                  lower_bound=0,
                                  unit=D.dollars)
    total_harvest = Variable("total harvest",
                             "All water that has been harvested in the world",
                             lower_bound=0,
                             dimension=D.volume * D.time,
                             unit=D.meters ** 3 / D.years)
    total_nutrition = Variable("total nutrition",
                               "All water that is being consumed in the world",
                               lower_bound=0,
                               dimension=D.volume * D.time,
                               unit=D.meters ** 3 / D.years)
    water_price = Variable("water price",
                           "price of water that is calculated by market "
                           "clearing",
                           lower_bound=0,
                           unit=D.dollars,
                           default=1)


class Society (object):
    """Interface for Society entity type mixin."""

    # endogenous variables:
    municipality_like = Variable("municipality like",
                                 "If true, society is a Municipality, "
                                 "otherwise a county",
                                 datatype=bool)
    base_mean_income = Variable("base income",
                                "Base of scaling mean income dependend on "
                                "population, only important for municipality")
    mean_income_or_farmsize = Variable("Mean income or farmsize",
                                       "Mean income or farm size dependend on "
                                       "population and base_mean_income")
    income_or_farm_size_pdf = Variable("income or farm size probability "
                                       "density function",
                                       "function which distributes income and "
                                       "farm size")
    income_or_farm_size_cdf = Variable("income or farm size cumulative "
                                       "distribution function",
                                       "cumulative distribution function of "
                                       "income and farm size")
    pdf_mu = Variable("log normal parameter mu",
                      "parameter mu of the log-normal distribution",
                      lower_bound=0)
    pdf_sigma = Variable("log normal parameter sigma",
                         "parameter sigma of the log-normal distribution",
                         lower_bound=0)
    liquidity_sigma = Variable("Liquidity sigma",
                               "Sigma parameter of pdf of liquidity")
    liquidity_median = Variable("Liquidity Mean",
                                "Median of pdf of liquidity")
    liquidity_loc = Variable("Liquidity location",
                             "Location parameter of pdf of liquidity")
    average_liquidity = Variable("Average Liquidity",
                                 "Average over all liquidities in society",
                                 lower_bound=0,
                                 unit=D.dollars)
    average_utility = Variable("Average Utility",
                               "Average Utility in a society")
    gini_coefficient = Variable("Gini Coefficient",
                                "Gini coefficient of utilities")

    # exogenous variables / parameters:


class Cell (object):
    """Interface for Cell entity type mixin."""

    # endogenous variables:

    characteristic = Variable("characteristic",
                              "sort of cell, e.g 'farmland' or 'city' ")
    average_precipitation = Variable("average precipitation",
                                     "average precipitation per square meter "
                                     "of cell's area and year",
                                     lower_bound=0,
                                     dimension=D.volume / (D.area * D.time),
                                     unit=D.meters/D.years)

    # exogenous variables / parameters:


class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
    profession = Variable("profession",
                          "profession of an Individual, eg. 'farmer' or "
                          " 'townsman' ")
    subjective_income_rank = Variable("subjective income rank",
                                      "ranking of an individual by income"
                                      "in its cell",
                                      lower_bound=0,
                                      upper_bound=1)
    farm_size = Variable("farm size",
                         "Size of the farm of an individual, if his "
                         "profession is farmer",
                         lower_bound=0,
                         unit=D.square_kilometers)
    gross_income = Variable("gross income",
                            "Income before trade, distributed by society if "
                            "society is a municipality",
                            lower_bound=0,
                            unit=D.dollars)
    harvest = Variable("harvest",
                       "Water harvested before trade, calculated by farm size "
                       "and average farmland precipitation",
                       lower_bound=0,
                       dimension=D.volume*D.time,
                       unit=D.meters**3 / D.years)
    liquidity = Variable("liquidity",
                         "income after trade",
                         lower_bound=0,
                         unit=D.dollars)
    nutrition = Variable("nutrition",
                         "water after trade. Since it is virtual water, "
                         "it can be subsumed into nutrition.",
                         lower_bound=0,
                         dimension=D.volume / D.time)
    nutrition_need = Variable("nutrition need",
                              "need of nutrition per time",
                              dimension=D.volume / D.time,
                              unit=D.meters**3 / D.years)
    utility = Variable("utility",
                       "Utility of an agent, calculated by any useful "
                       "function",
                       lower_bound=0,
                       upper_bound=1)
    second_degree_rewire_prob = Variable("second degree rewire probability",
                                         "Probability to rewire to a neighbour "
                                         "of degree 2.",
                                         default=0.3)
    outspokenness = Variable("outspokenness",
                             "Describes how often per year an individual does "
                             "social updates in average",
                             default=1)
    random_rewire = Variable("Random rewire",
                             "Probability to rewire to a random individual"
                             "and cutiing a connection with a known one.",
                             default=0.05)

    # exogenous variables / parameters:


# process taxa:


class Metabolism (object):
    """Interface for Metabolism process taxon mixin."""

    # endogenous variables:
    market_frequency = Variable("market frequency",
                                "Defines how often per year the market "
                                "clearing is calculated",
                                default=1)

    non_equilibrium_checker = Variable("Nonequilibrium Checker",
                                       "Is set true, if market is not in "
                                       "equilibrium anymore",
                                       default=False)


class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:
    network_clustering = Variable("network clustering",
                                  "Average clustering of network, values from"
                                  "networkx.average_clustering",
                                  default=0)
    modularity = Variable("Modularity",
                          "Modularity of a partition of the network",
                          default=0)
    transitivity = Variable("Transitivity",
                            "Transitivity of the network")
    split = Variable("Split",
                     "Shows if network has split",
                     default=False)
    fully_connected_network = Variable("Fully connected Network",
                                       "This var is set true when the "
                                       "acquaintance network is fully "
                                       "connected",
                                       default=False,
                                       datatype=bool)
