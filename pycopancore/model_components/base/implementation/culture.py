""" """

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from networkx import DiGraph, Graph

# only used in this component, not in others:
from pycopancore.model_components import abstract
from pycopancore.private._simple_expressions import unknown

from .. import interface as Interface


class Culture(Interface.Culture, abstract.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:

    def __init__(
        self,
        *,
        acquaintance_network=None,
        group_membership_network=None,
        **kwargs,
    ):
        """Initialize the unique instance of Culture.

        Parameters
        ----------
        acquaintance_network: Graph
            The Network of acquaintances which is managed by Culture
            (default is None)
        group_membership_network: DiGraph
            The Network between Individiuals and groups, which is managed
            by Culture (default is None)
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        if acquaintance_network is None:
            acquaintance_network = Graph()
        assert isinstance(acquaintance_network, Graph)
        self.acquaintance_network = acquaintance_network

        if group_membership_network is None:
            group_membership_network = DiGraph()
        assert isinstance(group_membership_network, DiGraph)
        self.group_membership_network = group_membership_network

        self._worlds = set()
        self._groups = set()

        # make sure all variable values are valid:
        self.assert_valid()

    # getters and setters:
    @property  # read-only
    def worlds(self):
        """Get the set of all Worlds this Culture acts in."""
        return self._worlds

    _individuals = unknown
    """cache, depends on self.worlds, world.individuals"""

    @property  # read-only
    def individuals(self):
        """Get and set the set of Individuals governed by this Culture."""
        if self._individuals is unknown:
            # aggregate from worlds:
            self._individuals = set()
            for w in self.worlds:
                self._individuals.update(w.individuals)
        return self._individuals

    @individuals.setter
    def individuals(self, u):
        assert u == unknown, "setter can only be used to reset cache"
        self._individuals = unknown
        # reset dependent caches:
        pass

    _social_systems = unknown
    """cache, depends on self.worlds, world.social_systems"""

    @property  # read-only
    def social_systems(self):
        """Get and set the set of SocialSystems governed by this Culture."""
        if self._social_systems is unknown:
            # aggregate from worlds:
            self._social_systems = set()
            for w in self.worlds:
                self._social_systems.update(w.social_systems)
        return self._social_systems

    @social_systems.setter
    def social_systems(self, u):
        assert u == unknown, "setter can only be used to reset cache"
        self._social_systems = unknown
        # reset dependent caches:
        pass

    @property  # read-only
    def groups(self):
        """Get the set of all Groups in this Culture."""
        return self._groups

    # no process-related methods

    processes = []  # no processes in base
