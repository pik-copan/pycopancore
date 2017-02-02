"""Metabolism mixin class template."""

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

from .interface import Metabolism_
from pycopancore.model_components import abstract

#
#  Define class Metabolism
#


class Metabolism(Metabolism_, abstract.Metabolism):
    """Define properties of simple_extraction metabolism.

    Inherits from Metabolism_
    as the interface with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 **kwargs):
        """Initialize an instance of Nature."""
        super(Metabolism, self).__init__(**kwargs)

    def __str__(self):
        """Return a string representation of the instance."""
        return (super().__repr__() +
                ('simple_extraction.metabolism object')
                )

    processes = []

    #
    #  Definitions of further methods
    #
