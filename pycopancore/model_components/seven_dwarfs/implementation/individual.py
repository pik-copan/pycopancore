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
# from .... import master_data_model as D
from pycopancore import ODE, Step, Explicit
import numpy as np

class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 age = 0,
                 beard_length = 0,
                 beard_growth_parameter = 0.1,
                 eating_parameter = 1,
                 **kwargs):
        """Initialize an instance of dwarf."""
        super().__init__(**kwargs)

        self.age = age
        self.beard_length = beard_length
        self.beard_growth_parameter = beard_growth_parameter
        self.eating_parameter = eating_parameter

        pass


    def deactivate(self):
        """Deactivate a dwarf."""
        super().deactivate()

    def reactivate(self):
        """Reactivate a dwarf."""
        super().reactivate()

    # process-related methods:

    def aging(self):
        """Make dwarf have birthday."""
        self.age = self.age + 1
        if self.age/100 >= np.random.random():
            print("Dwarf died from age.")
            self.deactivate()

    def step_timing(self, t):
        """Let one year pass."""
        return t + 1

    ' TODO: Check if interface attribute should be changed or self.cell.stock' \
    ' variable! Since the latter uses the base class, is a reference variable needed?'
    def eating(self, t):
        """Let dwarf eat from stock."""
        print("Hello Dwarf!")
        if self.cell.stock < self.eating_parameter:
            print("Dwarf starved.")
            self.cell.stock = 0
            self.deactivate()
            #I.Cell.d_stock -= 0
        # else:  I.Cell.d_stock -= self.eating_parameter
        self.cell.d_stock -= self.eating_parameter

    def beard_growing(self):
        """Grow beard of dwarf in explicit manner."""
        self.beard_length = (self.beard_length
                             + self.beard_growth_parameter
                             * self.age
                             )

    processes = [
        Step("aging", [I.Individual.age], [step_timing, aging]),
        ODE("eating", [I.Cell.stock], eating),
        Explicit("beard_growth", [I.Individual.beard_length], beard_growing)
    ]
