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

from networkx import DiGraph, Graph

from pycopancore.model_components import abstract
from pycopancore.private._simple_expressions import unknown
from pycopancore.process_types import Explicit

from .. import interface as Interface


class World(Interface.World, abstract.World):
    """World entity type mixin implementation class.

    Base component's World mixin that every model must use in composing their
    World class. Inherits from Interface.World as the interface with all
    necessary variables and parameters.

    """

    def __init__(
        self,
        *,
        environment=None,
        metabolism=None,
        acquaintance_network=None,
        group_membership_network=None,
        **kwargs,
    ):
        """Instantiate (typically the only) instance of World.

        Parameters
        ----------
        environment : obj
            Environment acting on this World.
        metabolism : obj
            Metabolism acting on this World.
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

        self._environment = None
        self.environment = environment
        self._metabolism = None
        self.metabolism = metabolism
        self._social_systems = set()
        self._cells = set()
        self._groups = set()

        # make sure all variable values are valid:
        self.assert_valid()

    # getters and setters:
    @property
    def environment(self):
        """Get world's environment."""
        return self._environment

    @environment.setter
    def environment(self, n):
        """Set world's environment."""
        if self._environment is not None:
            # first deregister from previous environment's list of worlds:
            self._environment.worlds.remove(self)
        if n is not None:
            assert isinstance(
                n, Interface.Environment
            ), "Environment must be taxon type Environment"
            n._worlds.add(self)
        self._environment = n

    @property
    def metabolism(self):
        """Get the World the Cell is part of."""
        return self._metabolism

    @metabolism.setter
    def metabolism(self, m):
        """Set the Metabolism the World is part of."""
        if self._metabolism is not None:
            # first deregister from previous metabolism's list of worlds:
            self._metabolism.worlds.remove(self)
        if m is not None:
            assert isinstance(
                m, Interface.Metabolism
            ), "Metabolism must be of process taxon type Metabolism"
            m._worlds.add(self)
        self._metabolism = m

    @property  # read-only
    def social_systems(self):
        """Get the set of all SocialSystems on this World."""
        return self._social_systems

    @property  # read-only
    def top_level_social_systems(self):
        """Get the set of top-level SocialSystems on this World."""
        # find by filtering:
        return set(
            [
                s
                for s in self._social_systems
                if s.next_higher_social_system is None
            ]
        )

    @property  # read-only
    def cells(self):
        """Get the set of Cells on this World."""
        return self._cells

    @property  # read-only
    def groups(self):
        """Get the set of Groups on this World."""
        return self._groups

    _individuals = unknown
    """cache, depends on self.cells, cell.individuals"""

    @property  # read-only
    def individuals(self):
        """Get and set the set of Individuals residing on this World."""
        if self._individuals is unknown:
            # aggregate from cells:
            self._individuals = set()
            for c in self.cells:
                self._individuals.update(c.individuals)
        return self._individuals

    @individuals.setter
    def individuals(self, u):
        assert u == unknown, "setter can only be used to reset cache"
        self._individuals = unknown
        # reset dependent caches:
        pass

    processes = [
        # TODO: convert this into an Implicit equation once supported:
        Explicit(
            "aggregate cell carbon stocks",
            [
                Interface.World.terrestrial_carbon,
                Interface.World.fossil_carbon,
            ],
            [
                Interface.World.sum.cells.terrestrial_carbon,
                Interface.World.sum.cells.fossil_carbon,
            ],
        )
    ]
