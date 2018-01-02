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

from .... import Explicit


class World (I.World, abstract.World):
    """World entity type mixin implementation class.

    Base component's World mixin that every model must use in composing their
    World class. Inherits from I.World as the interface with all necessary
    variables and parameters.

    """

    def __init__(self,
                 *,
                 environment=None,
                 metabolism=None,
                 culture=None,
                 **kwargs
                 ):
        """Instantiate (typically the only) instance of World.

        Parameters
        ----------
        environment : obj
            Environment acting on this World.
        metabolism : obj
            Metabolism acting on this World.
        culture : obj
            Culture acting on this World.
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        self._environment = None
        self.environment = environment
        self._metabolism = None
        self.metabolism = metabolism
        self._culture = None
        self.culture = culture
        self._social_systems = set()
        self._cells = set()

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
            assert isinstance(n, I.Environment), "Environment must be taxon type Environment"
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
            assert isinstance(m, I.Metabolism), \
                "Metabolism must be of process taxon type Metabolism"
            m._worlds.add(self)
        self._metabolism = m

    @property
    def culture(self):
        """Get world's culture."""
        return self._culture

    @culture.setter
    def culture(self, c):
        """Set world's culture."""
        if self._culture is not None:
            # first deregister from previous culture's list of worlds:
            self._culture.worlds.remove(self)
        if c is not None:
            assert isinstance(c, I.Culture), \
                "Culture must be taxon type Culture"
            c._worlds.add(self)
        self._culture = c

    @property
    def culture(self):
        """Get the Culture acting in this World."""
        return self._culture

    @culture.setter
    def culture(self, c):
        """Set the World the SocialSystem is part of."""
        if self._culture is not None:
            self._culture._worlds.remove(self)
        assert isinstance(c, I.Culture), "culture must be of taxon type Culture"
        c._worlds.add(self)
        self._culture = c

    @property  # read-only
    def social_systems(self):
        """Get the set of all SocialSystems on this World."""
        return self._social_systems

    @property  # read-only
    def top_level_social_systems(self):
        """Get the set of top-level SocialSystems on this World."""
        # find by filtering:
        return set([s for s in self._social_systems
                    if s.next_higher_social_system is None])

    @property  # read-only
    def cells(self):
        """Get the set of Cells on this World."""
        return self._cells

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
        Explicit("aggregate cell carbon stocks",
                 [I.World.terrestrial_carbon,
                  I.World.fossil_carbon],
                 [I.World.sum.cells.terrestrial_carbon,
                  I.World.sum.cells.fossil_carbon])
    ]
