""" """

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# only used in this component, not in others:
from ... import abstract

from .. import interface as I

from networkx import Graph


class Culture (I.Culture, abstract.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 acquaintance_network=None,
                 **kwargs):
        """Initialize the unique instance of Culture.

        Parameters
        ----------
        acquaintance_network: Graph
            The Network of acquaintances which is managed by Culture
            (default is None)
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        if acquaintance_network is None:
            acquaintance_network = Graph()
        assert isinstance(acquaintance_network, Graph)
        self.acquaintance_network = acquaintance_network
        self._worlds = set()

        self._worlds = set()

        # make sure all variable values are valid:
        self.assert_valid()

    # getters and setters:
    @property  # read-only
    def worlds(self):
        """Get the set of all Worlds this Culture acts in."""
        return self._worlds

    # no process-related methods

    processes = []  # no processes in base
