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

from pycopancore.data_model import Variable


class _AbstractEntityMixin (object):
    """Define AbstractEntityMixin.

    Entity-unspecific abstract class from which all entity-specific abstract
    mixin classes are derived.
    """

    # NEXTUID is variable to adress identifiers.
    NEXTUID = 0
    processes = []
    model = None
    instances = None
    idle_entities = None

    def __init__(self,
                 **kwargs):
        """Initialize an _AbstractEntityMixin instance."""
        self._uid = self.get_next_uid()  # Jobst: I don't see why we need this
        try:
            self.__class__.instances.append(self)
        except AttributeError:
            self.__class__.instances = [self]

    def deactivate(self):
        """Deactivate entity.

        Remove Entity from its classes entities list and add it to its classes
        idle_entities list.
        """
        self.__class__.instances.remove(self)
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
        self.__class__.instances.append(self)

# Jobst: I don't see why we need this:
    def __repr__(self):
        return "{}[UID={}]".format(self.__class__.__name__, self._uid)

    def __str__(self):
        return repr(self)

    def set_value(self, variable, value):
        assert isinstance(variable, Variable), \
            "variable must be a Variable object"
        variable.set_value(self, value)

    @classmethod
    def get_next_uid(cls):
        """Generate UIDs (Unique identifier).

        Returns
        -------
        current_uid: int
            the current uid
        """
        current_uid = cls.NEXTUID
        cls.NEXTUID += 1
        return current_uid
