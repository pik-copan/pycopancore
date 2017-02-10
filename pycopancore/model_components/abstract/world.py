"""Abstract class from which all World mixin class must implement."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore.private import _AbstractEntityMixin


class World (_AbstractEntityMixin):
    """Abstract class all World mixin classes must implement."""

    def __init__(self, **kwargs):
        """Initialize object."""
        super().__init__(**kwargs)

    processes = []
