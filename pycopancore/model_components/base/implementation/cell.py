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
from ....private import unknown

# typical imports for implementation classes:
from .. import interface as I
from .... import master_data_model as D


class Cell (I.Cell, abstract.Cell):
    """Cell entity type mixin implementation class.

    Base component's Cell mixin that every model must use in composing their
    Cell class. Inherits from I.Cell as the interface with all necessary
    variables and parameters.

    """

    def __init__(self,
                 *,
                 world=None,
                 social_system=None,
                 **kwargs
                 ):
        """Initialize an instance of Cell.

        Parameters
        ----------
        world : obj
            World the Cell belongs to (the default is None)
        social_system : obj
            SocialSystem the Cell belongs to (the default is None)
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        # init and set variables implemented via properties
        self._world = None
        self._social_system = None
        if world:
            self.world = world
        self.social_system = social_system  # this line must occur after setting world!

        # make sure all variable values are valid:
        self.assert_valid()

        # init other caches:
        self._individuals = set()

        # register with all mandatory networks:
        if self.environment:
            self.environment.geographic_network.add_node(self)


    # getters and setters for references:

    @property
    def world(self):
        """Get the World the Cell is part of."""
        return self._world

    @world.setter
    def world(self, w):
        """Set the World the Cell is part of."""
        if self._world is not None:
            # first deregister from previous world's list of cells:
            self._world.cells.remove(self)
        assert isinstance(w, I.World), "world must be of entity type World"
        w._cells.add(self)
        self._world = w

    @property
    def social_system(self):
        """Get the lowest-level SocialSystem whose territory the Cell is part of."""
        return self._social_system

    @social_system.setter
    def social_system(self, s):
        """Set the lowest-level SocialSystem whose territory the Cell is part of."""
        if self._social_system is not None:
            # first deregister from previous social_system's list of cells:
            self._social_system._direct_cells.remove(self)
            # reset dependent caches:
            self._social_system.cells = unknown
            self._social_system.direct_individuals = unknown
        if s is not None:
            assert isinstance(s, I.SocialSystem), \
                "social_system must be of entity type SocialSystem"
            s._direct_cells.add(self)
            # reset dependent caches:
            s.cells = unknown
            s.direct_individuals = unknown
            self.world = s.world
        self._social_system = s
        # reset dependent caches:
        self.social_systems = unknown

    # getters for backwards references and convenience variables:

    @property  # read-only
    def environment(self):
        """Get the Environment of which the Cell is a part."""
        return self._world.environment

    @property  # read-only
    def metabolism(self):
        """Get the Metabolism of which the Cell is a part."""
        return self._world.metabolism

    @property  # read-only
    def culture(self):
        """Get the Culture of which the Cell is a part."""
        return self._world.culture

    _social_systems = unknown
    """cache, depends on self.social_system, self.social_system.higher_social_systems"""
    @property  # read-only
    def social_systems(self):
        """Get upward list of SocialSystems the Cell belongs to (in)directly."""
        if self._social_systems is unknown:
            self._social_systems = [] if self.social_system is None \
                else [self.social_system] + self.social_system.higher_social_systems
        return self._social_systems

    @social_systems.setter
    def social_systems(self, u):
        """Set upward list of SocialSystems the Cell belongs to (in)directly."""
        assert u == unknown, "setter can only be used to reset cache"
        self._social_systems = unknown
        # reset dependent caches:
        pass

    @property  # read-only
    def individuals(self):
        """Get the Individuals which reside in the Cell."""
        return self._individuals

    # no process-related methods

    processes = []  # no processes in base
