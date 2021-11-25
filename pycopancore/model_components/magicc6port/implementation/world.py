"""World entity type mixing class template.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

"""
Implementation strategy
"""

from ..interface import Environment as E 
from ..interface import World as W 
# from .... import master_data_model as D

from .... import Explicit, ODE

class World (W):
    """World entity type mixin implementation class."""

    # process-related methods:

    processes = [
    
        # A1 The Carbon cycle
            
        ODE ("Change in atmospheric CO2 mixing ratio",
             [W.carbon_stock_atmospheric_CO2],
             [W.carbon_flow_CO2_emissions_fossil_industrial
              + W.carbon_flow_CO2_emissions_human_biosphere
              + W.carbon_flow_emissions_flow_methane_fuel
              - W.carbon_flow_uptake_ocean
              - W.carbon_flow_uptake_biosphere],
             desc="Changes in atmospheric CO2 concentration, C, are determined by CO2 emissions from fossil and industrial sources (<math>E_{\rm foss}</math>), other directly human-induced CO2 emissions from or removals to the terrestrial biosphere (<math>E_{\rm lu}</math>), the contribution from oxidized methane of fossil fuel origin (<math>E_{\rm fCH_4},</math>), the flux due to ocean carbon uptake (<math>F_{\rm ocn}</math>) and the net carbon uptake or release by the terrestrial biosphere (<math>F_{\rm terr}</math>) due to CO2 fertilization and climate feedbacks. As in the C4MIP generation of carbon cycle models, no nitrogen or sulphur deposition effects on biospheric carbon uptake are included here Thornton et al., 2006. Hence, the budget Eq.A1 for a change in atmospheric CO2 concentrations is: <math>\Delta C/\Delta t= E_{\rm foss} + E_{\rm lu} + E_{\rm fCH_4}- F_{\rm ocn} - F_{\rm terr}</math>",
             ref="(A1) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle"),

        # A1.1 Terrestrial carbon cycle
        
        ODE ("Mass balance for the plant box",
             [W.carbon_stock_living_plants],
             [E.NPP_fraction_to_living_plants * W.carbon_flow_net_primary_production
              - W.carbon_flow_heterotrophic_respiration
              - W.carbon_flow_litter_production
              - W.carbon_flow_gross_deforestation],
             desc="The plant box has two decay terms, litter production <math>L</math> and a part of gross deforestation <math>D_{\rm gross}^P</math>. Litter production is partitioned to both the detritus (<math>\phi_H</math>=98%) and soil box (<math>\phi_S</math>=1-<math>\phi_H</math>=2%). Thus, the mass balance for the plant box is: <math>\Delta P/\Delta t = g_P{\rm NPP} - R - L - D_{\rm gross}^P \label{eq_massbalance_P}</math>",
             ref="(A2) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle"),
            
        ODE ("Mass balance for the detritus box",
             [W.carbon_stock_detritus],
             [E.NPP_fraction_to_detritus * W.carbon_flow_net_primary_production
              + E.litter_fraction_to_detritus * W.carbon_flow_litter_production
              - W.carbon_flow_detritus_oxidization
              - W.carbon_flow_detritus_to_soil
              - W.carbon_flow_detritus_landuse],
             desc="The detritus box has sources from litter production (<math>\phi_HL</math>) and sinks to the atmosphere due to land use (<math>D_{\rm lu}^H</math>), non-land use related oxidation (<math>Q_A</math>), and a sink to the soil box (<math>Q_S</math>). The mass balance for the detritus box is thus <math> \Delta H/\Delta t = g_H{\rm NPP} + \phi_H L - Q_A - Q_S - D_{\rm lu}^H \label{eq_massbalance_H}</math>",
             ref="(A3) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle"),
            
        ODE ("Mass balance for the soil box",
             [W.carbon_stock_soils],
             [E.NPP_fraction_to_soils * W.carbon_flow_net_primary_production
              + E.litter_fraction_to_soils * W.carbon_flow_litter_production
              + W.carbon_flow_detritus_to_soil
              - W.carbon_flow_soils_oxidization
              - W.carbon_flow_soils_landuse],
             desc="The soil box has sources from litter production (<math>\phi_S</math>L), the detritus box (<math>Q_S</math>) and fluxes to the atmosphere due to land use (<math>D_{\rm gross}^S</math>), and non-land use related oxidation (<math>U</math>). The mass balance for the soil box is thus <math> \Delta S/\Delta t = g_S{\rm NPP} +\phi_S L + Q_S - U - D_{\rm lu}^S \label{eq_massbalance_S}</math>",
             ref="(A4) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle"),
            
        Explicit ("Decay of terrestrial carbon pools",
                  [W.carbon_flow_litter_production,
                   W.carbon_flow_detritus_decay,
                   W.carbon_flow_soils_oxidization],
                  [W.carbon_stock_living_plants / W.turnover_time_living_plants,
                   W.carbon_stock_detritus / W.turnover_time_detritus,
                   W.carbon_stock_soils / W.turnover_time_soils],
                  desc="The decay rates (<math>L</math>, <math>Q</math> and <math>U</math>) of each pool are assumed to be proportional to pool's box masses <math>P</math>, <math>H</math> and <math>S</math>, respectively.",
                  ref="(A5,A6,A7) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle"),
        # TODO: verify that A5 is actually meant to say L=P/τP for *all* timepoints, with τP given by A12, and similarly for the other two
        
        ODE ("Terrestrial carbon turnover times",
             [W.turnover_time_living_plants,
              W.turnover_time_detritus,
              W.turnover_time_soils],
             [- E.terrestrial_carbon_fraction_not_regrowing * E.fraction_net_landuse_emissions_living_plants 
              * W.carbon_flow_CO2_emissions_human_biosphere / W.initial_carbon_flow_litter_production,
              # = − ψ dP Elu / L0
              - E.terrestrial_carbon_fraction_not_regrowing * E.fraction_net_landuse_emissions_detritus 
              * W.carbon_flow_CO2_emissions_human_biosphere / W.initial_carbon_flow_detritus_decay,
              # = − ψ dH Elu / Q0
              - E.terrestrial_carbon_fraction_not_regrowing * E.fraction_net_landuse_emissions_soils 
              * W.carbon_flow_CO2_emissions_human_biosphere / W.initial_carbon_flow_soils_oxidization,
              # = − ψ dS Elu / U0
             ],
             desc="The turnover times <math>\tau_P</math>, <math>\tau_H</math> and <math>\tau_S</math> are determined by the initial steady-state conditions for box sizes and fluxes. <math>L_0 = P_0/\tau^P_0</math>, <math>Q_0 = H_0/\tau^H_0</math>, <math>U_0 = S_0/\tau^S_0\label{eq_terrcc_turnovertimes}</math> [...] ",
             ref="(A12,A13,A14) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle"),
            
    ]
    """
        ODE ("",
             [W.],
             [],
             desc="",
             ref="() "),
            
        Explicit ("",
                  [W.],
                  [],
                  desc="",
                  ref="() "),
            
    """
