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
from ....private import unknown

# typical imports for implementation classes:
from .. import interface as I
from .... import master_data_model as D


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
                 land_area = 1 * D.square_kilometers,
                 geometry=None,
                 **kwargs
                 ):
        """Initialize an instance of Cell.

        Parameters
        ----------
        world : obj
            World the Cell belongs to (the default is None)
        society : obj
            Society the Cell belongs to (the default is None)
        location : obj
            Location of Cell (the default is None)
        land_area : quantity
            Area of Cell, (the default is 1 * km^2)
        geometry : obj
            Geometry of Cell (the default is None)
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        # init and set variables implemented via properties
        self._world = None
        self._society = None
        if world:
            self.world = world
        self.society = society  # this line must occur after setting world!

        # set other variables:
        self.location = location
        self.land_area = land_area
        self.geometry = geometry

        # make sure all variable values are valid:
        self.assert_valid()

        # init other caches:
        self._individuals = set()

        # register with all mandatory networks:
        if self.nature:
            self.nature.geographic_network.add_node(self)


    # getters and setters for references:

    @property
    def world(self):
        """Get the World the Cell is part of."""
        return self._world

    @world.setter
    def world(self, w):
        """Set the World the Cell is part of."""
        if self._world is not None:
            # first deregister from previous world's list of cells:
            self._world.cells.remove(self)
        assert isinstance(w, I.World), "world must be of entity type World"
        w._cells.add(self)
        self._world = w

    @property
    def society(self):
        """Get the lowest-level Society whose territory the Cell is part of."""
        return self._society

    @society.setter
    def society(self, s):
        """Set the lowest-level Society whose territory the Cell is part of."""
        if self._society is not None:
            # first deregister from previous society's list of cells:
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
        """Get the Nature of which the Cell is a part."""
        return self._world.nature

    @property  # read-only
    def metabolism(self):
        """Get the Metabolism of which the Cell is a part."""
        return self._world.metabolism

    @property  # read-only
    def culture(self):
        """Get the Culture of which the Cell is a part."""
        return self._world.culture

    _societies = unknown
    """cache, depends on self.society, self.society.higher_societies"""
    @property  # read-only
    def societies(self):
        """Get upward list of Societies the Cell belongs to (in)directly."""
        if self._societies is unknown:
            self._societies = [] if self.society is None \
                else [self.society] + self.society.higher_societies
        return self._societies

    @societies.setter
    def societies(self, u):
        """Set upward list of Societies the Cell belongs to (in)directly."""
        assert u == unknown, "setter can only be used to reset cache"
        self._societies = unknown
        # reset dependent caches:
        pass

    @property  # read-only
    def individuals(self):
        """Get the Individuals which reside in the Cell."""
        return self._individuals

    # no process-related methods

    processes = []  # no processes in base
