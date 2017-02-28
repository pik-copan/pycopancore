"""base component's World entity type mixin implementation class"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others:
from pycopancore.model_components import abstract

from .. import interface as I


class World (I.World, abstract.World):
    """World entity type mixin implementation class.

    Base component's World mixin that every model must use in composing their
    World class. Inherits from I.World as the interface with all necessary
    variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 nature=None,
                 metabolism=None,
                 culture=None,
                 human_population=0,
                 **kwargs
                 ):
        """Initialize an (typically the only) instance of World"""
        super().__init__(**kwargs)  # must be the first line

        self.nature = nature
        self.metabolism = metabolism
        self.culture = culture
        self.human_population = human_population

        self._societies = set()
        self._cells = set()

    # getters and setters:

    @property  # read-only
    def societies(self):
        return self._societies

    @property  # read-only
    def top_level_societies(self):
        # find by filtering:
        return set([s for s in self._societies
                    if s.next_higher_society is None])

    @property  # read-only
    def cells(self):
        return self._cells

    @property  # read-only
    def individuals(self):
        # find indirectly via cells:
        r = set()
        for c in self._cells:
            r.update(c.individuals)
        return r

    # no process-related methods

    processes = []
