"""Abstract Individual entity type class, inherited by base model component."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from pycopancore.data_model.ordered_set import OrderedSet
from pycopancore.private._abstract_entity_mixin import (
    _AbstractEntityMixin,
)


class Individual(_AbstractEntityMixin):
    """Abstract Individual entity type class.

    Inherited by base model component.
    """

    variables = OrderedSet()
    """All variables occurring in this entity type"""
