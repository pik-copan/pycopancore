"""Port of MAGICC6.0 as described in Meinshausen et al. 2008

The 'Model for the Assessment of Greenhouse Gas Induced Climate Change' (MAGICC) is a simple/reduced complexity climate model. MAGICC has a hemispherically averaged upwelling-diffusion ocean coupled to an atmosphere layer and a globally averaged carbon cycle model. As with most other simple models, MAGICC evolved from a simple global average energy-balance equation. 

This port is a direct implementation of the equations given in the Appendix of Meinshausen et al. 2008 as a single pycopancore model component that uses only the entity type World and the process taxon Environment. Wherever possible, Variables, Dimensions and Units from the master_data_model have been used. For now, the master_data_model has not been extended to include further variables or units from MAGICC. A future version might do this.

Variables' 'name' and 'symbol' attributes contain the name and symbol used in Meinshausen et al. 2008, modified to improve clarity. In particular, carbon stocks and flows contain 'cstock' or 'cflow' in their name. Their 'desc', 'CF', and 'AMIP' attributes are left empty for now but should be filled where possible soon. 

Processes' 'desc' attribute contain relevant text copied from Meinshausen et al. 2008 or the MAGICC wiki page, their 'ref' contains the respective equation numbers from Meinshausen et al. 2008 and a link to a related MAGICC wiki page. 

In case of conflicts between Meinshausen et al. 2008 and the MAGICC wiki page, the version in the wiki is used.

References: 
* Meinshausen, M., Raper, S. C. B., & Wigley, T. M. L. (2008). Emulating IPCC AR4 atmosphere-ocean and carbon cycle models for projecting global-mean, hemispheric and land/ocean temperatures: MAGICC 6.0. Atmospheric Chemistry and Physics Discussions, 8(2), 6153–6272.
* http://wiki.magicc.org
* http://wiki.magicc.org/index.php?title=Creating_MAGICC_Scenario_Files
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from . import interface as I
# import all needed entity type implementation classes:
from .implementation import World
# import all needed process taxon implementation classes:
from .implementation import Environment


class Model (I.Model):
    """Model mixin class."""

    # mixins provided by this model component:

    entity_types = [World]
    """list of entity types augmented by this component"""
    process_taxa = [Environment]
    """list of process taxa augmented by this component"""
