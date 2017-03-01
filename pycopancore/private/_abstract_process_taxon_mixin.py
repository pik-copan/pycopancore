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

from pycopancore.data_model import Variable


class _AbstractProcessTaxonMixin(object):
    """Define Entity-unspecific abstract class.

    From this class all entity-specific abstract mixin classes are derived.
    """

    processes = []
    model = None
    instances = None

    def __init__(self):
        """Initialize an _AbstractProcessTaxonMixin instance."""
        if self.__class__.instances:
            self.__class__.instances.append(self)
            print('This Process Taxon is already initialized!')
        else:
            self.__class__.instances = [self]

    def set_value(self, variable, value):
        assert isinstance(variable, Variable), \
            "variable must be a Variable object"
        variable.set_value(self, value)
