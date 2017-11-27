"""Explicit process class.

Explicit functions are used to calculate variables to help other functions,
for example calculate temperature from co2 level.
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


class Explicit(_AbstractProcess):
    """Define explicit process class."""

    type = "Explicit"
    timetype = "continuous"

    def __init__(self,
                 name,
                 targets,
                 specification,
                 smoothness=0
                 ):
        """Instantiate an instance of an explicit process.

        Parameters
        ----------
        name :
        targets :
        specification : func
            function(self,t)
        smoothness :
        """
        super().__init__(name)

        self.targets = targets
        self.specification = specification
        self.smoothness = smoothness
