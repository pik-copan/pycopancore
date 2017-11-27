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

from ... import master_data_model as D
from ...data_model.master_data_model import CUL, I
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "social learning of environmental friendliness"
    """a unique name for the model component"""
    description = "a certain fraction of individuals imitates a random " \
        "acquaintance's env. friendliness with a probability depending on " \
        "their surrounding terrestrial carbon density "
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:


class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
    is_environmentally_friendly = I.is_environmentally_friendly


# process taxa:


class Culture (object):
    """Interface for Culture process taxon mixin."""

    # exogenous variables / parameters:
    environmental_friendliness_learning_rate = \
        Variable("environmental friendliness learning rate",
                 "rate at which a fraction of individuals learn " \
                 "environmental (un)friendliness from neighbours",
                 unit=D.years**-1, lower_bound=0, default=1)
    environmental_friendliness_learning_fraction = \
        Variable("awareness update fraction",
                 "fraction of individuals learning environmental " \
                 "(un)friendliness simultaneously",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=0.1)
    environmental_friendliness_learning_density_quotient_offset = Variable(
        "environmental friendliness learning density quotient offset",
        "terrestrial carbon density quotient at which imitation probability "
        "has its point of inflection", 
        unit=D.unity, is_intensive=True, default=1)
    environmental_friendliness_learning_probability_characteristic_slope = Variable(
        "environmental friendliness imitation probability's characteristic slope",
        "slope of the normalized sigmoid function at its point of inflection", 
        unit=D.unity, is_intensive=True, default=1)
