""" """

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# only used in this component, not in others:
from pycopancore.private._abstract_process_taxon_mixin import \
    _AbstractProcessTaxonMixin
from pycopancore.data_model.ordered_set import OrderedSet

from pycopancore.model_components import abstract
from pycopancore.private._simple_expressions import unknown

from .. import interface as I


class Region(I.Region, abstract.Region):
    """Region entity type mixin implementation class.

    Base component's Region mixin that every model must use in composing their
    Region class. Inherits from I.Region as the interface with all necessary
    variables and parameters.

    """

    def __init__(self,
                 *,
                 environment=None,
                 metabolism=None,
                 **kwargs
                 ):
        """Instantiate (typically the only) instance of World.

        Parameters
        ----------
        environment : obj
            Environment acting on this World.
        metabolism : obj
            Metabolism acting on this World.
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        self._world = None
        self._metabolism = metabolism
        self._social_systems = set()
        self._cells = set()
        self._groups = set()

        # make sure all variable values are valid:
        self.assert_valid()

    # getters and setters for references:

    @property
    def world(self):
        """Get the World the Region is part of."""
        return self._world

    @world.setter
    def world(self, w):
        """Set the World the Region is part of."""
        if self._world is not None:
            # first deregister from previous world's list of cells:
            self._world.regions.remove(self)
        assert isinstance(w, I.World), "world must be of entity type World"
        w._regions.add(self)
        self._world = w

    @property
    def metabolism(self):
        """Get the World the Cell is part of."""
        return self._metabolism

    @metabolism.setter
    def metabolism(self, m):
        """Set the Metabolism the World is part of."""
        if self._metabolism is not None:
            # first deregister from previous metabolism's list of regions:
            self._metabolism.regions.remove(self)
        if m is not None:
            assert isinstance(m, I.Metabolism), \
                "Metabolism must be of process taxon type Metabolism"
            m._regions.add(self)
        self._metabolism = m

    @property  # read-only
    def social_systems(self):
        """Get the set of all SocialSystems on this World."""
        return self._social_systems

    @property  # read-only
    def cells(self):
        """Get the set of Cells on this World."""
        return self._cells

    @property  # read-only
    def groups(self):
        """Get the set of Groups on this World."""
        return self._groups

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


    processes = []
