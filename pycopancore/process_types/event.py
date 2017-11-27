"""Event-type process class.

It is used for processes that do not occur in regular timesteps.
An event might be something like a birth or death, catastrophes of all sorts.
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


class Event(_AbstractProcess):
    """Define Event process class."""

    type = "Event"
    timetype = "discrete"

    def __init__(self,
                 name,
                 variables,
                 specification,
                 smoothness=0
                 ):
        """Instantiate an instance of an Event process.

        Parameters
        ----------
        name
        variables
        specification : list
            Structured as followed: [eventtype ("rate" or "time"), rate
            or time-function, method/function of variable(s)]
        smoothness
        """
        super().__init__(name)

        self.variables = variables
        self.specification = specification
        self.smoothness = smoothness
