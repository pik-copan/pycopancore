"""model component Interface.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# Use variables from the master data model wherever possible
from ... import master_data_model as D
from ...data_model.master_data_model import unity, GtC, yr
from ... import Variable

class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "Port of MAGICC6.0 as described in Meinshausen et al. 2008"
    """a unique name for the model component"""
    description = "The 'Model for the Assessment of Greenhouse Gas Induced Climate Change' (MAGICC) is a simple/reduced complexity climate model."
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""
    version = 0.1
    """model component version number"""

#
# Entity types
#
class World (object):
    """Interface for World mixin."""

    # EXOGENOUS variables (drivers):

    initial_carbon_flow_litter_production = Variable(
        "Initial litter production", "Note: this is needed for (A12)",  
        symbol="L0", CF=None, AMIP=None,
        unit=GtC/yr, strict_lower_bound=0, is_extensive=True)

    initial_carbon_flow_detritus_decay = Variable(
        "Initial decay of detritus", "Note: this is needed for (A13)",  
        symbol="Q0", CF=None, AMIP=None,
        unit=GtC/yr, strict_lower_bound=0, is_extensive=True)

    initial_carbon_flow_soils_oxidization = Variable(
        "Initial soils sink due to non-landuse related oxidization", "Note: this is needed for (A14)",  
        symbol="U0", CF=None, AMIP=None,
        unit=GtC/yr, strict_lower_bound=0, is_extensive=True)

    carbon_flow_CO2_emissions_fossil_industrial = Variable(
        "CO2 emissions from fossil and industrial sources", "",  
        symbol="Efoss", CF=None, AMIP=None,
        unit=GtC/yr, is_extensive=True, default=0)
    
    carbon_flow_CO2_emissions_human_biosphere = Variable(
        "Other directly human-induced CO2 emissions from or removals to the terrestrial biosphere", "",  
        symbol="Elu", CF=None, AMIP=None,
        unit=GtC/yr, is_extensive=True, default=0)
    
    carbon_flow_emissions_flow_methane_fuel = Variable(
        "Contribution from oxidized methane of fossil fuel origin", "",  
        symbol="EfCH4", CF=None, AMIP=None,
        unit=GtC/yr, lower_bound=0, is_extensive=True, default=0)

    carbon_flow_gross_deforestation = Variable(
        "gross deforestation", "",  
        symbol="DPlu", CF=None, AMIP=None,
        unit=GtC/yr, is_extensive=True, default=0)

    # ENDOGENOUS variables:

    # A1 The Carbon cycle

    carbon_stock_atmospheric_CO2 = Variable(
        "atmospheric carbon stored as CO2", "Note: in the paper this was called 'mixing ratio' with symbol 'χCO2', in the wiki 'concentration' with symbol 'C', but units suggest it is actually a carbon *stock*",  
        symbol="C", CF=None, AMIP=None,
        unit=GtC, strict_lower_bound=0, is_extensive=True)
    # Note: we are *not* using D.World.atmospheric_carbon since the latter is meant to contain non-CO2 carbon with respective multipliers related to CO2-equivalents, while this here is really just the C stored in CO2.
        
    carbon_flow_uptake_ocean = Variable(
        "Flux due to ocean carbon uptake", "Note: Despite the word 'flux', this is *not* per-area.",  
        symbol="Focn", CF=None, AMIP=None,
        unit=GtC/yr, is_extensive=True, default=0)

    carbon_flow_uptake_biosphere = Variable(
        "Net non-‘directly human-induced’ carbon uptake or release by the terrestrial biosphere "
        "due to CO2 fertilization and climate feedbacks", "",  
        symbol="Fterr", CF=None, AMIP=None,
        unit=GtC/yr, is_extensive=True, default=0)

    # A1.1 Terrestrial carbon cycle

    carbon_stock_living_plants = Variable(
        "Living plants", "Woody material, leaves/needles, grass, and roots, but not the rapid turnover part of living biomass, which can be assumed to have a zero lifetime on the timescales of interest here",  
        symbol="P", CF=None, AMIP=None,
        unit=GtC, strict_lower_bound=0, is_extensive=True)

    carbon_stock_detritus = Variable(
        "Detritus", "",  
        symbol="H", CF=None, AMIP=None,
        unit=GtC, strict_lower_bound=0, is_extensive=True)

    carbon_stock_soils = Variable(
        "Organic matter in soils", "",  
        symbol="S", CF=None, AMIP=None,
        unit=GtC, strict_lower_bound=0, is_extensive=True)

    carbon_flow_net_primary_production = Variable(
        "Net primary production", "",  
        symbol="NPP", CF=None, AMIP=None,
        unit=GtC/yr, lower_bound=0, is_extensive=True, default=0)

    carbon_flow_litter_production = Variable(
        "Litter production", "",  
        symbol="L", CF=None, AMIP=None,
        unit=GtC/yr, lower_bound=0, is_extensive=True, default=0)

    carbon_flow_detritus_landuse = Variable(
        "Detritus sink to the atmosphere due to landuse", "",  
        symbol="DHlu", CF=None, AMIP=None,
        unit=GtC/yr, is_extensive=True, default=0)
    # TODO: verify this is not exogenous!

    carbon_flow_detritus_decay = Variable(
        "Decay of detritus", "Note: this is assumed to be the sum of QA and QS",  
        symbol="Q", CF=None, AMIP=None,
        unit=GtC/yr, lower_bound=0, is_extensive=True, default=0)

    carbon_flow_detritus_oxidization = Variable(
        "Detritus sink to the atmosphere due to non-landuse related oxidization", "",  
        symbol="QA", CF=None, AMIP=None,
        unit=GtC/yr, lower_bound=0, is_extensive=True, default=0)

    carbon_flow_detritus_to_soil = Variable(
        "Detritus sink to the soils", "",  
        symbol="QS", CF=None, AMIP=None,
        unit=GtC/yr, lower_bound=0, is_extensive=True, default=0)

    carbon_flow_soils_landuse = Variable(
        "Soils sink to the atmosphere due to landuse", "",  
        symbol="DSlu", CF=None, AMIP=None,
        unit=GtC/yr, is_extensive=True, default=0)
    # TODO: verify this is not exogenous!

    carbon_flow_soils_oxidization = Variable(
        "Soils sink due to non-landuse related oxidization", "",  
        symbol="U", CF=None, AMIP=None,
        unit=GtC/yr, lower_bound=0, is_extensive=True, default=0)

    carbon_flow_heterotrophic_respiration = Variable(
        "Heterotrophic_respiration", "",  
        symbol="R", CF=None, AMIP=None,
        unit=GtC/yr, lower_bound=0, is_extensive=True, default=0)
    # TODO: identify equation and definition in text!
    
    turnover_time_living_plants = Variable(
        "Turnover time of living plants", "Inverse of decay rate, should be initially P/L",  
        symbol="τP", CF=None, AMIP=None,
        unit=yr, strict_lower_bound=0, is_extensive=False)

    turnover_time_detritus = Variable(
        "Turnover time of detritus", "Inverse of decay rate, should be initially H/Q",  
        symbol="τH", CF=None, AMIP=None,
        unit=yr, strict_lower_bound=0, is_extensive=False)

    turnover_time_soils = Variable(
        "Turnover time of soils", "Inverse of decay rate, should be initially S/U",  
        symbol="τS", CF=None, AMIP=None,
        unit=yr, strict_lower_bound=0, is_extensive=False)

    
    """
     = Variable(
        "", "",  
        symbol="", CF=None, AMIP=None,
        unit=, lower_bound=, is_extensive=, default=0)

    """
    

#
# Process taxa
#
class Environment (object):
    """Interface for Environment process taxon mixin."""

    # EXOGENOUS PARAMETERS:      

    NPP_fraction_to_living_plants = Variable(
        "NPP flux: carbon fluxes to the remainder plant box", "Note: this is actually not a flux but simply a fraction",  
        symbol="gP", CF=None, AMIP=None,
        unit=unity, lower_bound=0, upper_bound=1, is_extensive=True, default=0.35)

    NPP_fraction_to_detritus = Variable(
        "NPP flux: carbon fluxes to the detritus box", "Note: this is actually not a flux but simply a fraction",  
        symbol="gH", CF=None, AMIP=None,
        unit=unity, lower_bound=0, upper_bound=1, is_extensive=True, default=0.60)

    litter_fraction_to_detritus = Variable(
        "Fraction of litter production going to detritus", "",  
        symbol="φH", CF=None, AMIP=None,
        unit=unity, lower_bound=0, upper_bound=1, is_extensive=True, default=0.98)

    terrestrial_carbon_fraction_not_regrowing = Variable(
        "Terrestrial carbon fraction that will not regrow", "",  
        symbol="ψ", CF=None, AMIP=None,
        unit=unity, lower_bound=0, upper_bound=1, is_extensive=True, default=0)

    fraction_net_landuse_emissions_living_plants = Variable(
        "Fraction of net landuse emissions related to living plants", "Note: dP does not seem to have a name in MAGICC",  
        symbol="dP", CF=None, AMIP=None,
        unit=unity, lower_bound=0, upper_bound=1, is_extensive=True, default=0)

    fraction_net_landuse_emissions_detritus = Variable(
        "Fraction of net landuse emissions related to detritus", "Note: dH does not seem to have a name in MAGICC",  
        symbol="dH", CF=None, AMIP=None,
        unit=unity, lower_bound=0, upper_bound=1, is_extensive=True, default=0)

    


    # ENDOGENOUS quantities:

    NPP_fraction_to_soils = Variable(
        "NPP flux: carbon fluxes to the soil box", "Note: this is actually not a flux but simply a fraction",  
        symbol="gS", CF=None, AMIP=None,
        unit=unity, lower_bound=0, upper_bound=1, is_extensive=True, default=0.05)
    # calculated as 1 - NPP_fraction_to_living_plants - NPP_fraction_to_detritus

    litter_fraction_to_soils = Variable(
        "Fraction of litter production going to soils", "",  
        symbol="φS", CF=None, AMIP=None,
        unit=unity, lower_bound=0, upper_bound=1, is_extensive=True, default=0.02)
    # calculated as 1 - litter_fraction_to_detritus

    fraction_net_landuse_emissions_soils = Variable(
        "Fraction of net landuse emissions related to soils", "Note: dS does not seem to have a name in MAGICC",  
        symbol="dS", CF=None, AMIP=None,
        unit=unity, lower_bound=0, upper_bound=1, is_extensive=True, default=0)
    # calculated as 1 - fraction_net_landuse_emissions_living_plants - fraction_net_landuse_emissions_detritus 

    

    """
     = Variable(
        "", "",  
        symbol="", CF=None, AMIP=None,
        unit=, lower_bound=, is_extensive=, default=0)

    """
        
        
