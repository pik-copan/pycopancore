from pycopancore.data_model import Variable

# Population, demographics:

population = Variable("human population", "",
                      IAMC="Population",
                      CETS="SP.POP",
                      is_extensive=True, lower_bound=0)

# Note: when using the following, include
# Implicit(population == sum(population_by_age))
population_by_age = Variable("human population by age",
                             "(in years from 0 to 99+)",
                             IAMC="Population",
                             CETS="SP.POP",
                             is_extensive=True, lower_bound=0,
                             array_shape=(100,))  # 1d-array

# Resource extraction and waste:


# Economy:

