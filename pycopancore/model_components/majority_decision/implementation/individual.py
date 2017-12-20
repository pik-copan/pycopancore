"""Individual entity type class template.

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


class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 # *,  # TODO: uncomment when adding named args behind here
                 **kwargs):
        """Initialize an instance of Individual."""
        super().__init__(**kwargs)  # must be the first line
        # TODO: add custom code here:
        pass

    def deactivate(self):
        """Deactivate an individual."""
        # TODO: add custom code here:
        pass
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate an individual."""
        super().reactivate()  # must be the first line
        # TODO: add custom code here:
        pass

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
