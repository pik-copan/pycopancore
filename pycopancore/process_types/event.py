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


class Event(_AbstractProcess):
    """
    Discrete process
    """

    type = "Event"
    timetype = "discrete"

    def __init__(self,
                 name,
                 variables,
                 specification,
                 smoothness=0,
                 ):
        """

        Parameters
        ----------
        name
        variables
        specification : list
            Structured as followed: [eventtype ("rate" or "time"), rate
            or time-function, method/function of variable(s)]
        smoothness
        """

        super(Event, self).__init__()

        self.name = name
        self.variables = variables
        self.specification = specification
        self.smoothness = smoothness
