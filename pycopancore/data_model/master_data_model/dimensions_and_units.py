from .. import Dimension
from .. import Unit

# fundamental physical dimensions and units:

length = Dimension("length", "1D spatial dimension")
meters = Unit("meters", "meters", symbol="m", dimension=length)
length.default_unit = kilometers = \
    (meters * 1000).named("kilometers", symbol="km")

time = Dimension("time", "time")
time.default_unit = years = Unit("years", "years", symbol="a")
seconds = (years / 31556952).named("seconds")

mass = Dimension("mass",
                 "mass (only use for matter changing its type, otherwise use specific mass dimension, e.g. 'carbon')")
mass.default_unit = tonnes = \
    Unit("tonnes",
         "metric tonnes (only use for matter changing its type, otherwise use specific mass units, e.g. 'GtC')",
         symbol="t")
gigatonnes = (tonnes * 1e9).named("gigatonnes", symbol="Gt")
kilograms = (tonnes * 1e-3).named("kilograms", symbol="kg")

absolute_temperature = Dimension("absolute temperature",
                                 "absolute temperature")
absolute_temperature.default_unit = kelvins = \
    Unit("kelvins", "kelvins (degrees Kelvin)", symbol="K")


# other base dimensions and units:

# TODO: maybe rename to monetary value:
value = Dimension("value",
                  "inflation-adjusted monetary value of goods, services etc.")
value.default_unit = dollars = US_dollars_2005 = \
    Unit("dollars",
         "inflation-adjusted 2005 US dollars", symbol="$")
# TODO: also provide US_dollars_1992 etc. for conversion

utility = Dimension("utility",
                    "abstract utility, representing an individual's preferences. BEWARE: this may not be considered to be interpersonally comparable!")
utility.default_unit = utils = \
    Unit("utils", "utility points", symbol="u")

carbon = Dimension("carbon",
                   "mass of carbon, whether atomic or in some chemical compound")
carbon.default_unit = tonnes_carbon = \
    Unit("tonnes carbon",
         "tonnes of carbon, whether atomic or in some chemical compound",
         symbol="tC")
gigatonnes_carbon = (tonnes_carbon * 1e9).named("gigatonnes carbon",
                                                symbol="GtC")

humans = Dimension("humans", "cardinality of a set of human beings")
humans.default_unit = people = \
    Unit("people", "number of human beings", symbol="H")

# derived flow dimensions:

value_flow = (value / time).named("value flow")
carbon_flow = (carbon / time).named("carbon flow")
human_flow = (humans / time).named("human flow")

# other derived dimensions and units:

area = (length**2).named("area", "2D spatial dimension")
square_kilometers = kilometers**2

volume = (length**3).named("volume", "3D spatial dimension")

velocity = (length / time).named("velocity")

acceleration = (velocity / time).named("acceleration")

energy = (mass * velocity**2).named("energy")
joules = kilograms * meters**2 / seconds**2
energy.default_unit = gigajoules = \
    (joules * 1e9).named("gigajoules", symbol="GJ")
