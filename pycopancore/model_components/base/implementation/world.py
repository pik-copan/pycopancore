"""Base component's World entity type mixin implementation class."""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others:
from pycopancore.model_components import abstract
from pycopancore import master_data_model as D

from .. import interface as I
from pycopancore import Explicit


class World (I.World, abstract.World):
    """World entity type mixin implementation class.

    Base component's World mixin that every model must use in composing their
    World class. Inherits from I.World as the interface with all necessary
    variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 nature=None,
                 metabolism=None,
                 culture=None,
                 population = 0 * D.people,
                 **kwargs
                 ):
        """Initialize an (typically the only) instance of World."""
        super().__init__(**kwargs)  # must be the first line

        if len(self.__class__.instances) > 1:
            raise ValueError('Only one world allowed!')

        self.nature = nature
        self.metabolism = metabolism
        self.culture = culture
        self.population = population

        self._societies = set()
        self._cells = set()

    # getters and setters:

    @property  # read-only
    def societies(self):
        """Return societies of world."""
        return self._societies

    @property  # read-only
    def top_level_societies(self):
        """Return top level society of world."""
        # find by filtering:
        return set([s for s in self._societies
                    if s.next_higher_society is None])

    @property  # read-only
    def cells(self):
        """Return cells of world."""
        return self._cells

    # TODO: use a cache (and last_modified dates) to speed up this and similar
    # aggregations:
    @property  # read-only
    def individuals(self):
        """Return individuals of world."""
        # find indirectly via cells:
        r = set()
        for c in self._cells:
            r.update(c.individuals)
        return r

    # process-related methods:

    def aggregate_cell_carbon_stocks(self, unused_t):
        cs = self.cells
        self.terrestrial_carbon = sum([c.terrestrial_carbon for c in cs])
        self.fossil_carbon = sum([c.fossil_carbon for c in cs])

    processes = [
                 # TODO: convert this into an Implicit equation once supported:
                 Explicit("aggregate cell carbon stocks",
                          [I.World.terrestrial_carbon,
                           I.World.fossil_carbon],
                          aggregate_cell_carbon_stocks)
                 ]
