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


class Group (I.Group, abstract.Group):
    """Gropp entity type mixin implementation class.

    Base component's Group mixin that every model must use in composing
    their Group class. Inherits from I.Group as the interface with all
    necessary variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 social_system,
                 next_higher_group=None,
                 **kwargs
                 ):
        """Initialize an instance of Group.

        Parameters
        ----------
        socialsystem: obj
            SocialSystem the Group belongs to (default is None)
        next_higher_group: obj
            Optional Group the Group belongs to (default is None)
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        # init and set variables implemented via properties:
        self._social_system = None
        self.social_system = social_system
        self._next_higher_group = None
        self.next_higher_group = next_higher_group

        # init caches:
        self._next_lower_group = set()
        self._direct_cells = set()



    # getters and setters for references:

    @property
    def social_system(self):
        """Get the World the SocialSystem is part of."""
        return self._social_system

    @social_system.setter
    def social_system(self, s):
        """Set the World the SocialSystem is part of."""
        if self._social_system is not None:
            self._social_system._groups.remove(self)
        assert isinstance(s, I.SocialSystem), "socialsystem must be of entity type SocialSystem"
        s._groups.add(self)
        self._social_system = s

    @property
    def next_higher_group(self):
        """Get next higher group."""
        return self._next_higher_group

    @next_higher_group.setter
    def next_higher_group(self, s):
        """Set next higher group."""
        if self._next_higher_group is not None:
            self._next_higher_group._next_lower_groups.remove(self)
            # reset dependent cache:
            self._next_higher_group.cells = unknown
        if s is not None:
            assert isinstance(s, I.Group), \
                "next_higher_group must be of entity type group"
            s._next_lower_groups.add(self)
            # reset dependent cache:
            s.cells = unknown
        self._next_higher_group = s
        # reset dependent caches:
        self.higher_groups = unknown

    # getters for backwards references and convenience variables:

    @property  # read-only
    def environment(self):
        """Get the Environment of which the Group is a part."""
        return self._world.environment

    @property  # read-only
    def metabolism(self):
        """Get the Metabolism of which the Group is a part."""
        return self._world.metabolism

    @property  # read-only
    def culture(self):
        """Get the Culture of which the Group is a part."""
        return self._world.culture

    _higher_groups = unknown
    """cache, depends on self.next_higher_group
    and self.next_higher_group.higher_groups"""
    @property  # read-only
    def higher_groups(self):
        """Get higher groups."""
        if self._higher_groups is unknown:
            # find recursively:
            self._higher_groups = [] if self.next_higher_group is None \
                else ([self.next_higher_group]
                      + self.next_higher_group.groups)
        return self._higher_groups

    @higher_groups.setter
    def higher_groups(self, u):
        """Set higher groups."""
        assert u == unknown, "setter can only be used to reset cache"
        self._higher_groups = unknown
        # reset dependent caches:
        for s in self._next_lower_groups:
            s.higher_groups = unknown
        for c in self._direct_cells:
            c.groups = unknown

    @property  # read-only
    def next_lower_groups(self):
        """Get next lower groups."""
        return self._next_lower_groups

    @property  # read-only
    def lower_groups(self):
        """Get lower groups."""
        # aggregate recursively:
        l = self._next_lower_groups
        for s in self._next_lower_groups:
            l.update(s.lower_groups)
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


