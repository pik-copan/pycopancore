"""provides this model component's World mixin class"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .... import Explicit
from .. import interface as I
from ...base import interface as B


class World (I.World):
    """
    """

    processes = [

        Explicit("aggregate flows",
                 [I.World.renewable_energy_input_flow],
                 [B.World.sum.social_systems.renewable_energy_input_flow]),
    ]
