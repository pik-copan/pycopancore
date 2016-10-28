from sympy import Symbol


## OUTPUT VARIABLES (sympy Symbols representing model variables):

# global variables (representing scalars):

    temperature_ = Symbol("temperature")
    atmospheric_carbon_ = Symbol("atmospheric carbon")
    maritime_carbon_ = Symbol("maritime carbon")

# societal variables (representing vectors indexed by society id):

    # none!

# individual variables (vectors indexed by individual id):

    # none!

# cellular variables (vectors indexed by cell id):

    renewable_stock_ = Symbol("renewable stock")

# other variables (more complex data types):

    common_border_network_ = Symbol("common border network")
