"""The simple_extraction individual module has some dynamics.

That's about it.
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

from pycopancore.model_components import abstract
from .interface import Individual_

#
#  Define class Individual
#


class Individual(Individual_, abstract.Individual):
    """Define properties of simple_extraction individual.

    Inherits from Individual_ as the interface
    with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 *,
                 strategy=0,
                 **kwargs
                 ):
        """Initialize an instance of Individual."""
        super(Individual, self).__init__(**kwargs)

        self.strategy = strategy,

    #
    #  Definitions of further methods
    #

    processes = []
