# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module a template for the Culture mixing class is composed to give an
example of the basic structure for the in the model used Culture class. It
Inherits from Culture_ in that variables and parameters are defined.
"""

#
#  Imports
#

from .interface import Culture_
from pycopancore.model_components import abstract

#
#  Define class Culture
#


class Culture(Culture_, abstract.Culture):
    """
    A template for the basic structure of the Culture mixin class that every
    model must use to compose their Culture class. Inherits from Culture_ from
    the interface with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 # *,
                 **kwargs):
        """
        Initialize an instance of Culture.
        """
        super().__init__(**kwargs)

    def __str__(self):
        """
        Return a string representation of the instance created by Culture
        """

    processes = []

    #
    #  Definitions of further methods
    #
