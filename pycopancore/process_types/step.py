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
    """
    Discrete process
    """

    type = "Step"
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
        name : string
        variables
        specification : list
            Structured as followed: [first execution (float),function to
             estimate next_time (function(t)), function to calculate variables
             of each entity (function(self)]
             # Do we really want a function to give back next t? Or is a simple
             # value enogh? then the value would specifiy how big a step is
        smoothness
        """

        super(Step, self).__init__()

        self.name = name
        self.variables = variables
        self.specification = specification
        self.smoothness = smoothness

# TODO: add metadata like immediate, later... for step, since the dynamic may
# happen with different dealys
