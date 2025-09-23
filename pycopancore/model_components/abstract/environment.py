"""Abstract Environment process taxon class, inherited by base model
component."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore.data_model.ordered_set import OrderedSet
from pycopancore.private._abstract_process_taxon_mixin import (
    _AbstractProcessTaxonMixin,
)


class Environment(_AbstractProcessTaxonMixin):
    """Abstract Environment process taxon class.

    Inherited by base model component.
    """

    variables = OrderedSet()
    """All variables occurring in this entity type"""
