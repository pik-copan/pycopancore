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
# Definition of class _AbstractEntityMixin
#

NEXTUID = 0


def get_next_uid():
    """
    Function to generate UIDs (Unique identifier)
    Returns
    -------
    current_uid: int
        the current uid
    """
    global NEXTUID
    current_uid = NEXTUID
    NEXTUID += 1
    return current_uid


class _AbstractEntityMixin(object):
    """
    Entity-unspecific abstract class from which all entity-specific abstract
    mixin classes are derived.
    """

    processes = None
    model = None

    def __init__(self):
        """
        Initializes an _AbstractEntityMixin instance.
        """
        self._uid = get_next_uid()
        # pass

    def __repr__(self):
        return "{}[UID={}]".format(self.__class__.__name__, self._uid)

    def __str__(self):
        return repr(self)
