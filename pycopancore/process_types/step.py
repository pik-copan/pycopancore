"""Step process class.

A step process may be used for things that reoccur regularly.
It might also be used for things that are continuos but are approximated by
steps.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

#
# Imports
#


#
# Definition of class Event
#

from ..private import _AbstractProcess


class Step(_AbstractProcess):
    """Define the step-process-type."""

    type = "Step"
    timetype = "discrete"

    def __init__(self,
                 name,
                 variables,
                 specification
                 ):
        """Instantiate a process of type step.

        Parameters
        ----------
        name : string
        variables
        specification : list
            Structured as followed: [function to
             return next_time (function(self, t)), function to calculate
             variables of each entity (function(self, t)]
        """
        super().__init__(name)

        self.variables = variables
        self.specification = specification
