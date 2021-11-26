"""Port of MAGICC6.0 as described in Meinshausen et al. 2011

The 'Model for the Assessment of Greenhouse Gas Induced Climate Change' (MAGICC) is a simple/reduced complexity climate model. MAGICC has a hemispherically averaged upwelling-diffusion ocean coupled to an atmosphere layer and a globally averaged carbon cycle model. As with most other simple models, MAGICC evolved from a simple global average energy-balance equation. 

This port is a direct implementation of the equations given in the Appendix of Meinshausen et al. 2011 as a single pycopancore model component that uses only the entity type World and the process taxon Environment. Wherever possible, Variables, Dimensions and Units from the master_data_model have been used. For now, the master_data_model has not been extended to include further variables or units from MAGICC. A future version might do this.

Variables' 'name' and 'symbol' attributes contain the name and symbol used in Meinshausen et al. 2011, modified to improve clarity and only slightly abbreviated to avoid clutter. In particular, carbon stocks and flows contain 'cstock' or 'cflow' in their name. Their 'desc', 'CF', and 'AMIP' attributes are left empty for now but should be filled where possible soon. Their codes['MAGICC'] entry contains the name used in MAGICC input and output files.

Each of the main equations (or sometimes a group of closely related equations) is transformed into an individual process of type ODE or Explicit specified via symbolic expressions. Formulae for purely auxiliary quantities such as (A17,19) are transformed into auxiliary subexpressions. Time convolutions with polynomials such as (A23) are turned into a set of ODEs for the necessary number of derivatives of the dependent variable.
 
Processes' 'desc' attribute contain relevant text copied from Meinshausen et al. 2011 or the MAGICC wiki page, their 'ref' contains the respective equation numbers from Meinshausen et al. 2011 and a link to a related MAGICC wiki page below http://wiki.magicc.org. 

In case of conflicts between Meinshausen et al. 2011 and the MAGICC wiki page, the version in the wiki is used.

Configuration:
--------------

Before importing model_components.magicc6port in your model, import model_components.config and set its attribute 'magicc6port' to a dict of configuration options, e.g.

```
from ..model_components import config
config.magicc6port = { 
    'parameters': ['MAGTUNE_FULLTUNE_MEDIUM_CMIP3_ECS3.CFG', 
                   'MAGTUNE_C4MIP_BERN.CFG', 
                   'MAGCFG_USER.CFG'], 
    'emissions': 'RCP85.SCEN'
    }
from ..model_components import magicc6port
``` 

The following configuration options are available:

* parameters (default: None): Optional path or list of paths to one or more MAGICC tuning files (typical file extention .CFG) containing model parameter values. If None, parameters will have roughly set default values and should be filled at model initialization. If set, those values contained in the file(s) are used as initial values but could potentially be altered by other model components during the simulation run. If several listed files specify conflicting values, the first (!) specified file takes precedence (similar to python's behavior when a class derives from several base classes).

* emissions (default: None): Optional path or list of paths to one or more MAGICC emissions scenario files (typical file extension .SCEN). If None, all emissions variables default to zero and should be filled by other model components. If set, those variables contained in the files are set by the values from the files at each time point, linearly interpolated between the two closest time points surrounding the current time point that are contained in the file. If several listed files specify conflicting values, the first (!) specified file takes precedence.

All paths can be given either as absolute paths, or as relative paths relative to the folder '.../pycopancore/model_components/magicc6port/input_files'. E.g., 'scenario': 'RCP85.SCEN' will resolve to '.../pycopancore/model_components/magicc6port/input_files/RCP85.SCEN'.


References: 
-----------

* Meinshausen, M., Raper, S. C. B., & Wigley, T. M. L. (2011). Emulating coupled atmosphere-ocean and carbon cycle models with a simpler model, MAGICC6 - Part 1: Model description and calibration. Atmospheric Chemistry and Physics, 11(4), 1417–1456. https://doi.org/10.5194/acp-11-1417-2011

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
