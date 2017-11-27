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
from .... import master_data_model as D
from ....private import unknown

from .. import interface as I


class SocialSystem (I.SocialSystem, abstract.SocialSystem):
    """SocialSystem entity type mixin implementation class.

    Base component's SocialSystem mixin that every model must use in composing
    their SocialSystem class. Inherits from I.SocialSystem as the interface with all
    necessary variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 world,
                 next_higher_social_system=None,
                 **kwargs
                 ):
        """Initialize an instance of SocialSystem.

        Parameters
        ----------
        world: obj
            World the SocialSystem belongs to (default is None)
        next_higher_social_system: obj
            Optional SocialSystem the SocialSystem belongs to (default is None)
        population: int
            Number of people residing in the SocialSystem's territory
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        # init caches:
        self._next_lower_social_systems = set()
        self._direct_cells = set()

        # init and set variables implemented via properties:
        self._world = None
        self.world = world
        self._next_higher_social_system = None
        self.next_higher_social_system = next_higher_social_system

    # getters and setters for references:

    @property
    def world(self):
        """Get the World the SocialSystem is part of."""
        return self._world

    @world.setter
    def world(self, w):
        """Set the World the SocialSystem is part of."""
        if self._world is not None:
            self._world._social_systems.remove(self)
        assert isinstance(w, I.World), "world must be of entity type World"
        w._social_systems.add(self)
        self._world = w

    @property
    def next_higher_social_system(self):
        """Get next higher social_system."""
        return self._next_higher_social_system

    @next_higher_social_system.setter
    def next_higher_social_system(self, s):
        """Set next higher social_system."""
        if self._next_higher_social_system is not None:
            self._next_higher_social_system._next_lower_social_systems.remove(self)
            # reset dependent cache:
            self._next_higher_social_system.cells = unknown
        if s is not None:
            assert isinstance(s, I.SocialSystem), \
                "next_higher_social_system must be of entity type SocialSystem"
            s._next_lower_social_systems.add(self)
            # reset dependent cache:
            s.cells = unknown
        self._next_higher_social_system = s
        # reset dependent caches:
        self.higher_social_systems = unknown

    # getters for backwards references and convenience variables:

    @property  # read-only
    def environment(self):
        """Get the Environment of which the SocialSystem is a part."""
        return self._world.environment

    @property  # read-only
    def metabolism(self):
        """Get the Metabolism of which the SocialSystem is a part."""
        return self._world.metabolism

    @property  # read-only
    def culture(self):
        """Get the Culture of which the SocialSystem is a part."""
        return self._world.culture

    _higher_social_systems = unknown
    """cache, depends on self.next_higher_social_system
    and self.next_higher_social_system.higher_social_systems"""
    @property  # read-only
    def higher_social_systems(self):
        """Get higher social_systems."""
        if self._higher_social_systems is unknown:
            # find recursively:
            self._higher_social_systems = [] if self.next_higher_social_system is None \
                else ([self.next_higher_social_system]
                      + self.next_higher_social_system.higher_social_systems)
        return self._higher_social_systems

    @higher_social_systems.setter
    def higher_social_systems(self, u):
        """Set higher social_systems."""
        assert u == unknown, "setter can only be used to reset cache"
        self._higher_social_systems = unknown
        # reset dependent caches:
        for s in self._next_lower_social_systems:
            s.higher_social_systems = unknown
        for c in self._direct_cells:
            c.social_systems = unknown

    @property  # read-only
    def next_lower_social_systems(self):
        """Get next lower social_systems."""
        return self._next_lower_social_systems

    @property  # read-only
    def lower_social_systems(self):
        """Get lower social_systems."""
        # aggregate recursively:
        l = self._next_lower_social_systems
        for s in self._next_lower_social_systems:
            l.update(s.lower_social_systems)
        return l

    @property  # read-only
    def direct_cells(self):
        """Get cells that directly belong to the SocialSystem."""
        return self._direct_cells

    _cells = unknown
    """cache, depends on self.direct_cells, self._next_lower_social_systems,
    and lowersocial_system.cells"""
    @property  # read-only
    def cells(self):
        """Get cells that directly abd indirectly belong to the SocialSystem."""
        if self._cells is unknown:
            # aggregate recursively:
            self._cells = self.direct_cells
            for s in self._next_lower_social_systems:
                self._cells.update(s.cells)
        return self._cells

    @cells.setter
    def cells(self, u):
        """Set cells that directly and indirectly belong to the SocialSystem."""
        assert u == unknown, "setter can only be used to reset cache"
        self._cells = unknown
        # reset dependent caches:
        if self.next_higher_social_system is not None:
            self.next_higher_social_system.cells = unknown

    _direct_individuals = unknown
    """cache, depends on _direct_cells, directcell.individuals"""
    @property  # read-only
    def direct_individuals(self):
        """Get resident Individuals not in subsocial_systems."""
        if self._direct_individuals is unknown:
            # aggregate from direct_cells:
            self._direct_individuals = set()
            for c in self._direct_cells:
                self._direct_individuals.update(c.individuals)
        return self._direct_individuals

    @direct_individuals.setter
    def direct_individuals(self, u):
        """Set resident Individuals not in subsocial_systems."""
        assert u == unknown, "setter can only be used to reset cache"
        self._direct_individuals = unknown
        # reset dependent caches:
        pass

    _individuals = unknown
    """cache, depends on self.cells, cell.individuals"""
    @property  # read-only
    def individuals(self):
        """Get direct and indirect resident Individuals."""
        if self._individuals is unknown:
            # aggregate from cells:
            self._individuals = set()
            for c in self.cells:
                self._individuals.update(c.individuals)
        return self._individuals

    @individuals.setter
    def individuals(self, u):
        """Set direct and indirect resident Individuals."""
        assert u == unknown, "setter can only be used to reset cache"
        self._individuals = unknown
        # reset dependent caches:
        pass

    # TODO: helper methods for mergers, splits, etc.

    # no process-related methods

    processes = []  # no processes in base
