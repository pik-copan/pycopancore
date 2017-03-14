"""Base component's Nature process taxon mixin implementation class."""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others:
from ... import abstract

from .. import interface as I

from networkx import Graph


class Nature (I.Nature, abstract.Nature):
    """Nature process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 geographic_network=None,
                 **kwargs):
        """Initialize the unique instance of Nature."""
        super().__init__(**kwargs)  # must be the first line

        if geographic_network is None:
            geographic_network = Graph()
        self.geographic_network = geographic_network


    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
