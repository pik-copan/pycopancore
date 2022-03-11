"""Interface for lpjml coupler on CORE-side.

TODO: adjust or fill in code and documentation wherever marked by "TODO:", then
remove these instructions.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# Use variables from the master data model wherever possible
# from tkinter import Variable #TODO what is this?

from typing import List, Dict

from ... import master_data_model as D
from ...data_model import Dimension, Unit #TODO: what else do we need from the data model?

# TODO: uncomment and adjust to use variables from other pycopancore model
# components:
# from ..MODEL_COMPONENT import interface as MODEL_COMPONENT

# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable

import numpy as np


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "lpjml coupler"
    description = "model component implementing the bidirectional coupling of copan:CORE to lpjml"
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


#
# Entity types
#




class Cell (object):
    """Interface for Cell entity type mixin."""

    # endogenous variables:
    lpjml_grid_cell_ids = Variable(
        "LPJmL grid cell ids",
        "List of ids of LPJmL cells that belong to this macro cell",
        datatype = List[int],
        default = [])
    
    cftfrac = Variable(
        "cftfrac bands",
        "array of cftfrac bands",
        datatype = np.array,
        array_shape = (32, ))

    # exogenous variables / parameters:
    landuse = Variable(
        "landuse bands",
        "array of landuse bands",
        datatype = np.array,
        array_shape = (64, ))


#
# Process taxa
#
class Environment (object):
    """Interface for Environment process taxon mixin."""

    # endogenous variables:
    old_out_dict = Variable(
        "old output from lpjml", 
        """output dictionary from lpjml, like e.g. cftfrac""",
        datatype = Dict[str, np.ndarray])    # TODO: make generic
    
    out_dict = Variable(
        "output from lpjml", 
        """output dictionary from lpjml, like e.g. cftfrac""",
        datatype = Dict[str, np.ndarray])    # TODO: make generic
    

    # exogenous variables / parameters:
    delta_t = Variable(
        "time step",
        """time step has to be given in study script""")
    
    end_year = Variable(
        "copan_start_year", 
        """start year of the copan run given by end year of lpjml spinup""")
    
    in_dict = Variable(
        "input to lpjml", 
        """input dictionary to lpjml with values on e.g. land use""",
        datatype = Dict[str, np.ndarray])
    # INPUT_VARIABLE_OF_INTEREST = ...
    # OUTPUT_VARIABLE_OF_INTEREST = ...


