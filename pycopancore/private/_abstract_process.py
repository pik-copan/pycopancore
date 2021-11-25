"""_AbstractProcess class.

It sets the basic structure of processes (ODE,explicit, step, event).
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
# Definition of class _AbstractProcess
#

class _AbstractProcess(object):
    """Define Abstract class for representing types of model processes.

    These are ODEs, steps, explicit/implicit equations, events.
    """

    name = None
    """short human-readable name"""
    desc = None
    """a longer description"""    
    ref = None
    """some URL, e.g. a wikipedia page or doi, and/or a page/line/equation number"""
  
    type = None
    """mathematical type (ODE, Explicit, ...)"""
    timetype = None
    """time type"""
    smoothness = None
    """degree of smoothness"""

    owning_class = None
    """the class (entity-type or process taxon) owning the process"""

    def __init__(self, name="", desc="", ref=""):
        """Initialize an _AbstractProcess instance."""
        self.name = name
        self.desc = desc
        self.ref = ref
        self.owning_class = None

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name + " (" + self.type + ")"
