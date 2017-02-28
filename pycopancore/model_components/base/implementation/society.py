"""base component's Society entity type mixin implementation class"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others:
from pycopancore.model_components import abstract 

from . import interface as I


class Society (I.Society, abstract.Society):
    """Society entity type mixin implementation class.

    Base component's Society mixin that every model must use in composing 
    their Society class. Inherits from Society_ as the interface with all 
    necessary variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 world=None,
                 next_higher_society=None,
                 population=0,
                 **kwargs
                 ):
        """Initialize an instance of Society"""
        super().__init__(**kwargs) # must be the first line

        self.world = world
        self.next_higher_society = next_higher_society
        self.population = population


    # getters and setters:
    
    @property
    def world(self):
        return self._world
    
    @world.setter
    def world(self, w):
        if self._world is not None: self._world._societies.remove(self) 
        if w is not None: 
            assert isinstance(w, I.World), "world must be of entity type World"
            w._societies.add(self) 
        self._world = w

    @property
    def next_higher_society(self):
        return self._next_higher_society
    
    @world.setter
    def next_higher_society(self, s):
        if self._next_higher_society is not None: 
            self._next_higher_society._next_lower_societies.remove(self) 
        if s is not None: 
            assert isinstance(s, I.Society), \
                "world must be of entity type Society"
            s._next_lower_societies.add(self) 
        self._next_higher_society = s

    @property
    def population(self):
        return self._population
    
    @population.setter
    def population(self, p):
        if p is not None: assert p >= 0, "population must be >= 0"
        self._population = p
        
    @property # read-only
    def next_lower_societies(self):
        return self._next_lower_societies

    @property # read-only
    def direct_territory(self):
        return self._direct_territory

    @property # read-only
    def territory(self):
        """aggregate all direct territory of self and all subsocieties"""
        t = self.direct_territory
        for s in self.next_lower_societies: t.union_update(s.territory)
        return t 
    
    @property # read-only
    def direct_citizens(self):
        return self._direct_citizens

    @property # read-only
    def citizens(self):
        """aggregate all direct citizens of self and all subsocieties"""
        c = self.direct_citizens
        for s in self.next_lower_societies: c.union_update(s.citizens)
        return c 
    
    
    # no process-related methods

    processes = []

