"""base component's Metabolism process taxon mixin implementation class"""


# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore.model_components import abstract # only used in this component, not in others
from .interface import Metabolism_


class Metabolism (Metabolism_, abstract.Metabolism):
    """Define properties of the base.metabolism.

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
        """Initialize the unique instance of Metabolism.

        Parameters
        ----------
        kwargs:
        """
        super(Metabolism, self).__init__(**kwargs)
        pass

    def __repr__(self):
        """Return a string representation of the object of base.Metabolism."""
        return (super().__repr__() +
                'base.metabolism'
                )

    def __str__(self):
        """Return a readable representation of the object."""
        return (super().__str__() +
                'base.metabolism'
                )

    processes = []

    #
    #  Definitions of further methods
    #
