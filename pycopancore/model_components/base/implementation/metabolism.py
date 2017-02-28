"""base component's Metabolism process taxon mixin implementation class"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others:
from pycopancore.model_components import abstract

from .. import interface as I


class Metabolism (I.Metabolism, abstract.Metabolism):
    """Metabolism process taxon mixin implementation class"""

    # standard methods:

    def __init__(self,
                 #*,
                 **kwargs):
        """Initialize the unique instance of Metabolism."""
        super().__init__(**kwargs)  # must be the first line
        # TODO: add custom code here:
        pass

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
