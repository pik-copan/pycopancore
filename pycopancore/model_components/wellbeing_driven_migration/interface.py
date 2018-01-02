"""model component Interface template.
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
from ... import master_data_model as D
from ...data_model.master_data_model import MET, S
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "wellbeing-driven migration"
    """a unique name for the model component"""
    description = "migration flow between social_systems is proportional to a " \
        "sigmoid function of wellbeing difference and product of populations"
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:


class SocialSystem (object):
    """Interface for SocialSystem entity type mixin."""

    # endogenous variables:

    immigration = S.immigration
    emigration = S.emigration

    migrant_population = S.migrant_population
    
    # exogenous variables / parameters:
    
    population = S.population
    wellbeing = S.wellbeing
    

# process taxa:


class Metabolism (object):
    """Interface for Metabolism process taxon mixin."""

    # endogenous variables:

    # exogenous variables / parameters:
    emigration_wellbeing_quotient_offset = Variable(
        "emigration wellbeing quotient offset",
        "wellbeing quotient at which emigration probability has its point "
        "of inflection", 
        unit = D.unity,
        is_intensive=True,
        default=3) # 1
    emigration_probability_characteristic_slope = Variable(
        "emigration probability's characteristic slope",
        "slope of the normalized sigmoid function at its point of inflection", 
        unit = D.unity,
        is_intensive=True,
        default=1)
    basic_emigration_probability_rate = Variable(
        "basic emigration probability rate",
        "absolute value of emigration probability rate at its point of inflection",
        unit = D.years**-1 / D.people**2,
        lower_bound=0, is_intensive=True, 
        default = 8e-13) # 3e-13
    