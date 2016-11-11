# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module the basic Cell mixing class is composed to set the basic
structure for the later in the model used Cell class. It Inherits from Cell_
in that basic variables and parameters are defined.
"""

#
#  Imports
#

from private import Variable
from .interface import Cell_, Nature_, Individual_, Culture_, Society_, Metabolism_, Model_

#
#  Define class Cell
#


class Cell(Cell_):
    """
    Basic Cell mixin class that every model must use in composing their Cell
    class. Inherits from Cell_ as the interface with all necessary variables
    and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 *,
                 location=(0, 0),
                 area=1,
                 society=None,
                 geometry=None,
                 **kwargs
                 ):
        """
        Initialize an instance of Cell.
        """
        super(Cell, self).__init__(**kwargs)

        assert location is not None
        self.location = location

        assert area > 0, "area must be > 0"
        self.area = area

        assert isinstance(society, Society_), \
            "society must be an instance of Society"
        self.society = society

        self.geometry = geometry

    def __str__(self):
        """
        Return a string representation of the object of class Cell.
        """

    processes = []

    #
    #  Definitions of further methods
    #
