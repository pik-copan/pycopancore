"""_abstract_entity_mixin class.

It sets the basic structure of entity mixins (individuals, cells , social_systems).
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# TODO:
# - since this is beginning to contain logics, the name "Abstract..." is
#   no longer suitable. Rename to "_EntityMixin". Similar for _ProcessTaxon
# - in __init__, add logics that sets all variables to either their specified
#   values or their default values as given in Variable.

from . import _Mixin


class _AbstractEntityMixin(_Mixin):
    """Define _AbstractEntityMixin.

    Entity-unspecific abstract class from which all entity-specific abstract
    mixin classes are derived.
    """

    # NEXTUID is variable to address identifiers.

    # class (!) attributes:
    NEXTUID = 0
    idle_entities = None  # TODO: rename to inactive_entities
    """Inactive entities of this type"""

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

    def __init__(self, *args, **kwargs):
        """Initialize an _AbstractEntityMixin instance."""
        super().__init__(*args, **kwargs)
        self._uid = _AbstractEntityMixin.get_next_uid()
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

    def delete(self):
        """Delete entity from all lists."""
        # check if idle_entities list exists and if self in that list:
        if (self.__class__.idle_entities
                and self in self.__class__.idle_entities):
            self.__class__.idle_entities.remove(self)
        # check if instances list exists and if self in that list:
        if (self.__class__.instances
                and self in self.__class__.instances):
            self.__class__.instances.remove(self)
        # Now delete for good:
        del(self)

    @property
    def is_active(self):
        """Check if entity is active.
        
        In other words, check if entity is in self.__class__.instances"""
        if self in self.__class__.instances:
            return True
        if self in self.__class__.idle_entities:
            return False
        else:
            raise StatusError("Entity not active nor idle.")

    def __repr__(self):
        return "{}[UID={}]".format(self.__class__.__name__, self._uid)

    def __str__(self):
        return repr(self)


class StatusError(Exception):
    """Define Error.
    
    This Error is states, that an entity is neither active nor deactivated"""

    pass
