"""_abstract_mixin class.

It sets the basic structure of mixins (entity types, process taxa).
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

from ..data_model import variable
from ..private._expressions import _DotConstruct, aggregation_names
from ..data_model import OrderedSet

import inspect


class _MixinType(type):
    """metaclass for _Mixin.

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
        if name == "__qualname__":  # needed to make sphinx happy
            return "DUMMY"  # FIXME!
        if name in aggregation_names:
            dc = _DotConstruct(cls, [], aggregation=name)
#            print("new aggregation dot construct",dc,"at",cls,"with aggregation",name)
            return dc
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


class _Mixin(object, metaclass=_MixinType):
    """Define AbstractEntityMixin.

    Entity- or taxon-unspecific class from which all mixin classes are derived
    via _EntityMixin or _ProcessTaxonMixin.
    """

    # NEXTUID is variable to address identifiers.

    # class (!) attributes:
    processes = []
    """All processes of this entity type"""
    model = None
    """Current model using this entity type"""
    instances = None
    """Active entities of this type"""
    _composite_class = None
    """Composite class this mixin contributes to in the current model"""

    # needed to make sphinx happy:
    __qualname__ = "pycopancore.private._mixin._Mixin"

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
#            print("instantiating a", cls._composed_class, args, kwargs)
            obj = super().__new__(cls._composed_class, *args, **kwargs)
        except:
            # otherwise, we do what __new__ normally does, namely generate an
            # instance of the class invoking it, i.e., of cls:
#            print("instantiating a", cls, args, kwargs)
            obj = super().__new__(cls)
        return obj

    def __init__(self, **kwargs):
        """Initialize a _Mixin instance by assigning specified values to
        all variables."""
        # extract kwargs that correspond to Variables:
        varvals = {}
        nonvarkwargs = {}
        for key, val in kwargs.items():
            if hasattr(self.__class__, key):
                clsattr = getattr(self.__class__, key)
                if isinstance(clsattr, variable.Variable):
                    varvals[clsattr] = val
                    continue
            print("unexpected (misspelled?) keyword argument",key,"=",val)
            nonvarkwargs[key] = val
        # pass other kwargs to super:
        super().__init__(**nonvarkwargs)
        # assign Variable values:
        for var, val in varvals.items():
            var.set_value(self, val)
            
    def complete_values(self):
        """assign default values to all unset Variables"""
        for var in self.variables:
            if (not hasattr(self, var.codename)  # this happens for unset properties
                or isinstance(getattr(self, var.codename), variable.Variable)):
                # class attribute was returned by getattr,
                # hence object attribute has not been assigned a value yet. 
                try:
                    var.set_to_default(self)
                except AttributeError:
                    pass

    # Jobst: object provides a sufficient __str__ I guess
#    def __str__(self):
#        return repr(self)

    def set_value(self, var, value):
        """Dummy docstring"""
        # TODO: add docstring to method
        assert isinstance(var, variable.Variable), \
            "variable must be a Variable object"
        var.set_value(self, value)

    def assert_valid(self):  # TODO: rename to "validate" when adding code that sets unset vars to default?
        """Make sure all variable values are valid.

        By calling assert_valid for all Variables

        """
        for v in self.variables:
            try:
                val = v.get_value(self)
            except:
                # TODO: set to default if unset and default exists??
                return
            v.assert_valid(val)
