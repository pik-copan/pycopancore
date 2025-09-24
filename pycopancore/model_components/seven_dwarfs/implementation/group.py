"""Group entity type class template.

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

# TODO: import those process types you need:
from pycopancore.process_types import Explicit

from .. import interface as Interface


class Group(Interface.Group):
    """Group entity type mixin implementation class."""

    # standard methods:
    # TODO: only uncomment when adding custom code!

    #     def __init__(self,
    #                  # TODO: uncomment when adding named args behind here
    #                  # *,
    #                  **kwargs):
    #         """Initialize an instance of Individual."""
    #         super().__init__(**kwargs)  # must be the first line
    #         # TODO: add custom code here:
    #         pass
    #
    #     def deactivate(self):
    #         """Deactivate a Group."""
    #         # TODO: add custom code here:
    #         pass
    #         super().deactivate()  # must be the last line
    #
    #     def reactivate(self):
    #         """Reactivate a Group."""
    #         super().reactivate()  # must be the first line
    #         # TODO: add custom code here:
    #         pass

    # process-related methods:

    def check_if_member(self, unused_t):
        """Check if dwarf 1 is member of any group."""
        group_members = list(self.group_members)
        i_0 = list(self.world.individuals)[0]
        if i_0 in group_members:
            self.having_members = True
        else:
            self.having_members = False

    # TODO: add some if needed...

    processes = [
        Explicit(
            "simple test",
            [Interface.Group.having_members],
            check_if_member,
        )
    ]  # TODO: instantiate and list process objects here
