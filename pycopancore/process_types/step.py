"""Step process class.

A step process may be used for things that reoccur regularly.
It might also be used for things that are continuos but are approximated by
steps.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
# Imports
#


#
# Definition of class Event
#

from pycopancore.private import _AbstractProcess


class Step(_AbstractProcess):
    """Define the step-process-type."""

    type = "Step"
    timetype = "discrete"

    def __init__(self,
                 name,
                 variables,
                 specification
                 ):
        """Initiate a process of type step.

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
