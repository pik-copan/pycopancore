"""_abstract_dynamics_mixin class.

It sets the basic structure of dynamic mixins (culture, metabolism, nature).
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license


from . import _Mixin


class _AbstractProcessTaxonMixin(_Mixin):
    """Define Entity-unspecific abstract class.

    From this class all entity-specific abstract mixin classes are derived.
    """

    def __init__(self, *args, **kwargs):
        """Initialize an _AbstractProcessTaxonMixin instance."""
        assert self.__class__.instances is None, \
            "process taxa can be instantiated only once!"
        super().__init__(*args, **kwargs)
#        if self.__class__.instances:
#            self.__class__.instances.append(self)
#            print('This Process Taxon is already instantiated!')
#        else:
        self.__class__.instances = [self]

    def delete(self):
        """Delete this Process Taxon from lists."""
        # Remove from list, if list is existent:
        if (self in self.__class__.instances
                and self.__class__.instances):
            self.__class__.instances.remove(self)
        # If list then has lenght == 0, set it to None again, so everything is
        # fresh again...
        if (len(self.__class__.instances) == 0
                and self.__class__.instances):
            self.__class__.instances = None
        # Delete for good:
        del(self)
