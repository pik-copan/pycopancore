# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module the basic Cell mixing class is composed to set the basic
structure for the later used model Cell class. It Inherits from Cell_
in that basic variables and parameters are defined.
"""

#
#  Imports
#

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

    def __init__(self,*, **kwargs):
        """
        Initialize an instance of Cell.
        """
        super(Cell, self).__init__(**kwargs)

    def __str__(self):
        """
        Return a string representation of the object of class cells
        """

    #
    #  Definitions of further methods
    #