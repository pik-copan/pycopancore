# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module a template for the Society mixing class is composed to give
an example of the basic structure for the in the model used Society class.
It Inherits from Society_ in that variables and parameters are defined.
"""

#
#  Imports
#

from .interface import Society_
from pycopancore.model_components import abstract

#
#  Define class Society
#


class Society(Society_, abstract.Society):
    """
    A template for the basic structure of the Society mixin class that every
    model must use to compose their Society class. Inherits from Society_
    as the interface with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 **kwargs):
        """
        Initialize an instance of Society.
        """
        super(Society, self).__init__(**kwargs)

    processes = []

    #
    #  Definitions of further methods
    #