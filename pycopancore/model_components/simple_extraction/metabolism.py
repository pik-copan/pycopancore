"""Metabolism mixin class template."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from . import interface as I
from pycopancore.model_components import abstract


class Metabolism(I.Metabolism, abstract.Metabolism):
    """Define properties of simple_extraction metabolism.

    Inherits from I.Metabolism
    as the interface with all necessary variables and parameters.
    """

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
