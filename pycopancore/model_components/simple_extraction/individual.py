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

from pycopancore.model_components import abstract
from . import interface as I


class Individual(I.Individual, abstract.Individual):
    """Define properties of simple_extraction individual.

    Inherits from I.Individual as the interface
    with all necessary variables and parameters.
    """

    def __init__(self,
                 *,
                 strategy=0,
                 **kwargs
                 ):
        """Initialize an instance of Individual."""
        super(Individual, self).__init__(**kwargs)

        self.strategy = strategy,

    processes = []
