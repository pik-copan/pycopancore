""" """

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others
from ... import abstract
# from .... import master_data_model as D
from ....private import unknown

from .. import interface as I


class Individual (I.Individual, abstract.Individual):
    """Individual entity type mixin implementation class.

    Base component's Individual mixin that every model must use in composing
    their Individual class. Inherits from I.Individual as the interface with all
    necessary variables and parameters.

    """

    def __init__(self,
                 *,
                 cell,  # this is a mandatory keyword-only argument!
                 relative_weight=1,
                 **kwargs
                 ):
        """Instantiate an instance of Individual.

        Parameters
        ----------
        cell: obj
            Cell the Individual belongs to.
        relative_weight: float
            relative representation weight
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        # init and set variables implemented via properties:
        self._cell = None
        self.cell = cell

        # set other variables:
        self.relative_weight = relative_weight

        # make sure all variable values are valid:
        self.assert_valid()

        # register with all mandatory networks:
        if self.culture:
            self.culture.acquaintance_network.add_node(self)

    def deactivate(self):
        """Deactivate an individual.

        In particular, deregister from all networks.

        """
        # deregister from all networks:
        if self.culture:
            self.culture.acquaintance_network.remove_node(self)
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate an individual.

        In particular, deregister with all mandatory networks.

        """
        super().reactivate()  # must be the first line
        # reregister with all mandatory networks:
        if self.culture:
            self.culture.acquaintance_network.add_node(self)

    # getters and setters for references:

    @property
    def cell(self):
        """Get and set the Cell of residence the Individual belongs to."""
        return self._cell

    @cell.setter
    def cell(self, c):
        if self._cell:
            # first deregister from previous cell's list of individuals:
            self._cell._individuals.remove(self)
            # reset dependent caches:
            if self._cell.society is not None:
                self._cell.society.direct_individuals = unknown
                self._cell.society.individuals = unknown
            self.world.individuals = unknown
        assert isinstance(c, I.Cell), "cell must be of entity type Cell"
        c._individuals.add(self)
        self._cell = c
        # reset dependent caches:
        if c.society is not None:
            c.society.direct_individuals = unknown
            c.society.individuals = unknown
        self.world.individuals = unknown

    # getters for backwards references and convenience variables:

    @property  # read-only
    def world(self):
        """Get the World the Individual belongs to."""
        return self._cell.world

    @property  # read-only
    def nature(self):
        """Get the Nature the Individual is part of."""
        return self._cell.nature

    @property  # read-only
    def metabolism(self):
        """Get the Metabolism the Individual is part of."""
        return self._cell.metabolism

    @property  # read-only
    def culture(self):
        """Get the Culture the Individual is part of."""
        return self._cell.culture

    @property  # read-only
    def society(self):
        """Get the lowest level Society the Individual is resident of."""
        return self._cell.society

    @property  # read-only
    def societies(self):
        """Get the upward list of all Societies the Individual is resident
        of."""
        return self._cell.societies

    @property
    def population_share(self):
        """Get the share of Society's direct population represented by this
        individual."""
        total_relative_weight = sum([i.relative_weight
                                     for i in self.society.individuals])
        return self.relative_weight / total_relative_weight

    @property
    def represented_population(self):
        """Get the absolute population this Individual represents due to
        sampling."""
        return self.population_share * self.society.human_population

    @property
    def acquaintances(self):
        """Get the set of Individuals the Individual is acquainted with."""
        return self.culture.acquaintance_network.neighbors(self)

    # no process-related methods

    processes = []  # no processes in base
