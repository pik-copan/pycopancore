"""_AbstractProcess class.

It sets the basic structure of processes (ODE,explicit, step, event).
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
# Definition of class _AbstractProcess
#

class _AbstractProcess(object):
    """Define Abstract class for representing types of model processes.

    These are ODEs, steps, explicit/implicit equations, events.
    """

    name = None
    type = None
    timetype = None
    smoothness = None
    
    owning_classes = None

    def __init__(self, name=""):
        """Initialize an _AbstractProcess instance."""
        self.name = name
        self.owning_classes = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name + " (" + self.type + ")"
