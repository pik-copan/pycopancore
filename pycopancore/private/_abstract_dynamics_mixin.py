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
    """
    Entity-unspecific abstract class from which all entity-specific abstract mixin classes are derived.
    """

    processes = None
    model = None

    def __init__(self):
        """
        Initializes an _AbstractDynamicsMixin instance.
        """
        # Is "super..." necessary here?
        # super(AbstractDynamicsMixin, self).__init__()
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass