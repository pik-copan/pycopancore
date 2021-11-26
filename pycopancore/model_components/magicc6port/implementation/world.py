"""World entity type mixing class template.

Open questions
==============

* How are Q, QA, and QS related? Q seems to be governed by H and tauH via (A6). Is Q = QA + QS? If so, are QA, QS fixed fractions of Q?

* How is R determined, and what role do the quantities \sum R and Ua in the text below (A20) play?

* How are D*gross and D*lu related? Are the latter the "net" quantities? Which of them are inputs and which outputs of the model? Is there a DPlu in the first place? 

* Is it really DPgross in (A2) but DHlu and DSlu in (A3,A4)? The text below (A21) suggests that it should be DHgross and DSgross instead.

* How are GP, GH, GS determined?

* Is N in (A16) the same as NPP?

* Is NPP really independent of P and S? Isn't it plants that grow from soil and grow larger?

* (A21) suggests there are two versions (plain and feedback-adjusted) of the quantities NPP, R, Q, and U. In which of the earlier equations (A2–A16) do we use the plain versions and in which do we use the feedback-adjusted versions? Is it correct to use first calculate the plain versions from (A16), (A??), (A6), and (A7), then calculate the feedback-adjusted ones via (A21), and then use these feedback-adjusted versions in (A2,A3,A4)? 

"""

# This file is part of pycopancore.
#
# Copyright (C) 2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

import sympy as sp

from ...base import interface as B
from ..interface import World as W, ppmvCO2
# from .... import master_data_model as D

from .... import Explicit, ODE

E = B.World.environment

class World (W):
    """World entity type mixin implementation class."""

    # auxiliary quantities:
    
    r = ((
            1 + E.NPP_enhancement_340_to_680_ppm 
                * (sp.log(E.const_680_ppmvCO2 / W.preind_cstock_atmo_CO2)) 
         ) / (
            1 + E.NPP_enhancement_340_to_680_ppm 
                * (sp.log(E.const_340_ppmvCO2 / W.preind_cstock_atmo_CO2))
        ))
    """(A17)"""
    
    b = ((
            (E.const_680_ppmvCO2 - E.NPP_zero_cstock_atmo_CO2) 
            - r * (E.const_340_ppmvCO2 - E.NPP_zero_cstock_atmo_CO2)
         ) / (
             (r - 1) 
             * (E.const_680_ppmvCO2 - E.NPP_zero_cstock_atmo_CO2) 
             * (E.const_340_ppmvCO2 - E.NPP_zero_cstock_atmo_CO2)
        ))
    """(A18)"""
    
    # processes:    
    
    processes = [
    
        # A1 The Carbon cycle
            
        ODE ("Change in atmospheric CO2 mixing ratio",
             [W.cstock_atmo_CO2],
             [W.cflow_CO2_emiss_fossil_industrial
              + W.cflow_CO2_emiss_human_biosphere
              + W.cflow_emiss_flow_methane_fuel
              - W.cflow_uptake_ocean
              - W.cflow_uptake_biosphere],
             desc="Changes in atmospheric CO2 concentration, C, are determined by CO2 emissions from fossil and industrial sources (<math>E_{\rm foss}</math>), other directly human-induced CO2 emissions from or removals to the terrestrial biosphere (<math>E_{\rm lu}</math>), the contribution from oxidized methane of fossil fuel origin (<math>E_{\rm fCH_4},</math>), the flux due to ocean carbon uptake (<math>F_{\rm ocn}</math>) and the net carbon uptake or release by the terrestrial biosphere (<math>F_{\rm terr}</math>) due to CO2 fertilization and climate feedbacks. As in the C4MIP generation of carbon cycle models, no nitrogen or sulphur deposition effects on biospheric carbon uptake are included here Thornton et al., 2006. Hence, the budget Eq.A1 for a change in atmospheric CO2 concentrations is: <math>\Delta C/\Delta t= E_{\rm foss} + E_{\rm lu} + E_{\rm fCH_4}- F_{\rm ocn} - F_{\rm terr}</math>",
             ref="(A1) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle"),

        # A1.1 Terrestrial carbon cycle
        
        ODE ("Mass balance for the plant box",
             [W.cstock_plants],
             [E.NPP_fraction_to_plants * W.cflow_net_primary_prod
              - W.cflow_het_respiration
              - W.cflow_litter_prod
              - W.cflow_gross_deforest_plants],
             desc="The plant box has two decay terms, litter production <math>L</math> and a part of gross deforestation <math>D_{\rm gross}^P</math>. Litter production is partitioned to both the detritus (<math>\phi_H</math>=98%) and soil box (<math>\phi_S</math>=1-<math>\phi_H</math>=2%). Thus, the mass balance for the plant box is: <math>\Delta P/\Delta t = g_P{\rm NPP} - R - L - D_{\rm gross}^P \label{eq_massbalance_P}</math>",
             ref="(A2) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle"),
            
        ODE ("Mass balance for the detritus box",
             [W.cstock_detritus],
             [E.NPP_fraction_to_detritus * W.cflow_net_primary_prod
              + E.litter_fraction_to_detritus * W.cflow_litter_prod
              - W.cflow_detritus_oxid
              - W.cflow_detritus_to_soil
              - W.cflow_detritus_landuse],
             desc="The detritus box has sources from litter production (<math>\phi_HL</math>) and sinks to the atmosphere due to land use (<math>D_{\rm lu}^H</math>), non-land use related oxidation (<math>Q_A</math>), and a sink to the soil box (<math>Q_S</math>). The mass balance for the detritus box is thus <math> \Delta H/\Delta t = g_H{\rm NPP} + \phi_H L - Q_A - Q_S - D_{\rm lu}^H \label{eq_massbalance_H}</math>",
             ref="(A3) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle"),
            
        ODE ("Mass balance for the soil box",
             [W.cstock_soils],
             [E.NPP_fraction_to_soils * W.cflow_net_primary_prod
              + E.litter_fraction_to_soils * W.cflow_litter_prod
              + W.cflow_detritus_to_soil
              - W.cflow_soils_oxid
              - W.cflow_soils_landuse],
             desc="The soil box has sources from litter production (<math>\phi_S</math>L), the detritus box (<math>Q_S</math>) and fluxes to the atmosphere due to land use (<math>D_{\rm gross}^S</math>), and non-land use related oxidation (<math>U</math>). The mass balance for the soil box is thus <math> \Delta S/\Delta t = g_S{\rm NPP} +\phi_S L + Q_S - U - D_{\rm lu}^S \label{eq_massbalance_S}</math>",
             ref="(A4) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle"),
            
        Explicit ("Decay of terrestrial carbon pools",
                  [W.cflow_litter_prod,
                   W.cflow_detritus_decay,
                   W.cflow_soils_oxid],
                  [W.cstock_plants / W.turnover_time_plants,
                   W.cstock_detritus / W.turnover_time_detritus,
                   W.cstock_soils / W.turnover_time_soils],
                  desc="The decay rates (<math>L</math>, <math>Q</math> and <math>U</math>) of each pool are assumed to be proportional to pool's box masses <math>P</math>, <math>H</math> and <math>S</math>, respectively.",
                  ref="(A5,A6,A7) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle"),
        # TODO: verify that A5 is actually meant to say L=P/τP for *all* timepoints, with τP given by A12, and similarly for the other two
        
        ODE ("Terrestrial carbon turnover times",
             [W.turnover_time_plants,
              W.turnover_time_detritus,
              W.turnover_time_soils],
             [- E.terrestrial_carbon_fraction_not_regrowing * E.fraction_net_landuse_emiss_plants 
              * W.cflow_CO2_emiss_human_biosphere / W.initial_cflow_litter_prod,
              # = − ψ dP Elu / L0
              - E.terrestrial_carbon_fraction_not_regrowing * E.fraction_net_landuse_emiss_detritus 
              * W.cflow_CO2_emiss_human_biosphere / W.initial_cflow_detritus_decay,
              # = − ψ dH Elu / Q0
              - E.terrestrial_carbon_fraction_not_regrowing * E.fraction_net_landuse_emiss_soils 
              * W.cflow_CO2_emiss_human_biosphere / W.initial_cflow_soils_oxid,
              # = − ψ dS Elu / U0
             ],
             desc="The turnover times <math>\tau_P</math>, <math>\tau_H</math> and <math>\tau_S</math> are determined by the initial steady-state conditions for box sizes and fluxes. <math>L_0 = P_0/\tau^P_0</math>, <math>Q_0 = H_0/\tau^H_0</math>, <math>U_0 = S_0/\tau^S_0\label{eq_terrcc_turnovertimes}</math> [...] ",
             ref="(A12,A13,A14) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Terrestrial_carbon_cycle"),           
            
        Explicit ("Effective carbon fertilization factor",
                  [W.effective_carbon_fertil_factor],
                  [(2 - E.fertilization_parameter) * (
                        # βlog (A15):
                        1 + E.NPP_enhancement_340_to_680_ppm 
                            * sp.log(W.cstock_atmo_CO2 / W.preind_cstock_atmo_CO2)
                   ) 
                   + (E.fertilization_parameter - 1) * (
                        # βsig (A19):
                        (1 / (W.preind_cstock_atmo_CO2 - E.NPP_zero_cstock_atmo_CO2) + b)
                        / (1 / (W.cstock_atmo_CO2 - E.NPP_zero_cstock_atmo_CO2) + b)
                   )],
                  desc="CO2 fertilization indicates the enhancement in net primary production (NPP) due to elevated atmospheric CO2 concentration. As described in Wigley, 2000, there are two common forms used in simple models to simulate the CO2 fertilization effect: (a) the logarithmic form (fertilization parameter <math>\beta_m</math>=1) and (b) the rectangular hyperbolic or sigmoidal growth function (<math>\beta_m</math>=2) (see e.g. Gates, 1985. The rectangular hyperbolic formulation provides more realistic results for both low and high concentrations so that NPP does not rise without limit as CO2 concentrations increase. Previous MAGICC versions include both formulations, but used the second as default. The code now allows use of a linear combination of both formulations (1<math>{\leq}{\beta_m}{\leq}</math>2). The classic logarithmic fertilization formulation calculates the enhancement of NPP as being proportional to the logarithm of the change in CO2 concentrations C above the preind level <math>C_0</math>: <math>\beta_{\rm log}=1 + \beta_s \,{\rm ln}\,({\rm C/C}_0) \label{eq_CO2fertilization_logarithm}</math>. For better comparability with models using the logarithmic formulation, following Wigley, 2000, the CO2 fertilization factor <math>\beta_s</math> expresses the NPP enhancement due to a CO2 increase from 340 ppm to 680 ppm, valid under both formulations. Thus, MAGICC first determines the NPP ratio <math>r</math> for a given <math>\beta_s</math> fertilization factor according to: <math>r=\frac{{N}(680)}{{N}(340)}=\frac{{N}_0(1+\beta_s \,{\rm ln}\,(680/Template:C_0))}{{N}_0(1+\beta_s \,{\rm ln}\, (340/{C}_0))}\label{eq_CO2fertilization_340to640}</math>. Following from here, <math>b</math> in Eq. A16 is determined by <math>b=\frac{(680-{C}_b)-r(340-{C}_b)}{(r-1)(680-{C}_b)(340-{C}_b)}\label{eq_CO2fertilization_determining b}</math> which can in turn be used in Eq. A16 to calculate the effective CO2 fertilization factor <math>\beta _{\rm sig}</math> at time <math>t</math> as <math>\beta _{\rm sig}(t)=\frac{1/({C}_0 - {C}_b) + b}{1/({C}(t)- {C}_b) + b} \label{eq_CO2fertilization_factor_michaelismenton}</math>. MAGICC6 allows for an increased flexibility, as any linear combination between the two fertilization parameterizations can be chosen (1<math>{\leq}{\beta_m}{\leq}</math>2), so that the effective fertilization factor <math>\beta _{\rm eff}</math> is given by: <math>\beta _{\rm eff}(t)=(2-\beta_m)\beta_{\rm log}+(\beta_m-1)\beta_{\rm sig}\label{eq_CO2fertilization_factor_effective}</math>",
                  ref="(A15,A17,A18,A19,A20) http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Formulation_for_CO2_fertil"),

        Explicit ("Net primary production",
                  [W.cflow_net_primary_prod],
                  [W.effective_carbon_fertil_factor * W.preind_cflow_net_primary_prod],
                  desc="The CO2 fertilization effect affects NPP so that <math>\beta_{\rm eff}</math> = NPP - NPP0.",
                  ref="(A16) and below (A20), http://wiki.magicc.org/index.php?title=The_Carbon_Cycle#Formulation_for_CO2_fertil"),
            

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
