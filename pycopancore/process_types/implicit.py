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
    """
    Implicit process
    """

    type = "Implicit"
    timetype = "discrete"

    def __init__(self,
                 name,
                 variables,
                 specification,
                 smoothness=0,
                 ):
        """

        :param name: string
        :param variables:
        :param specification:
        :param smoothness:
        """
        super(Implicit, self).__init__()

        self.name = name
        self.variables = variables
        self.specification = specification
        self.smoothness = smoothness
