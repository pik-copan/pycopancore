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
from ... import abstract
from .... import master_data_model as D
from ....private import unknown

from .. import interface as I


class Group (I.Group, abstract.Group):
    """Gropp entity type mixin implementation class.

    Base component's Group mixin that every model must use in composing
    their Group class. Inherits from I.Group as the interface with all
    necessary variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 culture,
                 world,
                 **kwargs
                 ):
        """Initialize an instance of Group.

        Parameters
        ----------
        culture: obj
            Culture the Group belongs to
        world: obj
            World the Group belongs to (to bypass AttributeErrors for now)
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        # init and set variables implemented via properties:
        self._culture = None
        self.culture = culture
        self._world = None
        self.world = world

        if self.culture:
            self.culture.group_membership_network.add_node(self, type="Group", color="green")

    def deactivate(self):
        """Deactivate a group.

        In particular, deregister from all networks.

        """
        # deregister from all networks:
        if self.culture:
            self.culture.group_membership_network.remove_node(self)
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate a group.

        In particular, deregister with all mandatory networks.

        """
        super().reactivate()  # must be the first line
        # reregister with all mandatory networks:
        if self.culture:
            self.culture.group_membership_network.add_node(self, type="Group", color="green")


    # getters and setters for references:

    #culture needs to be before world, as group gets its world etc. over its culture
    @property
    def culture(self):
        """Get culture group is part of."""
        return self._culture

    @culture.setter
    def culture(self, c):
        """Set culture group is part of."""
        if self._culture is not None:
            # first deregister from previous culture's list of worlds:
            self._culture.groups.remove(self)
        if c is not None:
            assert isinstance(c, I.Culture), \
                "Culture must be taxon type Culture"
            c._groups.add(self)
        self._culture = c

    @property
    def world(self):
        """Get the World the Group is part of."""
        return self._world

    @world.setter
    def world(self, w):
        """Set the World the Group is part of."""
        if self._world is not None:
            # first deregister from previous world's list of cells:
            self._world.groups.remove(self)
        assert isinstance(w, I.World), "world must be of entity type World"
        w._groups.add(self)
        self._world = w

    # getters for backwards references and convenience variables:

    @property  # read-only
    def environment(self):
        """Get the Environment of which the Group is a part."""
        return self._world.environment

    @property  # read-only
    def metabolism(self):
        """Get the Metabolism of which the Group is a part."""
        return self._world.metabolism

    @property
    def group_members(self):
        """Get the set of Individuals associated with this Group."""
        # return self.culture.group_membership_network.neighbors(self)
        return self.culture.group_membership_network.predecessors(self) # .predecessors as network is directed from inds to groups


    # no process-related methods

    processes = []  # no processes in base


