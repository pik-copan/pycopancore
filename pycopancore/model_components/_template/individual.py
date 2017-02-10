"""Individual class template.

In this module a template for the Individual mixing class is composed to give
an example of the basic structure for the in the model used Individual class.
It Inherits from individual_ in that variables and parameters are defined.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
#  Imports
#

from .interface import * # import all interface classes since one typically wants to cross-ref variables between entity types (this is the whole point of having an interface in the first place)
from pycopancore.model_components import abstract

#
#  Define class Individual
#


class Individual(Individual_, abstract.Individual):
    """Define your Individual class.

    A template for the basic structure of the Individual mixin class that every
    component may use to compose their Individual class.
    Inherits from Individual_
    as the interface with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 # *,
                 **kwargs):
        """Initialize an instance of Individual."""
        super().__init__(**kwargs)
        # add custom code here:
        pass

    processes = []

    #
    #  Definitions of further methods
    #
