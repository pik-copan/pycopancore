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

from ..data_model import variable
from ..private._expressions import _DotConstruct, aggregation_names
from ..data_model import OrderedSet

import inspect


class _AbstractProcessTaxonMixinType(type):
    """metaclass for _AbstractProcessTaxonMixin.

    Needed for intercepting
    class attribute calls and having nice reprs.
    """

    def __getattribute__(cls, name):
        """Dummy docstring"""
        # TODO: add docstring to function
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


class _AbstractProcessTaxonMixin(object, metaclass=_AbstractProcessTaxonMixinType):
    """Define Entity-unspecific abstract class.

    From this class all entity-specific abstract mixin classes are derived.
    """

    processes = []
    """All processes of this taxon"""
    model = None
    """Current model using this taxon"""
    instances = None
    """List containing the unique (!) instance of this taxon"""
    _composite_class = None
    """Composite class this mixin contributes to in the current model"""

    def __init__(self):
        """Initialize an _AbstractProcessTaxonMixin instance."""
        if self.__class__.instances:
            self.__class__.instances.append(self)
            print('This Process Taxon is already initialized!')
        else:
            self.__class__.instances = [self]

    # the repr and the str methods were removed in the master/prototype_jobst1
    # Do we really don't want them anymore?
    def __repr__(self):
        return 'Process taxon object'

    def __str__(self):
        return repr(self)

    def set_value(self, var, value):
        """Dummy docstring"""
        # TODO: missing method docstring
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
