"""Culture process taxon mixing class template.

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


class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 # *,  # TODO: uncomment when adding named args behind here
                 **kwargs):
        """Initialize the unique instance of Culture."""
        super().__init__(**kwargs)  # must be the first line
        # TODO: add custom code here:
        pass

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
