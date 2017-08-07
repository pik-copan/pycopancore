"""Cell entity type mixing class template.

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


class Cell (I.Cell):
    """Cell entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 # *,  # TODO: uncomment when adding named args behind here
                 **kwargs):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)  # must be the first line
        # TODO: add custom code here:

        # At last, check for validity of all variables that have been
        # initialized and given a value:

        # Following method is defined in abstract_entity_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()
        pass

    def deactivate(self):
        """Deactivate a cell."""
        # TODO: add custom code here:
        pass
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate a cell."""
        super().reactivate()  # must be the first line
        # TODO: add custom code here:
        pass

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
