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

from .. import interface as I


class Metabolism (I.Metabolism, abstract.Metabolism):
    """Metabolism process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 # *,
                 **kwargs):
        """
        Initialize the unique instance of Metabolism.

        Parameters
        ----------
        **kwargs
            keyword arguments passed to super()

        """
        super().__init__(**kwargs)  # must be the first line

        self._worlds = set()

    @property  # read-only
    def worlds(self):
        """Get the set of Worlds on this Metabolism."""
        return self._worlds

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # no processes in base
