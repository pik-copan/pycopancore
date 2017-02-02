"""The simple_extraction cell module."""

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

# from pycopancore import ODE, Step, Explicit, Event
from pycopancore.model_components import abstract
from .interface import Cell_

#
#  Define class Cell
#


class Cell(Cell_, abstract.Cell):
    """Define properties of simple_extraction cell.

    Inherits from Cell_ as the interface
    with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 *,
                 stock=1,
                 **kwargs
                 ):
        """Initialize an instance of Cell."""
        super(Cell, self).__init__(**kwargs)

        self.stock = stock

    #
    #  Definitions of further methods
    #

    processes = []
