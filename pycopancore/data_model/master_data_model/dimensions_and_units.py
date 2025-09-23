"""Master data model for dimensions and units."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from pycopancore.data_model.dimension import Dimension
from pycopancore.data_model.unit import Unit, unity


class DimensionsAndUnits:
    # fundamental physical dimensions and units:

    length = Dimension("length", "1D spatial dimension")
    m = meters = Unit("meters", "meters", symbol="m", dimension=length)
    length.default_unit = km = kilometers = (meters * 1000).named(
        "kilometers", symbol="km"
    )
    decimeters = (meters / 10).named("decimeters", symbol="dm")

    time = Dimension("time", "time")
    time.default_unit = a = yr = years = Unit("years", "years", symbol="yr")
    s = seconds = (years / 31556952).named("seconds", symbol="s")
    minutes = (seconds * 60).named("minutes", symbol="min")
    h = hours = (minutes * 60).named("hours", symbol="h")
    days = (hours * 24).named("days", symbol="d")
    doy = (hours * 24).named("day of the year", symbol="doy")
    weeks = (days * 7).named("weeks")
    months = (years / 12).named("months")

    mass = Dimension(
        "mass",
        "mass (only use for matter changing its type, otherwise use specific mass dimension, e.g. 'carbon')",  # noqa: E501
    )
    mass.default_unit = t = tonnes = Unit(
        "tonnes",
        "metric tonnes (only use for matter changing its type, otherwise use specific mass units, e.g. 'GtC')",  # noqa: E501
        symbol="t",
    )
    Gt = gigatonnes = (tonnes * 1e9).named("gigatonnes", symbol="Gt")
    kg = kilograms = (tonnes * 1e-3).named("kilograms", symbol="kg")
    g = grams = (tonnes * 1e-6).named("grams", symbol="g")

    absolute_temperature = Dimension(
        "absolute temperature", "absolute temperature"
    )
    absolute_temperature.default_unit = K = kelvins = Unit(
        "kelvins", "kelvins (degrees Kelvin)", symbol="K"
    )

    # other base dimensions and units:

    money = monetary_value = Dimension(
        "money or monetary value",
        "inflation-adjusted money or monetary value of goods, services etc.",
    )
    monetary_value.default_unit = dollars = US_dollars_2005 = Unit(
        "dollars", "inflation-adjusted 2005 US dollars", symbol="$"
    )
    # TODO: also provide US_dollars_1992 etc. for conversion

    utility = Dimension(
        "utility",
        "abstract utility, representing an individual's preferences. BEWARE: this may not be considered to be interpersonally comparable!",  # noqa: E501
    )
    utility.default_unit = u = utils = Unit(
        "utils", "utility points", symbol="u"
    )

    carbon = Dimension(
        "carbon",
        "mass of carbon, whether atomic or in some chemical compound",
    )
    carbon.default_unit = tC = tonnes_carbon = Unit(
        "tonnes carbon",
        "tonnes of carbon, whether atomic or in some chemical compound",
        symbol="tC",
    )
    GtC = gigatonnes_carbon = (tonnes_carbon * 1e9).named(
        "gigatonnes carbon", symbol="GtC"
    )
    kgC = kilograms_carbon = (tonnes_carbon * 1e-3).named(
        "kilograms carbon", symbol="kgC"
    )
    gC = grams_carbon = (tonnes_carbon * 1e-6).named(
        "grams carbon", symbol="gC"
    )
    humans = Dimension("humans", "cardinality of a set of human beings")
    humans.default_unit = H = people = persons = Unit(
        "people", "number of human beings", symbol="H"
    )

    # we do NOT treat energy as convertible to mass, so we do NOT say:
    # energy = (mass * velocity**2).named("energy")
    # joules = kilograms * meters**2 / seconds**2
    # but:
    heat = energy = Dimension("energy", "(not convertible to mass velocity²)")
    J = joules = Unit(
        "joules",
        "(not convertible to kg m²/s²)",
        symbol="J",
        dimension=energy,
    )
    energy.default_unit = GJ = gigajoules = (joules * 1e9).named(
        "gigajoules", symbol="GJ"
    )
    # TODO: provide other common units: Btu, kcal., MWh, etc.
    Btu = british_thermal_units = (GJ * 0.10550559e-5).named(
        "British thermal units", symbol="Btu"
    )
    GWh = gigawatt_hours = (GJ * 3600).named("gigawatt_hours", symbol="GWh")
    Gcalth = gigacalories_th = (GJ * 4.184).named(
        "gigacalories (thermochemical)", symbol="Gcalth"
    )

    # derived flow dimensions and units:

    value_flow = (monetary_value / time).named("monetary_value flow")
    carbon_flow = (carbon / time).named("carbon flow")
    human_flow = (humans / time).named("human flow")

    GW = gigawatts = (GWh / h).named("gigawatts", symbol="GW")

    # other derived dimensions and units:

    percent = pct = (unity / 100).named("per cent", symbol="%")

    area = (length**2).named("area", "2D spatial dimension")
    km2 = square_kilometers = (kilometers**2).named(
        "square kilometers", symbol="km²"
    )
    ha = hectares = (meters**2 * 1e4).named("hectares", symbol="ha")
    m2 = square_meters = (meters**2).named("square meters", symbol="m²")

    volume = (length**3).named("volume", "3D spatial dimension")
    litres = (decimeters**3).named("litres", symbol="l")

    velocity = (length / time).named("velocity")
    acceleration = (velocity / time).named("acceleration")

    tC_per_ha = (t / ha).named("tonnes carbon per hectare", symbol="tC/ha")
    kgC_per_m2 = (kgC / m2).named(
        "kilograms carbon per square meter", symbol="kgC/m²"
    )
    gC_per_m2 = (gC / m2).named(
        "grams carbon per square meter", symbol="gC/m²"
    )

    person_hours = (people * hours).named("person hours")
    person_months = (people * months).named("person months")
