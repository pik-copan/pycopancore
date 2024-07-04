"""model component Interface of inseeds_farmer_management
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# from ..MODEL_COMPONENT import interface as MODEL_COMPONENT
from pycopancore.data_model.variable import Variable
from pycopancore.data_model.master_data_model.dimensions_and_units import \
    DimensionsAndUnits as DAU


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


class World(object):
    """Define Interface for World."""

    pass


class Individual (object):
    """Interface for Individual entity type mixin."""

    aft_id = Variable('AFT ID', 'unique identifier for agent')
    behaviour = Variable('agent behaviour', 'regenerative=1, conventional=0',
                         datatype=bool)
    pbc = Variable('perceived behavioural control',
                   'own appraisal of how much efficacy agent posesses')
    tpb = Variable('theory of planned behaviour',
                   'attitude, subjective norm, perceived behavioural control')
    social_norm = Variable('social norm',
                            'social norm based on observation of own and\
                             neighboring land')
    attitude = Variable('attitude',
                        'farmer attitude based on observation of yield and soilC of\
                         own land and neighboring land')
    attitude_own_land = Variable('attitude towards own land',
                                 'attitude based on observation of yield and soilC\
                                  of own land')
    attitude_social_learning = Variable('attitude based on social learning',
                                        'attitude based on observation of yield and\
                                         soilC of neighboring land')
    avg_hdate = Variable('average harvest date',
                         'weighted average harvest date of grown crops (by crop area)',
                         unit=DAU.doy)
    soilc = Variable('soil organic carbon',
                     'soil organic carbon content of agent land',
                     unit=DAU.gC_per_m2)
    cropyield = Variable('average crop yield',
                         'average crop yield of agent land weighted by crop area',
                         unit=DAU.gC_per_m2)
