"""Interface for lpjml coupler on CORE-side."""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from pycoupler.data import LPJmLData, LPJmLDataSet
from pycoupler.coupler import LPJmLCoupler
from networkx import Graph


from pycopancore.data_model.variable import Variable


class Model:
    """Interface for Model mixin."""

    # metadata:
    name = "lpjml coupler"
    description = "model component implementing the bidirectional coupling of\
                    copan:CORE to lpjml"
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


# Entity type world
class World:
    """Interface for World entity type mixin."""
    # TODO: This currently does not work with mixin, since mixin messes up
    #   Python inheritance logic
    # lpjml = Variable(
    #     "coupled lpjml simulation",
    #     "pycoupler lpjmlcoupler object to operate coupled lpjml instance",
    #     datatype=LPJmLCoupler
    # )

    input = Variable(
        "input to lpjml",
        "input LPJmLDataSet to lpjml with values on e.g. land use",
        datatype=LPJmLDataSet
    )

    output = Variable(
        "output from lpjml",
        "output LPJmLDataSet from lpjml with values on e.g. cftfrac",
        datatype=LPJmLDataSet
    )

    neighbourhood = Variable(
        "neighbourhood",
        "networkx graph of neighbourhood of cells",
        datatype=Graph
    )


class Cell:
    """Interface for Cell entity type mixin."""
    pass

    # TODO: This currently does not work with mixin, since mixin messes up
    #   Python inheritance logic

    # input = Variable(
    #     "input to lpjml",
    #     "input LPJmLDataSet to lpjml with values on e.g. land use",
    #     datatype=LPJmLDataSet
    # )

    # output = Variable(
    #     "output from lpjml",
    #     "output LPJmLDataSet from lpjml with values on e.g. cftfrac",
    #     datatype=LPJmLDataSet
    # )

    # neighbourhood = Variable(
    #     "neighbourhood",
    #     "neighbourhood of cells",
    #     datatype=LPJmLData
    # )
