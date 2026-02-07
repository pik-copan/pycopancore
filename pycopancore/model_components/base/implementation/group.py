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
from pycopancore.model_components import abstract

from .. import interface as Interface


class Group(Interface.Group, abstract.Group):
    """Gropp entity type mixin implementation class.

    Base component's Group mixin that every model must use in composing
    their Group class. Inherits from Interface.Group as the interface with all
    necessary variables and parameters.
    """

    # standard methods:

    def __init__(self, *, world, culture=None, **kwargs):
        """Initialize an instance of Group.

        Parameters
        ----------
        world: obj
            World the Group belongs to
        culture: obj, optional
            Culture the Group belongs to (optional)
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        # init and set variables implemented via properties:
        self._culture = None
        self._world = None
        self.world = world
        if culture is not None:
            self.culture = culture

        # Register with appropriate network
        if self.culture:
            self.culture.group_membership_network.add_node(
                self, type="Group", color="green"
            )
        elif self.world:
            # Use world's group membership network if no culture
            if hasattr(self.world, "group_membership_network"):
                self.world.group_membership_network.add_node(
                    self, type="Group", color="green"
                )

    def deactivate(self):
        """Deactivate a group.

        In particular, deregister from all networks.

        """
        # deregister from all networks:
        if self.culture:
            self.culture.group_membership_network.remove_node(self)
        elif self.world:
            if hasattr(self.world, "group_membership_network"):
                self.world.group_membership_network.remove_node(self)
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate a group.

        In particular, deregister with all mandatory networks.

        """
        super().reactivate()  # must be the first line
        # reregister with all mandatory networks:
        if self.culture:
            self.culture.group_membership_network.add_node(
                self, type="Group", color="green"
            )
        elif self.world:
            if hasattr(self.world, "group_membership_network"):
                self.world.group_membership_network.add_node(
                    self, type="Group", color="green"
                )

    # getters and setters for references:

    @property
    def culture(self):
        """Get culture group is part of."""
        return self._culture

    @culture.setter
    def culture(self, c):
        """Set culture group is part of."""
        if self._culture is not None:
            # first deregister from previous culture's list of groups:
            self._culture.groups.remove(self)
        if c is not None:
            assert isinstance(
                c, Interface.Culture
            ), "Culture must be taxon type Culture"
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
            # first deregister from previous world's list of groups:
            if hasattr(self._world, "groups"):
                self._world.groups.remove(self)
        # Accept any world object that has a groups attribute
        if hasattr(w, "groups"):
            # Try to add to _groups first (pycopancore style)
            if hasattr(w, "_groups"):
                w._groups.add(self)
            else:
                # For worlds with groups but no _groups, add to groups list
                w.groups.append(self)
            self._world = w
        else:
            # For worlds without groups attribute, just store the reference
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
        if self.culture:
            return self.culture.group_membership_network.predecessors(self)
        elif self.world and hasattr(self.world, "group_membership_network"):
            return self.world.group_membership_network.predecessors(self)
        else:
            # Return empty set if no network available
            return set()

    # no process-related methods

    processes = []  # no processes in base
