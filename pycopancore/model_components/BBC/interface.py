
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from ... import Variable

class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "BBC"
    """Behaviour-Bisophere-Climate Model"""
    description = "simple model for evaluating co-evolutionary danamics of human behaviour and Climate Change as well as Biosphere Integrity "


class Environment (object):
    #Variables
    temperature = Variable("Temperature",
                           """global mean temperature""",
                           default=0)
    temperature_slope = Variable("Temperature Slope",
                                 """Calculates the slope of the temperature. Is used for calculation the permafrost melting""",
                                 default=0)
    carbon_atmosphere = Variable("Carbon in the atmosphere",
                                 "Variable that captures the current atmospheric carbon in PgC",
                                 default=589)
    carbon_terrestrial = Variable("Carbon on land",
                                 "Variable that captures the current terrestrial carbon in PgC",
                                 default=1875)
    carbon_mixed_laxer = Variable("mixed layer carbon",
                                  "Variable that captures the current carbon ine ocean mixed layer in PgC",
                                  default=900)
    carbon_system = Variable("system carbon",
                             "carbon of the earth system in PgC",
                             default=0)
    terrestrial_carbon_cap = Variable("terrestrial carbon capacity",
                                      "terrestrial carbon carrying capacity",
                                      default=0)
    partial_pressure = Variable("partial pressure of CO2",
                                "partial pressure that is determined by the ocean carbon",
                                default=0)
    response_lag = Variable("response lag",
                            "global mean surface temperature to which global distributions of species are currently best adapted",
                            default=0)
    productivity = Variable("productivity",
                            "biodiversity productivity",
                            default=0)
    bio_pump_strength = Variable("biological pump strength",
                                 "strength of the biological pump",
                                 default=13)
    perma_carbon = Variable("permafrost carbon emissions",
                            "cumulative emissions from permafrost",
                            default=0)
    perma_temperature = Variable("Permafrost Temperature",
                                 "temperature of permafrost",
                                 default=0)
    J = Variable("Global measure of biodiversity",
                 "Variable to capture the current global state of biodiversity",
                 default=1)

    #Parameter
    K_c = Variable("Fertilization effect",
                   "Effect size of fertilization",
                   default=0.3)
    c_a0 = Variable("pre-industrial atmospheric carbon",
                    "pre-industrial atmospheric carbon stock",
                    default=589)
    Q_R = Variable("Terrestrial respiration temperature dependence",
                   "Dependence rate of the terrestrial respiration temperature",
                   default=1.72)
    c_t0 = Variable("pre-industrial terrestrial carbon",
                    "pre- industrial terrestrial carbon stock",
                    default=1875)
    K_A = Variable("Terrestrial carbon storage loss due to response lag",
                   "Loss of terrestrail carbon storage due to the response lag of the biosphere th chnages in the climate",
                   default=55)
    Dd = Variable("Atmosphere-ocean co2 diffusion",
                  "Diffusion rate of atmosphere-ocean co2",
                  default=1)
    c_m0 = Variable("pre-industrial mixed-layer carbon",
                    "pre-industrial mixed-layer carbon stock",
                    default=900)
    r = Variable("Revelle (buffer) factor",
                 "ratio of instantaneous change in CO2 to the change in total dissolved inorganic carbon",
                 default=12.5)
    D_T = Variable("Reduction of solubility with temperature",
                   "redaction rate of CO2 solubility in the ocean, depending on temperature",
                   default=0.0423)
    B_0 = Variable("Pre-industrial strength of the biological pump",
                   "strength of the pre-industrail biologial pump in the ocean",
                   default=13)
    B_T = Variable("Temperature dependence of biological pump",
                   "rate to with the strength of the biological pump changes wit a rising temperature",
                   default=0.12 / 3.7)
    B_TB = Variable("Biodiversity mediated temperature effects on the biological pump",
                    "changes in the strength of the biological pump in the ocean due to changes in biodiversity",
                    default=0.007)
    B_A = Variable("Biodiversity mediated acidification effects on the biological pump",
                   "changes in the strength of the biological pump in the ocean due to changes in the acidification rate of the ocean",
                   default=0.00298 / (16.43 - 0.00298 * 589 / 2.134))
    w_0 = Variable("solubility pump rate",
                   "solubility pump rate of CO2 in the ocean",
                   default=0.1)
    w_T = Variable("weakening of overturning circulation with cc",
                   "rate to which the overturning circulation weakens with increasing cc effects",
                   default=0.1)
    tau = Variable("climate lag",
                   "time lag between the release of carbon an climate effects",
                   default=4)
    lam = Variable("transit climate sensitivity",
                   "the global temperature rise following a doubling of CO2 concentration in the atmosphere compared to pre-industrial levels",
                   default=1.8)
    NPP = Variable("Pre-industrial net primary production",
                   "pre-industrial biomass production of primary producers",
                   default=55)
    I_CC = Variable("Effect of climate chnage on biodiversity",
                    "direct effect of climate change on biodiversity",
                    default=0.05)
    teta = Variable("exponent in the biodiversity-function relationship",
                    "parameter that mediates the biodiversity function relationship",
                    default=0.26)
    v_max = Variable("maximum response rate",
                     "maximal response rate that the ecosystems need to adapt to changes in temperature",
                     default=0.2 / 10)
    r_g = Variable("response relaxation rate",
                   "response rate to the ecosystems to changes in temperature",
                   default=0.025)
    p_T = Variable("permafrost thaw temperature response",
                   "rate to which the permafrost is melting with rising temperatures",
                   default=22.5)




class Culture (object):
    #Variables:
    perceived_risk_CC = Variable("perceived risk from climate change",
                                 "the risk people perceive from an increasing climate change",
                                 default=0)
    attitude_CC = Variable("attitude towards climate change",
                           "attitudes of people towards the state of climate change",
                           default=0)
    behavioural_change_CC = Variable("behavioural change",
                                     "rate to which people will take more or less action to prevent climate change",
                                     default=0)
    perceived_risk_BD = Variable("perceived risk from biodiversity loss",
                                 "the risk people perceive from an increasing loss of biodiversity",
                                 default=0)
    attitude_BD = Variable("attitudes towards biodiversity loss",
                           "attitudes of people towards the state of the biosphere integrity",
                           default=0)
    behavioural_change_BD = Variable("behavioural change",
                                     "rate to which people will take more or less action to prevent biodiversity loss",
                                     default=0)
    behavioural_intention_CC = Variable("behavioural intention",
                                        "rate to which people intend to take more or less action to prevent climate change",
                                        default=0)
    behavioural_intention_BD = Variable("behavioural intention",
                                        "rate to which people intend to take more or less action to prevent biodiversity loss",
                                        default=0)

    #Parameter:
    Ef_BD = Variable("perceived efficacy BD",
                     "rate to which people gave the feeling that their actions have an effect",
                     default=0.5)
    SN_BD = Variable("subjective norm BD",
                     "perceived nor of taking  action th prevent biodiversity loss",
                     default=0)
    PBC_BD = Variable("perceived behavioural control BD",
                      "rate to which people have the feeling that they can control their own actions",
                      default=0)
    alp = Variable("Relation between Attitude towards Biosphere Integrity and Climate change",
                   "factor that relates the magnitude of both attitudes",
                   default=0.66)
    Ef_CC = Variable("perceived efficacy CC",
                     "rate to which people gave the feeling that their actions have an effect",
                     default=0.5)
    SN_CC = Variable("subjective norm CC",
                     "perceived nor of taking  action th prevent biodiversity loss",
                     default=0)
    PBC_CC = Variable("perceived behavioural control BD",
                      "rate to which people have the feeling that they can control their own actions",
                      default=0)
    w1 = Variable("weight1",
                  "weight for the relation of attitude and efficacy",
                  default=0.5)
    w2 = Variable("weight2",
                  "weight of the calculation of the behaviour change",
                  default=0.5)
    wA = Variable("weightA",
                  "weight for attitude in linear implementation",
                  default=0.5)
    wN = Variable("weightN",
                  "weight for subjective norm in linear implementation",
                  default=0.5)
    wC = Variable("weightC",
                  "weight for perceived behavioural control in linear implementation",
                  default=0.5)
    PR = Variable("Perceived Risk",
                  "the version of the functional form of the perceived risk calculated",
                  default=1)
    TPB = Variable("Theory of planned behaviour",
                   "the version of the theory of planned behaviour calculated",
                   default=1)



class Metabolism (object):
    #Variables:
    max_change_CC = Variable("maximal possible change in emissions",
                             "the mitigation response can change to a maximum in each time step",
                             default=0)
    max_change_BD = Variable("maximal possible change in biodiversity impacts",
                             "the mitigation response can change to a maximum in each time step",
                             default=0)
    cum_CC = Variable("cumulative behaviour change CC",
                      "sum of all behaviour changes over time for CC",
                      default=0)
    cum_BD = Variable("cumulative behaviour change CC",
                      "sum of all behaviour changes over time for CC",
                      default=0)

    e = Variable("fossil fuel emissions",
                 "fossil fuel emissions depending on RCP scenario",
                 default=0)
    J_d = Variable("BD loss from human impacts",
                   "Impact of human on biodiversity depending on RCP scenario",
                   default=0.1)
    e_new = Variable("new emissions",
                     "updated emission based on human behaviour",
                     default=e)
    J_d_new = Variable("new Impact of humans on biodiversity",
                       "updated impact of humans on biodiversity based on the calculated himan behaviour",
                       default=J_d)

    #Parameter:
    LUC = Variable("Land-use emissions",
                   "Emissions from land-use based on RCP scenario",
                   default=.003)
    emission_array = Variable("emissions",
                                "array of emissions for each time step based on RCP scenario")
    LUC_array = Variable("LUC",
                           "LUC per time step for chosen RCP scenario")
    i_min = Variable("maximal direct human impact on biodiversity",
                        "maximal direct human impact on biodiversity in each time step",
                        default=0.1)
    R_max_BD = Variable("Maximal behaviour change rate BD",
                        "maximal rate to which the behaviour can change from one time step to another",
                        default=0.05)
    e_min = Variable("maximal emissions", "maximal emissions in each time step",
                        default=5.4)
    R_max_CC = Variable("Maximal behaviour change rate CC",
                        "maximal rate to which the behaviour can change from one time step to another",
                        default=0.05)


class World (object):
    run_counter = Variable("run counter", "counts the number of runs", default=0)
