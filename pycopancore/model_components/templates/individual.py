# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module a template for the Individual mixing class is composed to give
an example of the basic structure for the in the model used Individual class.
It Inherits from individual_ in that variables and parameters are defined.
"""

#
#  Imports
#

from .interface import Individual_
from pycopancore.model_components import abstract

#
#  Define class Individual
#


class Individual(Individual_, abstract.Individual):
    """
    A template for the basic structure of the Individual mixin class that every
    model must use to compose their Individual class. Inherits from Individual_
    as the interface with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 # *,
                 **kwargs):
        """
        Initialize an instance of Individual.
        """
        super().__init__(**kwargs)

    processes = []

    #
    #  Definitions of further methods
    #