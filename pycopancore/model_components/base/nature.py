# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module the basic Nature mixing class is composed to set the basic
structure for the later in the model used Nature class. It Inherits from
Nature_ in that basic variables and parameters are defined.
"""

#
#  Imports
#

from pycopancore import Variable
from .interface import Cell_, Nature_, Individual_, Culture_, Society_, Metabolism_, Model_

#
#  Define class Cell
#


class Nature(Nature_):
    """
    Basic Nature mixin class that every model must use in composing their
    Nature class. Inherits from Nature_ as the interface with all necessary
    variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 # *,
                 **kwargs
                 ):
        """
        Initialize an instance of Nature.

        :param kwargs:
        """
        super(Nature, self).__init__(**kwargs)
        pass

    def __str__(self):
        """
        Return a string representation of the object of class Nature.
        """

    processes = []

    #
    #  Definitions of further methods
    #
