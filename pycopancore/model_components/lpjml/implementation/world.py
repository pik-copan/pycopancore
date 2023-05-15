"""World entity type mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I
# from .... import master_data_model as D


class World (I.World):
    """World entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 **kwargs):
        """Initialize an instance of World."""
        super().__init__(**kwargs)

    def deactivate(self):
        """Deactivate a world."""
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate a world."""
        super().reactivate()  # must be the first line

    # process-related methods:

    processes = []
