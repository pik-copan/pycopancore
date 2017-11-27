"""SocialSystem entity type mixing class template.

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
#from .... import master_data_model as D


class SocialSystem (I.SocialSystem):
    """SocialSystem entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 harvest_rate=0.5,
                 **kwargs):
        """Initialize an instance of SocialSystem."""
        super().__init__(**kwargs)  # must be the first line

        self.harvest_rate = harvest_rate

    def deactivate(self):
        """Deactivate a social_system."""
        # TODO: add custom code here:
        pass
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate a social_system."""
        super().reactivate()  # must be the first line
        # TODO: add custom code here:
        pass

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
