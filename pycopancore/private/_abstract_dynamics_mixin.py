"""_abstract_dynamics_mixin class.

It sets the basic structure of dynamic mixins (culture, metabolism, nature).
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
# Definition of class _AbstractDynamicsMixin
#


class _AbstractDynamicsMixin(object):
    """Define Entity-unspecific abstract class.

    From this class all entity-specific abstract mixin classes are derived.
    """

    processes = None
    model = None
    entities = None

    def __init__(self):
        """Initialize an _AbstractDynamicsMixin instance."""
        if self.__class__.entities:
            self.__class__.entities.append(self)
            print('This Process Taxon is already initialized!')
        else:
            self.__class__.entities = [self]

    def __repr__(self):
        pass

    def __str__(self):
        pass
