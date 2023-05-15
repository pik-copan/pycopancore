"""Interface for lpjml coupler on CORE-side."""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from typing import List, Dict
import numpy as np

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
    pass


class Cell:
    """Interface for Cell entity type mixin."""

    # TODO: add list of all forseeable possible variables that will be used in the project

    # endogenous variables:
    lpjml_grid_cell_ids = Variable(
        "LPJmL grid cell ids",
        "List of ids of LPJmL cells that belong to this macro cell",
        datatype=List[int],
        default=[])

    cftfrac = Variable(
        "cftfrac bands",
        "array of cftfrac bands",
        datatype=np.array,
        array_shape=(32, ))

    with_tillage = Variable(
        "landuse bands",
        "array of landuse bands",
        datatype=np.array,
        array_shape=(1, ))

    landuse = Variable(
        "landuse decision bands",
        "array of landuse bands and cell ids",
        datatype=np.array
    )

    # landuse = DM.Culture.landuse_decisions.copy()

    pft_harvestc = Variable(
        "yields of different pfts",
        "array of pft_harvest bands",
        datatype=np.array,
        array_shape=(32, ))


#
# Process taxa
#
class Environment:
    """Interface for Environment process taxon mixin."""

    # endogenous variables:
    out_dict = Variable(
        "output from lpjml",
        """output dictionary from lpjml, like e.g. cftfrac""",
        datatype=Dict[str, np.ndarray])

    # TODO does this work?
    # coupler = Coupler(config_file=config_coupled_fn)

    old_out_dict = Variable(
        "old output from lpjml",
        """output dictionary from lpjml, like e.g. cftfrac""",
        datatype=Dict[str, np.ndarray])

    # exogenous variables / parameters:
    delta_t = Variable(
        "time step",
        """time step has to be given in study script""")

    start_year = Variable(
        "coupled start year",
        """start year of the coupled simulation, given by end year of lpjml spinup""")

    end_year = Variable(
        "coupled end year",
        """end year of coupled simulation""")

    in_dict = Variable(
        "input to lpjml",
        """input dictionary to lpjml with values on e.g. land use""",
        datatype=Dict[str, np.ndarray])
