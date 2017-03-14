"""Base component's Society entity type mixin implementation class."""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others:
from pycopancore.model_components import abstract
from pycopancore import master_data_model as D

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
                 population = 0 * D.people,
                 **kwargs
                 ):
        """Initialize an instance of Society."""
        super().__init__(**kwargs)  # must be the first line

        self._world = None
        self._next_higher_society = None

        self.world = world
        self.next_higher_society = next_higher_society
        self.population = population

        self._next_lower_societies = set()
        self._direct_cells = set()

    # getters and setters for references:

    @property
    def world(self):
        """Return world."""
        return self._world

    @world.setter
    def world(self, w):
        """Set world."""
        if self._world is not None:
            self._world._societies.remove(self)
        if w is not None:
            assert isinstance(w, I.World), "world must be of entity type World"
            w._societies.add(self)
        self._world = w

    @property
    def next_higher_society(self):
        """Return next higher society."""
        return self._next_higher_society

    @next_higher_society.setter
    def next_higher_society(self, s):
        """Set next higher society."""
        if self._next_higher_society is not None:
            self._next_higher_society._next_lower_societies.remove(self)
        if s is not None:
            assert isinstance(s, I.Society), \
                "next_higher_society must be of entity type Society"
            s._next_lower_societies.add(self)
        self._next_higher_society = s

    # getters for backwards references and convenience variables:
    # TODO: maybe later introduce some redundant storage to improve performance

    @property  # read-only
    def nature(self):
        """Return nature."""
        return self._world.nature

    @property  # read-only
    def metabolism(self):
        """Return metabolism."""
        return self._world.metabolism

    @property  # read-only
    def culture(self):
        """Return culture."""
        return self._world.culture

    @property  # read-only
    def higher_societies(self):
        """Return higher societies."""
        # find by following the ref-chain:
        h = []
        s = self
        while s.next_higher_society is not None:
            s = s.next_higher_society
            h.append(s)
        return h

    @property  # read-only
    def next_lower_societies(self):
        """Read next lower societies."""
        return self._next_lower_societies

    @property  # read-only
    def lower_societies(self):
        """Return lower societies."""
        # aggregate recursively:
        l = self._next_lower_societies
        for s in self._next_lower_societies:
            l.update(s.lower_societies)
        return l

    @property  # read-only
    def direct_cells(self):
        """Return direct cells."""
        return self._direct_cells

    @property  # read-only
    def cells(self):
        """Return cells."""
        # aggregate recursively:
        c = self.direct_cells
        for s in self._next_lower_societies:
            c.update(s.cells)
        return c

    @property  # read-only
    def direct_individuals(self):
        """Return direct individuals."""
        # aggregate from direct_cells:
        i = set()
        for c in self._direct_cells:
            i.update(c.individuals)
        return i

    @property  # read-only
    def individuals(self):
        """Return individuals."""
        # aggregate from cells:
        i = set()
        for c in self.cells:
            i.update(c.individuals)
        return i

    # TODO: helper methods for mergers, splits, etc.

    # no process-related methods

    processes = []
