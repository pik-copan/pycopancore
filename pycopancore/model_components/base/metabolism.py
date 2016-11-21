# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module the basic Metabolism mixing class is composed to set the basic
structure for the later in the model used Metabolism class. It Inherits from
Metabolism_ in that basic variables and parameters are defined.
"""

#
#  Imports
#

from pycopancore import Variable
from .interface import Cell_, Nature_, Individual_, Culture_, Society_, Metabolism_, Model_

#
#  Define class Metabolism
#


class Metabolism(Metabolism_):
    """
    Basic Metabolism mixin class that every model must use in composing their
    Metabolism class. Inherits from Metabolism_ as the interface with all
    necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 # *,
                 **kwargs
                 ):
        """
        Initialize an instance of Metabolism.

        Parameters
        ----------
        kwargs:
        """
        super(Metabolism, self).__init__(**kwargs)
        pass

    def __str__(self):
        """
        Return a string representation of the object of class Metabolism.
        """

    processes = []

    #
    #  Definitions of further methods
    #
