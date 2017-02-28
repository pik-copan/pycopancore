"""base component's World entity type mixin implementation class"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others:
from pycopancore.model_components import abstract

from . import interface as I


class World (I.World, abstract.World):
    """World entity type mixin implementation class.

    Base component's World mixin that every model must use in composing their
    World class. Inherits from I.World as the interface with all necessary
    variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 *,
                 **kwargs
                 ):
        """Initialize an (typically the only) instance of World"""
        super().__init__(**kwargs)  # must be the first line
        pass

    # getters and setters:

    @property  # read-only
    def societies(self):
        return self._societies

    @property  # read-only
    def cells(self):
        return self._cells

    # no process-related methods

    processes = []
