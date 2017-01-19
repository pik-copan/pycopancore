# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is the process type step class. A step process may be used for things that
reoccur regularly. It might also be used for things that are contiuos but
are approximated by steps.
"""

#
# Imports
#


#
# Definition of class Event
#

from pycopancore.private import _AbstractProcess


class Step(_AbstractProcess):
    """
    Discrete process
    """

    type = "Step"
    timetype = "discrete"

    def __init__(self,
                 name,
                 variables,
                 specification
                 ):
        """

        Parameters
        ----------
        name : string
        variables
        specification : list
            Structured as followed: [function to
             return next_time (function(self, t)), function to calculate
             variables of each entity (function(self, t)]
        """

        super().__init__()

        self.name = name
        self.variables = variables
        self.specification = specification
