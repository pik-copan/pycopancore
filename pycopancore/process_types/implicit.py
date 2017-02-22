"""Implicit proccess class.

Implicit functions are not yet implemented.
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


class Implicit(_AbstractProcess):
    """Define the class Implicit."""

    type = "Implicit"
    timetype = "discrete"

    def __init__(self,
                 name,
                 variables,
                 specification
                 ):
        """Initiate an instance of an implicit process.

        Parameters
        ----------
        name
        variables
        specification
        """
        super().__init__(name)

        self.variables = variables
        self.specification = specification
