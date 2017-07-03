""" """

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

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
                 nature=None,
                 metabolism=None,
                 culture=None,
                 population=0 * D.people,
                 **kwargs
                 ):
        """Instantiate (typically the only) instance of World.

        Parameters
        ----------
        nature: obj
            Nature the World is part of.
        metabolism: obj
            Metabolism the World is part of.
        culture: obj
            Culture the Wold is part of.
        population: int
            Population of the World (default is 0).
        **kwargs
            Arbitrary keyword arguments

        """
        super().__init__(**kwargs)  # must be the first line

        if len(self.__class__.instances) > 1:
            raise ValueError('Only one world allowed!')

        self.nature = nature
        self.metabolism = metabolism
        self.culture = culture
        self.population = population

        self._societies = set()
        """ # TODO: docstring """
        self._cells = set()
        """ # TODO: docstring """

    # getters and setters:

    @property  # read-only
    def societies(self):
        """Get the set of all Societies on this World."""
        return self._societies

    @property  # read-only
    def top_level_societies(self):
        """Get the set of top-level Societies on this World."""
        # find by filtering:
        return set([s for s in self._societies
                    if s.next_higher_society is None])

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

    # process-related methods:

    def aggregate_cell_carbon_stocks(self, unused_t):
        """Sum up all carbon stocks of Cells.

        Parameters
        ----------
        unused_t
            A parameter that is not used in the method but necessary for the
            runner.

        """
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
