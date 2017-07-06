"""Abstract Individual entity type class, inherited by base model component."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from ...private import _AbstractEntityMixin
from ...data_model import OrderedSet


class Individual (_AbstractEntityMixin):
    """Abstract Individual entity type class.

    Inherited by base model component.
    """

    variables = OrderedSet()
    """All variables occurring in this entity type"""
