"""Abstract SocialSystem entity type class, inherited by base model
component."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore.data_model.ordered_set import OrderedSet
from pycopancore.private._abstract_entity_mixin import (
    _AbstractEntityMixin,
)


class SocialSystem(_AbstractEntityMixin):
    """Abstract SocialSystem entity type class.

    Inherited by base model component.
    """

    variables = OrderedSet()
    """All variables occurring in this entity type"""
