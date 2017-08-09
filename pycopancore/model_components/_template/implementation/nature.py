"""Nature process taxon mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
# from .... import master_data_model as D


class Nature (I.Nature):
    """Nature process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 # *,  # TODO: uncomment when adding named args behind here
                 **kwargs):
        """Initialize the unique instance of Nature."""
        super().__init__(**kwargs)  # must be the first line
        # TODO: add custom code here:
        pass

        # At last, check for validity of all variables that have been
        # initialized and given a value:
        self.assert_valid()

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
