import numpy as np

from .... import base  # all models must use the base component
from ....model_components import config
from ....model_components import generic_imitation as imi
from . import other_component as other

config.generic_imitation = {
    "variables": [
        base.interface.Culture.social_systems.is_active,
        base.interface.Culture.social_systems.cells.an_ordinal_var,
        base.interface.Culture.individuals.a_nominal_var,
        base.interface.Culture.individuals.a_dimensional_var,
    ]
}


class World(base.World):
    pass


class SocialSystem(other.SocialSystem, base.SocialSystem):
    pass


class Cell(other.Cell, base.Cell):

    def imi_p_imitate_ord(self, own_trait=None, other_trait=None):
        return 1.0 if np.abs(other_trait[0] - own_trait[0]) <= 2 else 0.0


class Individual(other.Individual, base.Individual):

    def imi_evaluate_pair(self, other=None):
        return other.a_criterion


class Culture(imi.Culture, base.Culture):
    imi.Culture.imi_traits.default = {
        "bool": (other.SocialSystem.is_active,),
        "ord": (other.Cell.an_ordinal_var,),
        "pair": (
            other.Individual.a_nominal_var,
            other.Individual.a_dimensional_var,
        ),
    }


class Model(other.Model, imi.Model, base.Model):
    name = "Simple test of generic_imitation component"
    description = "uses only one other component"
    entity_types = [World, SocialSystem, Cell, Individual]
    process_taxa = [Culture]
