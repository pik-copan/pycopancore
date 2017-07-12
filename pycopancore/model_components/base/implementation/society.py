""" """

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others:
from ... import abstract
from .... import master_data_model as D
from ....private import unknown

from .. import interface as I


class Society (I.Society, abstract.Society):
    """Society entity type mixin implementation class.

    Base component's Society mixin that every model must use in composing
    their Society class. Inherits from I.Society as the interface with all
    necessary variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 world=None,
                 next_higher_society=None,
                 population=0 * D.people, # FIXME: Is the 0 correct?
                 **kwargs
                 ):
        """Initialize an instance of Society.

        Parameters
        ----------
        world: obj
            World the Society belongs to (default is None)
        next_higher_society: obj
            Optional Society the Society belongs to (default is None)
        population: int
            Number of people residing in the Society's territory
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        # init caches:
        self._next_lower_societies = set()
        self._direct_cells = set()

        # init and set variables implemented via properties:
        self._world = None
        self.world = world
        self._next_higher_society = None
        self.next_higher_society = next_higher_society

        # set other variables:
        self.population = population

        # make sure all variable values are valid:
        self.assert_valid()

    # getters and setters for references:

    @property
    def world(self):
        """Get the World the Society is part of."""
        return self._world

    @world.setter
    def world(self, w):
        """Set the World the Society is part of."""
        if self._world is not None:
            self._world._societies.remove(self)
        if w is not None:
            assert isinstance(w, I.World), "world must be of entity type World"
            w._societies.add(self)
        self._world = w

    @property
    def next_higher_society(self):
        """Get next higher society."""
        return self._next_higher_society

    @next_higher_society.setter
    def next_higher_society(self, s):
        """Set next higher society."""
        if self._next_higher_society is not None:
            self._next_higher_society._next_lower_societies.remove(self)
            # reset dependent cache:
            self._next_higher_society.cells = unknown
        if s is not None:
            assert isinstance(s, I.Society), \
                "next_higher_society must be of entity type Society"
            s._next_lower_societies.add(self)
            # reset dependent cache:
            s.cells = unknown
        self._next_higher_society = s
        # reset dependent caches:
        self.higher_societies = unknown

    # getters for backwards references and convenience variables:

    @property  # read-only
    def nature(self):
        """Get the Nature of which the Society is a part."""
        return self._world.nature

    @property  # read-only
    def metabolism(self):
        """Get the Metabolism of which the Society is a part."""
        return self._world.metabolism

    @property  # read-only
    def culture(self):
        """Get the Culture of which the Society is a part."""
        return self._world.culture

    _higher_societies = unknown
    """cache, depends on self.next_higher_society
    and self.next_higher_society.higher_societies"""
    @property  # read-only
    def higher_societies(self):
        """Get higher societies."""
        if self._higher_societies is unknown:
            # find recursively:
            self._higher_societies = [] if self.next_higher_society is None \
                else ([self.next_higher_society]
                      + self.next_higher_society.higher_societies)
        return self._higher_societies

    @higher_societies.setter
    def higher_societies(self, u):
        """Set higher societies."""
        assert u == unknown, "setter can only be used to reset cache"
        self._higher_societies = unknown
        # reset dependent caches:
        for s in self._next_lower_societies:
            s.higher_societies = unknown
        for c in self._direct_cells:
            c.societies = unknown

    @property  # read-only
    def next_lower_societies(self):
        """Get next lower societies."""
        return self._next_lower_societies

    @property  # read-only
    def lower_societies(self):
        """Get lower societies."""
        # aggregate recursively:
        l = self._next_lower_societies
        for s in self._next_lower_societies:
            l.update(s.lower_societies)
        return l

    @property  # read-only
    def direct_cells(self):
        """Get cells that directly belong to the Society."""
        return self._direct_cells

    _cells = unknown
    """cache, depends on self.direct_cells, self._next_lower_societies,
    and lowersociety.cells"""
    @property  # read-only
    def cells(self):
        """Get cells that directly abd indirectly belong to the Society."""
        if self._cells is unknown:
            # aggregate recursively:
            self._cells = self.direct_cells
            for s in self._next_lower_societies:
                self._cells.update(s.cells)
        return self._cells

    @cells.setter
    def cells(self, u):
        """Set cells that directly and indirectly belong to the Society."""
        assert u == unknown, "setter can only be used to reset cache"
        self._cells = unknown
        # reset dependent caches:
        if self.next_higher_society is not None:
            self.next_higher_society.cells = unknown

    _direct_individuals = unknown
    """cache, depends on _direct_cells, directcell.individuals"""
    @property  # read-only
    def direct_individuals(self):
        """Get resident Individuals not in subsocieties."""
        if self._direct_individuals is unknown:
            # aggregate from direct_cells:
            self._direct_individuals = set()
            for c in self._direct_cells:
                self._direct_individuals.update(c.individuals)
        return self._direct_individuals

    @direct_individuals.setter
    def direct_individuals(self, u):
        """Set resident Individuals not in subsocieties."""
        assert u == unknown, "setter can only be used to reset cache"
        self._direct_individuals = unknown
        # reset dependent caches:
        pass

    _individuals = unknown
    """cache, depends on self.cells, cell.individuals"""
    @property  # read-only
    def individuals(self):
        """Get direct abd indirect resident Individuals."""
        if self._individuals is unknown:
            # aggregate from cells:
            self._individuals = set()
            for c in self.cells:
                self._individuals.update(c.individuals)
        return self._individuals

    @individuals.setter
    def individuals(self, u):
        """Set direct abd indirect resident Individuals."""
        assert u == unknown, "setter can only be used to reset cache"
        self._individuals = unknown
        # reset dependent caches:
        pass

    # TODO: helper methods for mergers, splits, etc.

    # no process-related methods

    processes = []  # no processes in base
