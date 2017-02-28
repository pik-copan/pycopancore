"""base component's Individual entity type mixin implementation class"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others
from pycopancore.model_components import abstract

from .. import interface as I


class Individual (I.Individual, abstract.Individual):
    """Individual entity type mixin implementation class.

    Base component's Individual mixin that every model must use in composing
    their Individual class. Inherits from Individual as the interface with all
    necessary variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 cell=None,
                 relative_weight=1,
                 **kwargs
                 ):
        """Initialize an instance of Individual"""
        super().__init__(**kwargs)  # must be the first line

        self._cell = None

        self.cell = cell
        self.relative_weight = relative_weight

        self.culture.acquaintance_network.add_node(self)

    def deactivate(self):
        """Deactivate an individual."""
        self.culture.acquaintance_network.remove_node(self)
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate an individual."""
        super().reactivate()  # must be the first line
        self.culture.acquaintance_network.add_node(self)

    # getters and setters for references:

    @property
    def cell(self):
        return self._cell

    @cell.setter
    def cell(self, c):
        if self._cell is not None:
            self._cell._individuals.remove(self)
        if c is not None:
            assert isinstance(c, I.Cell), "cell must be of entity type Cell"
            c._individuals.add(self)
        self._cell = c

    # getters for backwards references and convenience variables:

    @property  # read-only
    def world(self):
        return self._cell.world

    @property  # read-only
    def nature(self):
        return self._cell.nature

    @property  # read-only
    def metabolism(self):
        return self._cell.metabolism

    @property  # read-only
    def culture(self):
        return self._cell.culture

    @property  # read-only
    def society(self):
        return self._cell.society

    @property  # read-only
    def societies(self):
        return self._cell.societies

    @property
    def population_share(self):
        total_relative_weight = sum([i.relative_weight
                                     for i in self.society.individuals])
        return self.relative_weight / total_relative_weight

    @property
    def represented_population(self):
        return self.population_share * self.society.human_population

    @property
    def acquaintances(self):
        return self.culture.acquaintance_network.neighbors(self)

    # no process-related methods

    processes = []
