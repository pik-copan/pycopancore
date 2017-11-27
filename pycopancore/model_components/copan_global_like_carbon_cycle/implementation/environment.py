"""provides this model component's Environment mixin class"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I


class Environment (I.Environment):
    """Environment process taxon mixin implementation class."""

    processes = []
