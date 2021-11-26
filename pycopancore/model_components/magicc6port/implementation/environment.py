"""Enviroment process taxon mixing class template.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from ..interface import Environment as E 
from .... import Explicit

class Environment (E):
    """Environment process taxon mixin implementation class."""
    processes = [
    
        # Consistency constraints for parameters:
            
        Explicit ("NPP fraction to soils",
                  [E.NPP_fraction_to_soils],
                  [1.0 - E.NPP_fraction_to_plants - E.NPP_fraction_to_detritus]),
    
        Explicit ("Fraction of litter production going to soils",
                  [E.litter_fraction_to_soils],
                  [1.0 - E.litter_fraction_to_detritus]),
    
        Explicit ("Fraction of net landuse emissions related to soils",
                  [E.fraction_net_landuse_emiss_soils],
                  [1.0 - E.fraction_net_landuse_emiss_plants - E.fraction_net_landuse_emiss_detritus]),
    
    ]

    # NOTE: we have implemented all processes as belonging to World.