"""Base component's Cell entity type mixin implementation class."""

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


class Cell (I.Cell, abstract.Cell):
    """Cell entity type mixin implementation class.

    Base component's Cell mixin that every model must use in composing their
    Cell class. Inherits from I.Cell as the interface with all necessary
    variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 world=None,
                 society=None,
                 location=None,
                 land_area = 1 * D.square_kilometers,
                 geometry=None,
                 **kwargs
                 ):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)  # must be the first line

        self._world = None
        self._society = None

        self.world = world
        self.society = society  # must be after setting world!
        self.location = location
        self.land_area = land_area
        self.geometry = geometry

        self._individuals = set()

    # getters and setters for references:

    @property
    def world(self):
        """Return world."""
        return self._world

    @world.setter
    def world(self, w):
        """Set world."""
        if self._world is not None:
            self._world.cells.remove(self)
        if w is not None:
            assert isinstance(w, I.World), "world must be of entity type World"
            w._cells.add(self)
        self._world = w

    @property
    def society(self):
        """Return society."""
        return self._society

    @society.setter
    def society(self, s):
        """Set society."""
        if self._society is not None:
            self._society._direct_cells.remove(self)
        if s is not None:
            assert isinstance(s, I.Society), \
                "society must be of entity type Society"
            s._direct_cells.add(self)
            self.world = s.world
        self._society = s

    # getters for backwards references and convenience variables:

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
    def societies(self):
        """Return societies."""
        return [] if self.society is None \
            else [self.society] + self.society.higher_societies

    @property  # read-only
    def individuals(self):
        """Return individuals."""
        return self._individuals

    # no process-related methods

    processes = []
