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
        assert len(self.__class__.instances) == 0, \
            "process taxa can be instantiated only once!"
        super().__init__(*args, **kwargs)
#        if self.__class__.instances:
#            self.__class__.instances.append(self)
#            print('This Process Taxon is already instantiated!')
#        else:
        self.__class__.instances = [self]

    # the repr and the str methods were removed in the master/prototype_jobst1
    # Do we really don't want them anymore?
    # Jobst: object provides a sufficient __repr__ I guess
#    def __repr__(self):
#        return 'Process taxon object'
