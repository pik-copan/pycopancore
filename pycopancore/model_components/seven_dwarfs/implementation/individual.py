"""Individual entity type class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
from pycopancore.model_components.base import interface as B
# from .... import master_data_model as D
from pycopancore import ODE, Step, Explicit, Event
import numpy as np


class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 age=0,
                 beard_length=0,
                 beard_growth_parameter=0.1,
                 eating_parameter=1,
                 **kwargs):
        """Initialize an instance of dwarf."""
        super().__init__(**kwargs)

        self.age = age
        self.beard_length = beard_length
        self.beard_growth_parameter = beard_growth_parameter
        self.eating_parameter = eating_parameter

        # Following method is defined in abstract_entity_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()

    # process-related methods:

    def aging(self, unused_t):
        """Make dwarf have birthday."""
        if self.age / 100 >= np.random.random():
            if self in self.__class__.instances:
                self.deactivate()
                print("Dwarf with UID {} died from age.".format(self._uid))

        else:
            self.age = self.age + 1

    def step_timing(self, t):
        """Let one year pass."""
        return t + 1

    def eating(self, t):
        """Let dwarf eat from stock."""

        # else:  I.Cell.d_stock -= self.eating_parameter
        if self.cell.eating_stock >= self.eating_parameter:
            self.cell.d_eating_stock -= self.eating_parameter
        else:
            self.cell.eating_stock = 0
            if self in self.__class__.instances:
                self.deactivate()
                print("Dwarf with UID {} starved.".format(self._uid))
            self.cell.d_eating_stock -= 0

    def beard_growing(self, t):
        """Grow beard of dwarf in explicit manner."""
        self.beard_length = (self.beard_growth_parameter
                             * t * np.sin(t)**2
                             )

    def reproduction(self, unused_t):
        """Reproduce."""
        if self in self.__class__.instances \
                and self.cell.eating_stock > 10\
                and self.age > 5:
            child = self.__class__(cell=self.cell,
                                   age=1,
                                   beard_length=0,
                                   beard_growth_parameter=2,
                                   eating_parameter=1)
            print('a new dwarf is born', child._uid)

    def birthdate(self, t):
        """Determine Birthday"""
        return t + 1

    processes = [
        Step("aging", [I.Individual.age], [step_timing, aging]),
        ODE("eating", [B.Individual.cell.eating_stock], eating),
        Explicit("beard_growth", [I.Individual.beard_length], beard_growing),
        Step("reproduction", [], [birthdate, reproduction])
    ]
