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

# Use variables from the master data model wherever possible
from ... import master_data_model as D

# from ..MODEL_COMPONENT import interface as MODEL_COMPONENT
from ... import Variable
from ..lpjml import interface as L
import numpy as np


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "..."
    """regenerative agriculture decisions"""
    description = "..."
    """this model component shall serve for the purpose of farmer 
    decision-making on the basis of the theory of planned behaviour (TPB). 
    It uses biophysical data from LPJmL"""
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

    # pft_harvestc = L.Cell.pft_harvestc
    crop_yield = L.Cell.pft_harvestc.copy()
    # crop_yield = Variable('current yield', 'yield in given LPJmL cell')
    # soil_carbon = Variable('current soilC value', 'proxy for soil health')
    soil_carbon = L.Cell.cftfrac.copy() # TODO this is not soil_carbon, adjust
    lpjml_cell_id = L.Cell.lpjml_grid_cell_ids.copy()
    # lpjml_cell_id = Variable('lpjml cell id', 'given by lpjml') 
    # core_cell_id = Variable('core cell id', 'lpjml cell mapped to core')


class Individual (object):
    """Interface for Individual entity type mixin."""

    attitude = Variable('farmer attitude',
                        'attitude based on observation of yield and soilC of\
                         own land and neighboring land')
    pbc = Variable('perceived behavioral control',
                   'own appraisal of how much efficacy agent posesses')
    subjective_norm = Variable('norm surrounding an individual agent',
                               'average displayed farming behaviour of all\
                               direct neighbours of agent')
    # also potentially different for the two AFTs
    behavior = Variable('agent behavior', 'regenerative=1, conventional=0',
                        datatype=bool)
    past_behavior = Variable('past agent farming behavior',
                             'individual behavior before last update')
    average_waiting_time = Variable('estimated waiting time tau', 'tau')
    update_time = Variable('next update time', 'next time for update')
    
    # Different weights for the two AFTs
    # Weights for the sustainability pioneer AFT
    w_sust_attitude = Variable('attitude weight of sust. AFT',
                               'relative importance of attitude for behavior')
    w_sust_yield = Variable('yield weight of sust. AFT',
                            'relative importance of yield for attitude')
    w_sust_soil = Variable('soil carbon weight of sust. AFT',
                           'relative importance of soil health for attitude')
    w_sust_norm = Variable('norm weight of sust. AFT',
                           'relative importance of social norm for behaviour')

    # attitude composition weights, for now not differentiated between AFTs
    w_social_learning = Variable('weight of social learning in attitude',
                                 'respective importance of social learning\
                                 compared to own land for attitude')
    w_own_land = Variable('weight of own land evaluation in attitude',
                          'respective importance of own land evaluation\
                          compared to social learning for attitude')

    # taken from ronja, what is it?
    # TODO chat with Ronja abput how these two could be set up
    sust_identity_vals = Variable('parameter for general enclinedness towards\
                                  sustainable farming')
    sust_inertia_vals = Variable('parameter for change aversion')
    sust_pbc = Variable('perceived behavioural control', 'pbc of sust. AFT')

    # Weights for traditionalist AFT
    w_trad_attitude = Variable('attitude weight of trad. AFT',
                               'relative importance of attitude for behavior')
    w_trad_yield = Variable('yield weight of trad. AFT',
                            'relative importance of yield for attitude')
    w_trad_soil = Variable('soil carbon weight of trad. AFT',
                           'relative importance of soil health for attitude')
    w_trad_norm = Variable('norm weight of trad. AFT',
                           'relative importance of social norm for behaviour')
    trad_identity_vals = Variable('parameter for general enclinedness towards\
                                  sustainable farming')
    trad_inertia_vals = Variable('parameter for change aversion')
    trad_pbc = Variable('perceived behavioural control', 'pbc of trad. AFT')
    # endogenous variables:
        
    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONEINDIVIDUALVARIABLE = master_data_model.Individual.\
    # ONEINDIVIDUALVARIABLE

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERINDIVIDUALVARIABLE= MODEL_COMPONENT.Individual.\
    # ANOTHERINDIVIDUALVARIABLE

# Process taxa


class Culture (object):
    """Interface for Culture process taxon mixin."""

    acquaintance_network = D.CUL.acquaintance_network
    #TODO make an array of all individual agent decisions and respective cell ids
    landuse_decisions = Variable(
        "landuse decision bands",
        "array of landuse bands and cell ids",
        datatype=np.array
    )
    
    last_execution_time = Variable('last exec. time',
                                   'last time a step was executed',
                                   default=-1)

    landuse_update_rate = Variable("landuse style update rate"
                                   """average number of time points per time\
                                   where some individuals update their landuse\
                                   style""",
                                   unit=D.years**(-1), default=1 / D.years,
                                   lower_bound=0)   
