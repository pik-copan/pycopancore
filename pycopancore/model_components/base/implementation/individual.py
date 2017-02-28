"""base component's Individual entity type mixin implementation class"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others
from pycopancore.model_components import abstract
from . import interface as I


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
                 **kwargs
                 ):
        """Initialize an instance of Individual"""
        super().__init__(**kwargs) # must be the first line

        self.cell = cell

        self.world.culture.basic_social_network.add_node(self)

    def deactivate(self):
        """Deactivate an individual."""
        self.world.culture.basic_social_network.remove_node(self)
        super().deactivate() # must be the last line

    def reactivate(self):
        """Reactivate an individual."""
        super().reactivate() # must be the first line
        self.world.culture.basic_social_network.add_node(self)


    # getters and setters:
    
    @property
    def world(self):
        return self._world
    
    @world.setter
    def world(self, w):
        if self._world is not None: self._world.individuals.remove(self) 
        if w is not None: 
            assert isinstance(w, World_), "world must be of entity type World"
            w._individuals.add(self) 
        self._world = w
        
    @property
    def cell(self):
        return self._cell
    
    @residence.setter
    def cell(self, c):
        if self._cell is not None: self._cell._individuals.remove(self) 
        if c is not None: 
            assert isinstance(c, Cell_), "cell must be of entity type Cell"
            c._individuals.add(self) 
        self._cell = c

    @property
    def population_share(self):
        total_relative_weight = sum([i.relative_weight
                                     for i in c.individuals 
                                     for c in self.cell.society.cells])
        return self.relative_weight / total_relative_weight

    @property
    def represented_population(self):
        return self.population_share * self.cell.society.population


    # no process-related methods

    processes = []
