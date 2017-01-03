# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module the basic Culture mixing class is composed to set the basic
structure for the later in the model used Culture class. It Inherits from
Culture_ in that basic variables and parameters are defined.
"""

#
#  Imports
#

from pycopancore import Variable
from pycopancore.model_components import abstract
from .interface import Cell_, Nature_, Individual_, Culture_, Society_, Metabolism_, Model_

#
#  Define class Culture
#


class Culture(Culture_, abstract.Culture):
    """
    Basic Culture mixin class that every model must use in composing their
    Culture class. Inherits from Culture_ as the interface with all necessary
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
        Initialize an instance of Culture.

        Parameters
        ----------
        kwargs:
        """
        super(Culture, self).__init__(**kwargs)
        pass

    def __repr__(self):
        """
        Return a string representation of the object of class base.Culture.
        """
        return (super().__repr__() +
                ('base.culture object')
                )

    processes = []

    #
    #  Definitions of further methods
    #
