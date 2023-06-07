"""Individual entity type class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I
import numpy as np
from itertools import chain

from pycopancore.process_types.event import Event
from pycopancore.model_components.base import interface as B


class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    # aufgeführt: alle allgemeinen parameter, und AFT-spezifische parameter
    # für den "traditionalist" type
    def __init__(self,
                 *,  # TODO: how to assign AFT to individual?
                 aft=1,
                 behaviour=0,
                 past_behaviour=0,
                 attitude=0,
                 subjective_norm=0,  # TODO maybe adapt this name or check in culture
                 pbc=0,
                 input_name="with_tillage",


                 # TODO implement weights in a way that makes sure they add up to 1
                 w_trad_attitude=1/2,
                 w_trad_yield=2/3,
                 w_trad_soil=1/3,
                 w_trad_norm=1/2,
                 trad_pbc=1/2,
                 w_trad_social_learning=1/2,
                 w_sust_social_learning=1/2,
                 w_trad_own_land=1/2,
                 w_sust_own_land=1/2,
                 w_sust_attitude=2/3,
                 w_sust_yield=1/3,
                 w_sust_soil=2/3,
                 w_sust_norm=1/3,
                 sust_pbc=1/2,
                 # how to bring diff pbc vals to AFTs? 
                 # in all other cases, weighting was necessary because one had
                 # 2 values (i.e., soil and yield), hw to do this now as it
                 # is just a parameter to multiply?
                 **kwargs):

        """Initialize an instance of Individual."""
        super().__init__(**kwargs)  # must be the first line
        self.neighbourhood = [cell_neighbour.individuals[0]
                              for cell_neighbour in self.cell.neighbourhood]
        self.aft = aft
        self.behaviour = behaviour
        self.past_behaviour = past_behaviour
        self.attitude = attitude
        self.subjective_norm = subjective_norm
        self.pbc = pbc

        self.input_name = input_name
        # trad and sust aft
        self.w_social_learning = [w_trad_social_learning,
                                  w_sust_social_learning]
        self.w_own_land = [w_trad_own_land, w_sust_own_land]
        self.w_attitude = [w_trad_attitude, w_sust_attitude]
        self.w_yield = [w_trad_yield, w_sust_yield]
        self.w_soil = [w_trad_soil, w_sust_soil]
        self.w_norm = [w_trad_norm, w_sust_norm]
        self.pbc = [trad_pbc, sust_pbc]

        self.soilc = self.cell_soilc
        self.max_soilc = self.soilc
        self.cropyield = self.cell_cropyield
        self.max_cropyield = self.cropyield

    @property
    def cell_cropyield(self):
        # harvest to be implemented (currently only pft_harvest - too large!)
        return self.cell.output.harvest.item()

    @property
    def cell_soilc(self):
        return self.cell.output.soilc.item()

    @property
    def attitude(self):
        return self.w_social_learning * \
                self.attitude_social_learning \
                + self.w_own_land * self.attitude_own_land

    # calculating the input of farmer's own land evaluation to attitude
    # differentiated for 2 farmer types
    @property
    def attitude_own_land(self):
        # TODO differentiate for 2 AFTs
        # TODO think about to which tate agent compares current state...
        # state before last update or last year?
        attitude_own_soil = sigmoid(self.past_soil -
                                    self.get_soil_carbon())
        attitude_own_yield = sigmoid(self.past_soil -
                                     self.get_yield())
        return attitude_own_soil, attitude_own_yield

    # calculating the input of farmer's comparison to neighbouring farmers
    # to attitide, differentiated for 2 farmer types
    @property
    def attitude_social_learning(self):
        # maybe split up method above? or explicitly refer to the valsneeded?
        average_cropyields = self.split_neighbourhood_status("cropyield")
        average_soilcs = self.split_neighbourhood_status("soilc")
        # important: this is about behaviour (RA / CF, NOT AFT)
        yields_diff, yields_same = average_cropyields[not self.behaviour],\
            average_cropyields[self.behaviour]
        soils_diff, soils_same = average_soilcs[not self.behaviour],\
            average_soilcs[self.behaviour]
        # TODO is agent_i.behaviour really getting me to the right return?

        # calc both yield and soil comparison, then weight
        # TODO think about sigmoid instead of heaviside?
        yield_comparison = yields_diff - self.get_yield() *\
            np.heaviside(yields_diff - yields_same, 0)
        soil_comparison = soils_diff - self.get_soil_carbon() *\
            np.heaviside(soils_diff - soils_same, 0)

        return sigmoid(self.w_yield * yield_comparison +
                       self.w_soil * soil_comparison)

    """The social learning part of TPB here looks at the average behaviour,
    not performance, of neighbouring agents"""
    @property
    # calculating descriptive social norm based on all neighbouring farmers
    def social_norm(self):
        # TODO check if base model is neede for .neighbours
        social_norm = 0
        if self.neighbourhood:
            social_norm = (
                sum(n.behaviour for n in self.neighbourhood) /
                len(self.neighbourhood)
            )
        if self.behaviour == 1:
            return sigmoid(0.5-social_norm)
        else:
            return sigmoid(social_norm-0.5)

    # TODO: how to do this for the two AFTs?
    @property
    def random_behaviour(self):
        """compute a random farming behaviour of individual"""
        return np.random.rand()

    def split_neighbourhood(self, attribute):
        first_nb = []  # regeneratively managed
        second_nb = []  # conventionally managed
        for neighbour in self.neighbourhood:
            if getattr(neighbour, attribute) == 1:
                first_nb.append(neighbour)
            else:
                second_nb.append(neighbour)
        return first_nb, second_nb

    def split_neighbourhood_status(self, variable):
        # sorting agent_i neighbours by their current farming behaviour 
        # (regenerative or conventional)
        # note: current behavoor is not necessarily = farmer type
        # calculate average yield for neighbours, reg. and conv.
        # TODO think about finding a nicer way to access list_neighbours outputs
        first_nb, second_nb = self.split_neighbourhood("behaviour")
        if first_nb:
            first_var = sum(getattr(n, variable) for n in first_nb)\
                / len(first_nb)
        else:
            first_var = 0
        # for conventionals
        if second_nb:
            second_var = sum(getattr(n, variable) for n in second_nb)\
                / len(second_nb)
        else:
            second_var = 0

        return first_var, second_var

    def update_behaviour(self, t):
        self.last_execution_time = t
        # TODO ? where does self come from in my model? nowhere...
        # behaviour = self.behaviour
        # TODO make sure that aft/behaviour here and strategy in Ronjas model
        # align

        # now comes the update
        # identity_value = 0
        tpb = (self.w_attitude * self.attitude
               + self.w_norm * self.calc_social_norm())\
            * self.pbc

        if np.random.random() < tpb:
            self.cropyield = self.cell_cropyield
            # self.max_crop_yield = max(self.max_crop_yield, self.cropyield)
            self.soilc = self.cell_soilc
            # self.max_soilc = max(self.max_soilc, self.soilc)
            self.behaviour = int(not self.behaviour)
            self.set_cell_input(self.behaviour)

        self.set_new_update_time(self)
        # do I want to check for consensus?
        # if self.check_for_consensus():
        #     print('Consensus! time ', t)

    def set_cell_input(self, value):
        self.cell.input[self.input_name] = value

    # TODO: define landuse_update_rate
    def next_landuse_update_time(self, t):
        return t + np.random.exponential(1 / self.landuse_update_rate)


# TODO adjust process to update_behaviour (TPB)
    processes = [
        Event("update landuse style",
                [I.Culture.acquaintance_network,
                 B.Culture.worlds.individuals.behaviour,
                 B.Culture.worlds.individuals.update_time],
                ["time",
                 next_landuse_update_time,
                 update_behaviour])
    ]  # TODO: instantiate and list process objects here


def sigmoid(x):
    """The following part contains helping stuff"""
    return 0.5 * (np.tanh(x) + 1)
