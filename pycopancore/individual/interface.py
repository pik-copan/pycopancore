from sympy import Symbol


## OUTPUT VARIABLES (sympy Symbols representing model variables):

# global variables (representing scalars):

global_carbon_tax_ = Symbol("global carbon tax")
global_carbon_cap_ = Symbol("global carbon cap")

# societal variables (representing vectors indexed by society id):

#domestic_carbon_tax_ = Symbol("domestic carbon tax")
#domestic_carbon_cap_ = Symbol("domestic carbon cap")
domestic_harvesting_policy_ = Symbol("domestic harvesting policy (none 0 or restrictive 1)")

# individual variables (vectors indexed by individual id):

individual_in_cell_ = Symbol("is individual in cell") # (sparse) matrix indicating residence
individual_in_society_ = Symbol("is individual in society") # (sparse) matrix indicating membership
#fossil_supply_acceptance_ = Symbol("fossil-energy based supply acceptance")
#fossil_job_acceptance_ = Symbol("fossil-energy related job acceptance")
individual_harvesting_effort_level_ = Symbol("individual's harvesting effort level (low 0 or high 1)")
social_network_ = Symbol("social network") # e.g. an igraph object
# cellular variables (vectors indexed by cell id):

# none!

# other variables (more complex data types):

acquaintance_network_ = Symbol("acquaintance network") # nodes are individuals
interaction_network_ = Symbol("interaction network") # nodes are individuals
diplomatic_network_ = Symbol("diplomatic network") # nodes are societies

