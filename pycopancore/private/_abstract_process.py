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
# Definition of class _AbstractProcess
#

class _AbstractProcess(object):
    """
    Abstract class for representing types of model processes (ODEs, steps,
    explicit/implicit equations, events).
    """

    name = None
    type = None
    timetype = None
    smoothness = None

    def __init__(self):
        """
        Initializes an _AbstractProcess instance.
        """
        # Is "super..." necessary here?
        # super(_AbstractProcess, self).__init__()
        pass

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name + " (" + self.type + ")"
