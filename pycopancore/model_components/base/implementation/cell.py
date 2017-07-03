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


class Cell (I.Cell, abstract.Cell):
    """Cell entity type mixin implementation class.

    Base component's Cell mixin that every model must use in composing their
    Cell class. Inherits from I.Cell as the interface with all necessary
    variables and parameters.

    """

    def __init__(self,
                 *,
                 world=None,
                 society=None,
                 location=None,
                 land_area=1 * D.square_kilometers,
                 geometry=None,
                 **kwargs
                 ):
        """Initialize an instance of Cell.

        Parameters
        ----------
        world: obj
            Instance of World to that the cell obj is assigned
        society: obj
            Instance of Society to that cell obj is assigned
        location: # TODO
            Location of cell object
        land_area: float
            Area of cell object
        geometry: # TODO
            Geometry of cell object

        """
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
        """Get and set the world object cell is assigned to.

        # TODO: Probably a closer detailed documentation of getter and setter.
        Doc-string should only be in the getter.

        """
        return self._world

    @world.setter
    def world(self, w):
        if self._world is not None:
            self._world.cells.remove(self)
        if w is not None:
            assert isinstance(w, I.World), "world must be of entity type World"
            w._cells.add(self)
        self._world = w

    @property
    def society(self):
        """Get and set the society object cell is assigned to.

        # TODO: Probably a closer detailed documentation of getter and setter.
        Doc-string should only be in the getter.

        """
        return self._society

    @society.setter
    def society(self, s):
        if self._society is not None:
            self._society._direct_cells.remove(self)
            # reset dependent caches:
            self._society.cells = unknown
            self._society.direct_individuals = unknown
        if s is not None:
            assert isinstance(s, I.Society), \
                "society must be of entity type Society"
            s._direct_cells.add(self)
            # reset dependent caches:
            s.cells = unknown
            s.direct_individuals = unknown
            self.world = s.world
        self._society = s
        # reset dependent caches:
        self.societies = unknown

    # getters for backwards references and convenience variables:

    @property  # read-only
    def nature(self):
        """Get the nature object cell is referenced to."""
        return self._world.nature

    @property  # read-only
    def metabolism(self):
        """Get the metabolism object cell is referenced to."""
        return self._world.metabolism

    @property  # read-only
    def culture(self):
        """Get the culture object cell is referenced to."""
        return self._world.culture

    _societies = unknown
    # TODO: should the following comment be a doc-string comment?
    """cache, depends on self.society, self.society.higher_societies"""
    @property  # read-only
    def societies(self):
        """Get and set societies the cell is assigned to.

        # TODO: Probably a closer detailed documentation of getter and setter.
        Doc-string should only be in the getter.

        """
        if self._societies is unknown:
            self._societies = [] if self.society is None \
                else [self.society] + self.society.higher_societies
        return self._societies

    @societies.setter
    def societies(self, u):
        assert u == unknown, "setter can only be used to reset cache"
        self._societies = unknown
        # reset dependent caches:
        pass

    @property  # read-only
    def individuals(self):
        """Get individuals the cell object is referenced to

        # TODO: Probably a closer detailed documentation of getter and setter.
        Doc-string should only be in the getter.

        """
        return self._individuals

    # no process-related methods

    processes = []
