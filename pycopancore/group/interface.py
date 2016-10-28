from sympy import Symbol


## OUTPUT VARIABLES (sympy Symbols representing model variables):

# global variables (representing scalars):


# societal variables (representing vectors indexed by society id):

#domestic_surface_area_ = Symbol("domestic surface area")
domestic_population_ = Symbol("domestic population")
#domestic_capital_ = Symbol("domestic capital")

#domestic_fossil_use_ = Symbol("domestic fossil use")
domestic_biomass_use_ = Symbol("domestic biomass use")
#domestic_renewable_use_ = Symbol("domestic (other) renewable use")

domestic_production_ = Symbol("domestic production")

wellbeing_ = Symbol("wellbeing")

domestic_carbon_emissions_ = Symbol("domestic carbon (-equivalent) emissions")
domestic_local_pollution_ = Symbol("domestic local pollution")

# individual variables (vectors indexed by individual id):

# none!

# cellular variables (vectors indexed by cell id):

cell_in_territory_ = Symbol("is cell in territory") # (sparse) matrix indicating membership
cell_biomass_use_ = Symbol("cellular biomass use")

# other variables (more complex data types):

migration_ = Symbol("migration") # matrix indexed by society
foreign_holdings_ = Symbol("foreign holdings") # ditto
