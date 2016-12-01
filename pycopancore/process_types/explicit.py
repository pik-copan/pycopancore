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
    """
    Implicit process
    """

    type = "Explicit"
    timetype = "continious"

    def __init__(self,
                 name,
                 variables,
                 specification,
                 smoothness=0,
                 ):
        """

        Parameters
        ----------
        name :
        variables :
        specification : func
            function(self,t)
        smoothness :
        """
        super(Explicit, self).__init__()

        self.name = name
        self.variables = variables
        self.specification = specification
        self.smoothness = smoothness
