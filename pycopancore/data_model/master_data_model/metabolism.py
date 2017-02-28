from pycopancore.data_model import Variable, CFVariable, CETSVariable

# Population, demographics:
human_population = CETSVariable(ref="???")
# in base: Implicit(human_population == sum(human_population_by_age))
human_population_by_age = Variable("human population by age",
                                   "bla", array_shape=(100,))  # 1d-array

# Economy:
