from .dimensions_and_units import *

from . import environment, metabolism #, culture
from . import environment as NAT
from . import environment as Environment
from . import metabolism as MET
from . import metabolism as Metabolism

# this way sphinx will include Variables from MDM:
# TODO: do the same for other taxa and entity types in MDM!
from .culture import Culture as CUL
from .culture import Culture as culture
from .culture import Culture

from . import world, social_system, cell, individual
from . import world as W
from . import world as World
from . import social_system as S
from . import social_system as SocialSystem
from . import cell as C
from . import cell as Cell
from . import individual as I
from . import individual as Individual

from .. import unity

# what models need:


# NATURE:

# GLOBAL, Anderies, Kellie-Smith--Cox:
#    terrestrial_carbon = vegetation_biomass = harvestable_biomass
#    geological_carbon = extractable_fossil_fuel
#    maritime_carbon = upper_oceans_carbon
#    atmospheric_carbon
#    global_mean_surface_air_temperature
#    +parameters

# Steven:
#    deep_ocean_carbon?

# Werner:
#    ?

# EXPLOIT, Brander--Taylor, Jobst para1:
#    harvestable_resource (= harvestable_biomass or harvestable_fish)
#    resource_basic_growth_rate
#    resource_capacity


# METABOLISM:

# GLOBAL, Brander--Taylor:
#    population = labour
#    economic_production (final sector)
#    human_wellbeing (per capita consumption plus ecosystem services)
#

#
