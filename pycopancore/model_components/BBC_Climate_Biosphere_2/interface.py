"""model component Interface template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:", then
remove these instructions.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# Use variables from the master data model wherever possible
#from ... import master_data_model as D
#from ...data_model.master_data_model import W
#from ...data_model import Dimension, Unit
#from ...import base as B
# TODO: uncomment and adjust to use variables from other pycopancore model
# components:
#from ..import BBC_Biosphere as BS
# from ..MODEL_C import interface as MODEL_COMPONENT

# TODO: uncomment and adjust only if you really need other variables:
from pycopancore import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "climate system"
    """a unique name for the model component"""
    description = "the climate system of the model"
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons



# Process taxa
#
class Environment (object):
    """Interface for Environment process taxon mixin."""

    # endogenous variables:
    #temperature=W.surface_air_temperature
    #carbon_atmosphere=W.atmospheric_carbon
    #carbon_terrestial=W.terrestrial_carbon
    #carbon_ocean=W.ocean_carbon

    dummy_variable=Variable("Dummy", """This does nothing""", default=0)
    temperature_slope=Variable("slope","""slop of temp""")

    temperature=Variable("Temperature","find better description",default=0)
    carbon_atmosphere=Variable("Carbon in the athmosphere","find better description", default=589, lower_bound=0)
    carbon_terrestial = Variable("Carbon on land", "find better description", default=1875)
    #carbon_ocean=Variable("caron in the oecan","find better description", default=900)
    terrestrial_carbon_cap = Variable ("terrestrial carbon carpacits", 
                                      "terrestrial crbon carring capacity", default=1687.5)
    carbon_mixed_laxer=Variable("mixed layer carbon",
                               "carbon in the ocean mixed layer", default=900)
    partial_pressure=Variable("partial pressure of co2", 
                              "partical pressure that is determined by the ocean carbon", default=589)
    carbon_system=Variable("system carbon", "carbon of the whole system", default=0)
    K_c = Variable("Fertilization effect", "Effect size of fertilization", default=0.3)
    c_a0 = Variable("initial atmospheric carbon","pre- industrial atmospheric carbon stock", default=589)
    Q_R = Variable("Terrestrial respiration temperature dependance", "Dependace rate of the terrestrial respiration teperature", default=1.72)
    c_t0 = Variable("initial terrestrial carbon","pre- industrial terrestrial carbon stock", default=1875)
    K_A = Variable("Terrestrail carbon storrage loss", "Loss of terrestrail carbon storrage due to the response lag", default=55)
    Dd = Variable ("Atmosphere-ocean co2 diffusion","Diffusion rate of atmosphere-ocean co2", default=1)
    c_m0 = Variable("initial mixed-layer carbon","pre- industrial mixed-layer carbon stock", default=900)
    r = Variable ("Revelle (buffer) factor", " add a good description", default=12.5)
    D_T = Variable("Solubility reduction", "Reduction of solubility with temperature", default=0.0423)
    B_0 = Variable("Initial biological pump", "strength of the pre-industrail biologial pump", default=13)
    B_T = Variable("Temperature depandance biological pump","rate to with the biological pump changes wit a rising temperature", default=0.032)
    B_TB = Variable("Biodiv-ediated temperatzre effects on the biological pump", "find good description", default=0.7)
    B_A = Variable ("Biodiv-ediated acidification effects on the biological pump", "find good description", default=0.019)
    w_0 = Variable ("solubility pump rate", "rate od the solubility pump", default=0.1)
    w_T = Variable ("weakening of overturning circulation with cc","find a better description", default=10)
    e = Variable("fossil fule emissions", "human fussil fule emissions", default=20)
    tau = Variable("climate lag", "find a good description", default=4)
    lam = Variable("transit climate sensitivity","find a good description", default=1.8 )
    LUC = Variable("Land-use emissions", "Emissions from land-use", default=1)
    NPP = Variable("Pre-industrial net primary production", "find a good description", default=55)
    response_lag= Variable("response lag",
                           "global mean surface temperature to which global distributions of species are currently best adapted", default=0)
    measurre_biodiv = Variable("measure biodiv", 
                               "a measure for the current state of biodiversity", default=0.9)
    productivity = Variable("productivity", 
                            "biodiversity productivity", default=0.973)
    bio_pump_strength = Variable("biological pump strength", 
                                 "strength of the biological pump", default=13)
    perma_carbon = Variable("permaforst carbon emissions", 
                            "cummulative emissions from permaforst", default=0)
    perma_tenperature = Variable("Permaforst Temperature", "temperature of permaforst", default=0)
    I_CC = Variable("Effect of CC on BD", "find good description", default=0.05)
    I_d = Variable("BD loss from human impacts", "will late be part of metabolism", default=0.1)
    teta = Variable ("exponent in the biodiversity-function relationship","find good description", default=0.26)
    v_max = Variable("maximum response rate", "find good description", default=0.02)
    r_g = Variable("response relaxation rate", "find good description", default=0.025)
    p_T = Variable("permafrost thaw temperature response", "find good description", default=22.5)
    dis =Variable("wvwh", "wnf kw", default=0)
    
    
    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONEENVIRONMENTVARIABLE = master_data_model.Environment.ONEENVIRONMENTVARIABLE

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERENVIROMENTVARIABLE= MODEL_COMPONENT.Environment.ANOTHERENVIROMENTVARIABLE

    # TODO: uncomment and adjust only if you really need other variables:
    # PERSONALENVIROMENTVARIABLE = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:


