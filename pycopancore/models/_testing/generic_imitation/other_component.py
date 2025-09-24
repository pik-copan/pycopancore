from .... import Variable
from .... import master_data_model as D

# INTERFACE:


class ISocialSystem(object):
    is_active = Variable(
        "a boolean variable", "", scale="nominal", datatype=bool
    )


class ICell(object):
    an_ordinal_var = Variable(
        "an ordinal variable",
        "e.g., a Likert scale",
        scale="ordinal",
        datatype=int,
        levels=[1, 2, 3, 4, 5],
    )


class IIndividual(object):
    a_nominal_var = Variable(
        "a nominal (categorical) variable",
        "",
        scale="nominal",
        datatype=str,
        levels=["a", "b", "c"],
    )
    a_dimensional_var = Variable("a dimensional variable", "", unit=D.dollars)
    a_criterion = Variable("a fitness criterion", "e.g. income")


class IModel(object):
    name = "other component"
    description = "only for testing generic_imitation"
    requires = []


class interface:
    SocialSystem = ISocialSystem
    Cell = ICell
    Individual = IIndividual
    Model = IModel


# IMPLEMENTATION:


class SocialSystem(ISocialSystem):
    processes = []


class Cell(ICell):
    processes = []


class Individual(IIndividual):
    processes = []


class Model(IModel):
    entity_types = [SocialSystem, Cell, Individual]
    process_taxa = []
