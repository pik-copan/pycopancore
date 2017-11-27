"""Cell entity type mixing class template.

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


class Cell (I.Cell):
    """Cell entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 characteristic=None,
                 average_precipitation=None,
                 **kwargs):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)  # must be the first line
        self.characteristic = characteristic
        self.average_precipitation = average_precipitation

        self.assert_valid()

        # assert that farmland is owned by county and city by municipality:
        if self.characteristic == 'farmland':
            assert self.social_system.municipality_like is False
        if self.characteristic == 'city':
            assert self.social_system.municipality_like is True

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
