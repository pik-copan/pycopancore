"""Metabolism mixin class template.

It is composed to give
an example of the basic structure for the in the model used Metabolism class.
It Inherits from Metabolism_ in that variables and parameters are defined.
"""

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

from .interface import * # import all interface classes since one typically wants to cross-ref variables between entity types (this is the whole point of having an interface in the first place)
from pycopancore.model_components import abstract

#
#  Define class Metabolism
#


class Metabolism(Metabolism_, abstract.Metabolism):
    """Define your Metabolism.

    A template for the basic structure of the Metabolism mixin class that your
    model may use to compose their Metabolism class. Inherits from Metabolism_
    as the interface with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 **kwargs):
        """Initialize the unique instance of Nature."""
        super(Metabolism, self).__init__(**kwargs)
        # add custom code here:
        pass

    def __str__(self):
        """Return a string representation of the instance."""

    processes = []

    #
    #  Definitions of further methods
    #
