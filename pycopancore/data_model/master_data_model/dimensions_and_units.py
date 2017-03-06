from .. import Dimension
from .. import Unit

# fundamental physical dimensions and units:

length = Dimension(name="length", desc="1D spatial dimension")
meters = Unit(name="meters", symbol="m", desc="meters", dimension=length)
length.default_unit = kilometers = \
    (1000 * meters).named("kilometers", symbol="km")

time = Dimension(name="time", desc="time")
time.default_unit = years = Unit(name="years", symbol="a", desc="years")

mass = Dimension(name="mass",
                 desc="mass (only use for matter changing its type, otherwise use specific mass dimension, e.g. 'carbon')")
mass.default_unit = tons = \
    Unit(name="tons", symbol="t",
         desc="tons (only use for matter changing its type, otherwise use specific mass units, e.g. 'GtC')")
gigatons = (1e9 * tons).named("gigatons", symbol="Gt")

absolute_temperature = Dimension(name="absolute temperature",
                                 desc="absolute temperature")
absolute_temperature.default_unit = kelvins = \
    Unit(name="kelvins", symbol="K", desc="kelvins (degrees Kelvin)")


# other base dimensions and units:

# TODO: maybe rename to monetary value:
value = Dimension(name="value",
                  desc="inflation-adjusted monetary value of goods, services etc.")
value.default_unit = dollars = \
    Unit(name="dollars", symbol="$",
         desc="inflation-adjusted 1990 US dollars")

utility = Dimension(name="utility",
                    desc="abstract utility, representing an individual's preferences. BEWARE: this may not be considered to be interpersonally comparable!")
utility.default_unit = utils = \
    Unit(name="utils", symbol="u", desc="utility points")

carbon = Dimension(name="carbon",
                   desc="mass of carbon, whether atomic or in some chemical compound")
carbon.default_unit = tons_carbon = \
    Unit(name="tons carbon", symbol="tC",
         desc="tons of carbon, whether atomic or in some chemical compound")
gigatons_carbon = (1e9 * tons_carbon).named("gigatons carbon", symbol="GtC")

humans = Dimension(name="humans", desc="cardinality of a set of human beings")
humans.default_unit = people = \
    Unit(name="people", symbol="H", desc="number of human beings")

# derived flow dimensions:

value_flow = (value / time).named("value flow")
carbon_flow = (carbon / time).named("carbon flow")
human_flow = (humans / time).named("human flow")

# other derived dimensions and units:

area = (length**2).named("area", desc="2D spatial dimension")
square_kilometers = kilometers**2

volume = (length**3).named("volume", desc="3D spatial dimension")

velocity = (length / time).named("velocity")

acceleration = (velocity / time).named("acceleration")
