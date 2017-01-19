# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module a template for the Nature mixing class is composed to give an
example of the basic structure for the in the model used Nature class. It
Inherits from Nature_ in that variables and parameters are defined.
"""

#
#  Imports
#

from .interface import Nature_
from pycopancore.model_components import abstract

#
#  Define class Nature
#


class Nature(Nature_, abstract.Nature):
    """
    A template for the basic structure of the Nature mixin class that every model
    must use to compose their Nature class. Inherits from Nature_ as the interface
    with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 **kwargs):
        """
        Initialize an instance of Nature.
        """
        super(Nature, self).__init__(**kwargs)

    def __str__(self):
        """
        Return a string representation of the instance created by Nature
        """

    processes = []

    #
    #  Definitions of further methods
    #