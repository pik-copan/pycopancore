"""base component's Nature process taxon mixin implementation class"""

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

from pycopancore.model_components import abstract # only used in this component, not in others
from .interface import Nature_

#
#  Define class Cell
#


class Nature (Nature_, abstract.Nature):
    """Define properties of the nature class.

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
        """Initialize the unique instance of Nature.

        Parameters
        ----------
        kwargs:
        """
        super(Nature, self).__init__(**kwargs)
        pass

    def __repr__(self):
        """Return a string representation of the object of base.Nature."""
        return (super().__repr__() +
                'base.nature object'
                )

    def __str__(self):
        """Return a readable representation of the object of base.Nature."""
        return (super().__str__() +
                'base.nature object'
                )

    processes = []

    #
    #  Definitions of further methods
    #
