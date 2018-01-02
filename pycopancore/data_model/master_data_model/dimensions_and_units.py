"""Master data model for dimensions and units."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import Dimension
from .. import Unit


class DimensionsAndUnits:
    
    # fundamental physical dimensions and units:
    
    length = Dimension("length", "1D spatial dimension")
    m = meters = Unit("meters", "meters", symbol="m", dimension=length)
    length.default_unit = km = kilometers = \
        (meters * 1000).named("kilometers", symbol="km")
    
    time = Dimension("time", "time")
    time.default_unit = a = yr = years = Unit("years", "years", symbol="a")
    s = seconds = (years / 31556952).named("seconds")
    minutes = (seconds * 60).named("minutes", symbol="min")
    h = hours = (minutes * 60).named("hours", symbol="h")
    
    mass = Dimension("mass",
                     "mass (only use for matter changing its type, otherwise use specific mass dimension, e.g. 'carbon')")
    mass.default_unit = t = tonnes = \
        Unit("tonnes",
             "metric tonnes (only use for matter changing its type, otherwise use specific mass units, e.g. 'GtC')",
             symbol="t")
    Gt = gigatonnes = (tonnes * 1e9).named("gigatonnes", symbol="Gt")
    kg = kilograms = (tonnes * 1e-3).named("kilograms", symbol="kg")
    
    absolute_temperature = Dimension("absolute temperature",
                                     "absolute temperature")
    absolute_temperature.default_unit = K = kelvins = \
        Unit("kelvins", "kelvins (degrees Kelvin)", symbol="K")
    
    
    # other base dimensions and units:
    
    # TODO: maybe rename to monetary monetary_value:
    monetary_value = \
        Dimension("monetary_value",
                  "inflation-adjusted monetary monetary_value of goods, services etc.")
    monetary_value.default_unit = dollars = US_dollars_2005 = \
        Unit("dollars",
             "inflation-adjusted 2005 US dollars", symbol="$")
    # TODO: also provide US_dollars_1992 etc. for conversion
    
    utility = Dimension("utility",
                        "abstract utility, representing an individual's preferences. BEWARE: this may not be considered to be interpersonally comparable!")
    utility.default_unit = u = utils = \
        Unit("utils", "utility points", symbol="u")
    
    carbon = Dimension("carbon",
                       "mass of carbon, whether atomic or in some chemical compound")
    carbon.default_unit = tC = tonnes_carbon = \
        Unit("tonnes carbon",
             "tonnes of carbon, whether atomic or in some chemical compound",
             symbol="tC")
    GtC = gigatonnes_carbon = (tonnes_carbon * 1e9).named("gigatonnes carbon",
                                                          symbol="GtC")
    
    humans = Dimension("humans", "cardinality of a set of human beings")
    humans.default_unit = H = people = \
        Unit("people", "number of human beings", symbol="H")
    
    # we do NOT treat energy as convertible to mass, so we do NOT say:
    #energy = (mass * velocity**2).named("energy")
    #joules = kilograms * meters**2 / seconds**2
    # but:
    energy = Dimension("energy", "(not convertible to mass velocity²)")
    J = joules = Unit("joules", "(not convertible to kg m²/s²)",
                      symbol="J", dimension=energy)
    energy.default_unit = GJ = gigajoules = \
        (joules * 1e9).named("gigajoules", symbol="GJ")
    # TODO: provide other common units: Btu, kcal., MWh, etc.
    Btu = british_thermal_units = (GJ * 0.10550559e-5
                                   ).named("British thermal units", symbol="Btu")
    GWh = gigawatt_hours = (GJ * 3600
                            ).named("gigawatt_hours", symbol="GWh")
    Gcalth = gigacalories_th = (GJ * 4.184
                                ).named("gigacalories (thermochemical)", 
                                        symbol="Gcalth")
    
    # derived flow dimensions:
    
    value_flow = (monetary_value / time).named("monetary_value flow")
    carbon_flow = (carbon / time).named("carbon flow")
    human_flow = (humans / time).named("human flow")
    
    GW = gigawatts = (GWh / h).named("gigawatts", symbol="GW")
    
    # other derived dimensions and units:
    
    area = (length**2).named("area", "2D spatial dimension")
    square_kilometers = kilometers**2
    
    volume = (length**3).named("volume", "3D spatial dimension")
    
    velocity = (length / time).named("velocity")
    
    acceleration = (velocity / time).named("acceleration")
