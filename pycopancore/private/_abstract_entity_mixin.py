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

# TODO:
# - since this is beginning to contain logics, the name "Abstract..." is
#   no longer suitable. Rename to "_EntityMixin". Similar for _ProcessTaxon
# - in __init__, add logics that sets all variables to either their specified
#   values or their default values as given in Variable.

from ..data_model import variable
from ..private._expressions import _DotConstruct, aggregation_names
from ..data_model import OrderedSet

import inspect


class _AbstractEntityMixinType(type):
    """metaclass for _AbstractEntityMixin.

    Needed for intercepting
    class attribute calls and having nice reprs.
    """

#     def __getattr__(cls, name):
#         """return an object representing an aggregation"""
#         print("seeking",cls,name,cls.__base__)
#         try:
#             return object.__getattribute__(name)
#         if name in aggregation_names:
#             return _DotConstruct(cls, [name])
#         res = getattr(cls.__base__, name)
#         return res

    def __getattribute__(cls, name):
        """Dummy docstring"""
        # TODO: add docstring to function
        if name in aggregation_names:
            return _DotConstruct(cls, [name])
        res = type.__getattribute__(cls, name)
        if isinstance(res, property):
            # find first overridden attribute in method resolution
            # order that is not a property (but a Variable object):
            for c in inspect.getmro(cls)[1:]:
                try:
                    res = c.__getattribute__(c, name)
                    if isinstance(res, variable.Variable):
                        return res
                except BaseException:
                    pass
            raise AttributeError("property " + name
                                 + " does not correspond to any Variable!")
        return res

#    def __str__(cls):
#        return cls.__name__


class _AbstractEntityMixin(object, metaclass=_AbstractEntityMixinType):
    """Define AbstractEntityMixin.

    Entity-unspecific abstract class from which all entity-specific abstract
    mixin classes are derived.
    """

    # NEXTUID is variable to adress identifiers.

    # class (!) attributes:
    NEXTUID = 0
    processes = []
    """All processes of this entity type"""
    model = None
    """Model containing this entity type"""
    instances = None
    """Entities of this type"""
    idle_entities = None

    def __new__(cls, *args, **kwargs):
        """Internal method called when instantiating a new entity.

        Don't call this directly, always generate entities by instantiating
        the a composite or mixin entity type class. This implementation makes
        sure that a composite entity is generated even when only a mixin is
        instantiated.
        """
        try:
            # if a composite class been registered with the invoking mixin
            # class, we generate an instance of that:
            print("instantiating a", cls._composed_class, args, kwargs)
            obj = super().__new__(cls._composed_class, *args, **kwargs)
        except:
            # otherwise, we do what __new__ normally does, namely generate an
            # instance of the class invoking it, i.e., of cls:
            print("instantiating a", cls, args, kwargs)
            obj = super().__new__(cls)
        return obj

    def __init__(self,
                 **kwargs):
        """Initialize an _AbstractEntityMixin instance."""
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

    def __repr__(self):
        return "{}[UID={}]".format(self.__class__.__name__, self._uid)

    def __str__(self):
        return repr(self)

    def set_value(self, var, value):
        """Dummy docstring"""
        # TODO: add docstring to method
        assert isinstance(var, variable.Variable), \
            "variable must be a Variable object"
        var.set_value(self, value)

    def assert_valid(self):
        """Make sure all variable values are valid.

        By calling assert_valid for all Variables

        """
        for v in self.variables:
            try:
                val = v.get_value(self)
            except:
                return
            v.assert_valid(val)

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


class StatusError(Exception):
    """Define Error.
    
    This Error is states, that an entity is neither active nor deactivated"""

    pass
