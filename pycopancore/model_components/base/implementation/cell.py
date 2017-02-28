"""base component's Cell entity type mixin implementation class"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore.model_components import abstract # only used in this component, not in others
from . import interface as I


class Cell (I.Cell, abstract.Cell):
    """Cell entity type mixin implementation class.

    Base component's Cell mixin that every model must use in composing their Cell
    class. Inherits from Cell_ as the interface with all necessary variables
    and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 world=None,
                 society=None,
                 location=None,
                 area=0,
                 geometry=None,
                 **kwargs
                 ):
        """Initialize an instance of Cell"""
        super().__init__(**kwargs) # must be the first line

        self.world = world
        self.society = society
        self.location = location
        self.area = area
        self.geometry = geometry

        self.residents = set()


    # getters and setters:
    
    @property
    def world(self):
        return self._world
    
    @world.setter
    def world(self, w):
        if self._world is not None: self._world.cells.remove(self) 
        if w is not None: 
            assert isinstance(w, I.World), "world must be of entity type World"
            w._cells.add(self) 
        self._world = w
        
    @property
    def society(self):
        return self._society
    
    @territory_of.setter
    def society(self, s):
        if self._society is not None: self._society._cells.remove(self) 
        if s is not None: 
            assert isinstance(s, I.Society), \
                "society must be of entity type Society"
            s._cells.add(self) 
        self._society = s
        
    @property
    def area(self):
        return self._area
    
    @area.setter
    def area(self, a):
        if a is not None: assert a >= 0, "area must be >= 0"
        self._area = a
        
    @property # read-only
    def residents(self):
        return self._residents
    
    
    # no process-related methods

    processes = []
