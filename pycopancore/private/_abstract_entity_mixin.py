"""_abstract_entity_mixin class.

It sets the basic structure of entity mixins (individuals, cells , societies).
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
# Definition of class _AbstractEntityMixin
#

NEXTUID = 0


def get_next_uid():
    """Generate UIDs (Unique identifier).

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
    """Define AbstractEntityMixin.

    Entity-unspecific abstract class from which all entity-specific abstract
    mixin classes are derived.
    """

    processes = None
    model = None
    entities = None
    idle_entities = None

    def __init__(self,
                 **kwargs):
        """Initialize an _AbstractEntityMixin instance."""
        self._uid = get_next_uid()
        try:
            self.__class__.entities.append(self)
        except AttributeError:
            self.__class__.entities = [self]

    def deactivate(self):
        """Deactivate entity.

        Remove Entity from its classes entities list and add it to its classes
        idle_entities list.
        """
        self.__class__.entities.remove(self)
        try:
            self.__class__.idle_entities.append(self)
        except AttributeError:
            self.__class__.idle_entities = [self]

    def reactivate(self):
        """Reactivate entity.

        Remove Entity from its classes idle_entities list and add it to its
        classes entities list.
        """
        assert self in self.__class__.idle_entities, 'Not deactivated'
        self.__class__.idle_entities.remove(self)
        self.__class__.entities.append(self)

    def __repr__(self):
        return "{}[UID={}]".format(self.__class__.__name__, self._uid)

    def __str__(self):
        return repr(self)
