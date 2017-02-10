from pycopancore import Variable, CFVariable, CETSVariable

# Population, demographics:
human_population = CETSVariable(ref="???")
# in base: Implicit(human_population == sum(human_population_by_age))
human_population_by_age = VariableArray(dim=1) # 1d-array

# Economy:

