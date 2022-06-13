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
                 world,
                 # culture=None,
                 next_higher_group=None,
                 **kwargs
                 ):
        """Initialize an instance of Group.

        Parameters
        ----------
        world: obj
            World the Group belongs to
        next_higher_group: obj
            Optional Group the Group belongs to (default is None)
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        # init and set variables implemented via properties:
        # self._culture = None
        # self.culture = culture
        self._world = None
        self.world = world

        # self._social_system = None
        # self.social_system = social_system
        self._next_higher_group = None
        self.next_higher_group = next_higher_group

        # init caches:
        self._next_lower_group = set()
        self._direct_cells = set()

        if self.culture:
            self.culture.group_membership_network.add_node(self)

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
            self.culture.group_membership_network.add_node(self)

    def member_mean(self, state):
        """
        Calculate the arithmetic mean of a state of all members of a groups.
        """



    # getters and setters for references:

    @property
    def world(self):
        """Get the World the Group is part of."""
        return self._world

    @world.setter
    def world(self, w):
        """Set the World the Group is part of."""
        if self._world is not None:
            self._world._groups.remove(self)
        assert isinstance(w, I.World), "world must be of entity type World"
        w._groups.add(self)
        self._world = w

    # @property
    # def social_system(self):
    #     """Get the SocialSystem the Group is part of."""
    #     return self._social_system

    # @social_system.setter
    # def social_system(self, s):
    #     """Set the SocialSystem the Group is part of."""
    #     if self._social_system is not None:
    #         self._social_system._groups.remove(self)
    #     assert isinstance(s, I.SocialSystem), "socialsystem must be of entity type SocialSystem"
    #     s._groups.add(self)
    #     self._social_system = s

    # @property
    # def next_higher_group(self):
    #     """Get next higher group."""
    #     return self._next_higher_group

    # @next_higher_group.setter
    # def next_higher_group(self, s):
    #     """Set next higher group."""
    #     if self._next_higher_group is not None:
    #         self._next_higher_group._next_lower_groups.remove(self)
    #         reset dependent cache:
            # self._next_higher_group.cells = unknown
        # if s is not None:
        #     assert isinstance(s, I.Group), \
        #         "next_higher_group must be of entity type group"
        #     s._next_lower_groups.add(self)
        #     reset dependent cache:
        #     s.cells = unknown
        # self._next_higher_group = s
        # reset dependent caches:
        # self.higher_groups = unknown

    # getters for backwards references and convenience variables:

    @property  # read-only
    def environment(self):
        """Get the Environment of which the Group is a part."""
        return self._world.environment

    @property  # read-only
    def metabolism(self):
        """Get the Metabolism of which the Group is a part."""
        return self._world.metabolism

    # @property
    # def culture(self):
    #     """Get groups's culture."""
    #     return self._culture

    # @culture.setter
    # def culture(self, c):
    #     """Set groups's culture."""
    #     if self._culture is not None:
    #         first deregister from previous culture's list of worlds:
            # self._culture.groups.remove(self)
        # if c is not None:
        #     assert isinstance(c, I.Culture), \
        #         "Culture must be taxon type Culture"
        #     c._groups.add(self)
        # self._culture = c

    # _higher_groups = unknown
    """cache, depends on self.next_higher_group
    and self.next_higher_group.higher_groups"""
    # @property  # read-only
    # def higher_groups(self):
    #     """Get higher groups."""
    #     if self._higher_groups is unknown:
            # find recursively:
            # self._higher_groups = [] if self.next_higher_group is None \
            #     else ([self.next_higher_group]
            #           + self.next_higher_group.groups)
        # return self._higher_groups

    # @higher_groups.setter
    # def higher_groups(self, u):
    #     """Set higher groups."""
    #     assert u == unknown, "setter can only be used to reset cache"
    #     self._higher_groups = unknown
        # reset dependent caches:
        # for s in self._next_lower_groups:
        #     s.higher_groups = unknown
        # for c in self._direct_cells:
        #     c.groups = unknown

    # @property  # read-only
    # def next_lower_groups(self):
    #     """Get next lower groups."""
    #     return self._next_lower_groups

    # @property  # read-only
    # def lower_groups(self):
    #     """Get lower groups."""
        # aggregate recursively:
        # l = self._next_lower_groups
        # for s in self._next_lower_groups:
        #     l.update(s.lower_groups)
        # return l

    @property
    def group_members(self):
        """Get the set of Individuals associated with this Group."""
        return self.culture.group_membership_network.neighbors(self) # .predeccessors as network is directed from inds to groups





    # no process-related methods

    processes = []  # no processes in base


