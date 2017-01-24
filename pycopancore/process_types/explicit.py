"""Explicit process class.

Explicit functions are used to calculate variables to help other functions,
for example calculate temperature from co2 level.
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


class Explicit(_AbstractProcess):
    """Define explicit process class."""

    type = "Explicit"
    timetype = "continious"

    def __init__(self,
                 name,
                 variables,
                 specification,
                 smoothness=0,
                 ):
        """Initiate an instance of an explicit process.

        Parameters
        ----------
        name :
        variables :
        specification : func
            function(self,t)
        smoothness :
        """
        super().__init__()

        self.name = name
        self.variables = variables
        self.specification = specification
        self.smoothness = smoothness
