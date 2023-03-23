"""model component Interface maxploit_simple_extraction."""

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
from ..maxploit_most_simple_vegetation import interface as VEG
# from ..maxploit_social_norms import Individual as MSNIndividual # this is slowwww
from ..maxploit_social_norms import interface as SN
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable


class Model(object):
    """Interface for Model mixin."""

    # metadata:
    name = "..."
    """simple extraction"""
    description = "..."
    """A simple extraction model"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:

class Individual(object):
    """Interface for Individual."""

    behaviour = SN.Individual.behaviour


class Cell(object):
    """Interface for Cell."""

    stock = VEG.Cell.stock
    growth_rate = VEG.Cell.growth_rate.copy()
    capacity = VEG.Cell.capacity.copy()