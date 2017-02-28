"""base component's Culture process taxon mixin implementation class"""


# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore.model_components import abstract # only used in this component, not in others
from . import interface as I


class Culture (I.Culture, abstract.Culture):
    """Define properties of base.culture.

    Basic Culture mixin class that every model must use in composing their
    Culture class. Inherits from Culture_ as the interface with all necessary
    variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 *,
                 basic_social_network=None,
                 **kwargs
                 ):
        """Initialize the unique instance of Culture"""
        super().__init__(**kwargs)

        self.basic_social_network = basic_social_network

