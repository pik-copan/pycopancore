"""Culture process taxon mixing class template.

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
from numpy.random import exponential, uniform
from .... import Event
from ...base import interface as B
from .... import master_data_model as D
from . import individual as ID
from . import cell as C
import numpy as np
import networkx as nx

# TODO: uncomment this if need ref. variables such as B.Culture.individuals:
# from ...base import interface as B

# TODO: import those process types you need:
# from .... import Explicit, ODE, Event, Step


class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:
    # TODO: only uncomment when adding custom code!

#     def __init__(self,
#                  # *,  # TODO: uncomment when adding named args behind here
#                  **kwargs):
#         """Initialize the unique instance of Culture."""
#         super().__init__(**kwargs)  # must be the first line
#         # TODO: add custom code here:
#         pass

    # process-related methods:
    # TODO fill these methods with decision tree formulas

    """The following part contains helping stuff"""
    def sigmoid(self, x):
        return 0.5 * (np.tanh(x) + 1)

    """The following part comprises decision-making based on the TPB."""
    # TPB: putting things together, differentiated for 2 farmer AFTs 
    # method

    def update_behaviour(self, t):
        self.last_execution_time = t
        agent_i = self.get_update_agent()
        # behaviour = agent_i.behaviour
        # TODO make sure that aft/behavior here and strategy in Ronjas model
        # align
        aft = agent_i.aft

        # now comes the update
        # identity_value = 0
        tpb = (agent_i.w_attitude[aft] * self.calc_attitude()
               + agent_i.w_norm[aft] * self.calc_social_norm())\
            * agent_i.pbc[aft]

        # if agent_i.aft == 1:
        #     tpb = (agent_i.w_sust_attitude * self.calc_attitude()
        #            + agent_i.w_sust_norm * self.calc_social_norm())\
        #            * sust_pbc
        # else:
        #     tpb = (agent_i.w_trad_attitude * self.calc_attitude()
        #            + agent_i.w_trad_norm * self.calc_social_norm())\
        #            * trad_pbc

        if np.random.random() < tpb:
            agent_i.past_yield = agent_i.get_yield()
            agent_i.past_soil_carbon = agent_i.get_soil_carbon()
            agent_i.past_behaviour = agent_i.behaviour
            agent_i.behaviour = int(not agent_i.behaviour)
            C.landuse_decisions[agent_i] = agent_i.behaviour

        self.set_new_update_time(agent_i)
        # do I want to check for consensus?
        # if self.check_for_consensus():
        #     print('Consensus! time ', t)

    """The attitude part of TPB here involves a mixture of attitude based on
    social learning and obersation of own land"""

    def calc_attitude(self, agent_i):
        return agent_i.w_social_learning[agent_i.aft] * \
                self.calc_attitude_social_learning \
                + agent_i.w_own_land[agent_i.aft] * self.calc_attitude_own_land

    # calculating the input of farmer's own land evaluation to attitude
    # differentiated for 2 farmer types
    def calc_attitude_own_land(self, agent_i):
        # TODO differentiate for 2 AFTs
        # TODO think about to which tate agent compares current state...
        # state before last update or last year?
        attitude_own_soil = self.sigmoid(agent_i.past_soil -
                                         agent_i.get_soil_carbon())
        attitude_own_yield = self.sigmoid(agent_i.past_soil -
                                          agent_i.get_yield())
        return attitude_own_soil, attitude_own_yield

    def list_neighbors(self, agent_i):
        reg_neighbors = []
        conv_neighbors = []
        if self.acquaintance_network.neighbors(agent_i):
            neighbors_i = list(self.acquaintance_network.neighbors(agent_i))
            for neighbor in neighbors_i:
                if neighbor.strategy == 1:
                    reg_neighbors.append(neighbor)
                else:
                    conv_neighbors.append(neighbor)
        return conv_neighbors, reg_neighbors

    def check_neighbors_yield(self, agent_i):
        # sorting agent_i neighbors by their current farming behavior 
        # (regenerative or conventional)
        # note: current behavoor is not necessarily = farmer type
        # calculate average yield for neighbors, reg. and conv.
        # TODO think about finding a nicer way to access list_neighbors outputs
        conv_neighbors = agent_i.list_neighbors()[0]
        reg_neighbors = agent_i.list_neighbors()[1]
        if reg_neighbors:
            yield_reg = sum(n.get_yield() for n in reg_neighbors)\
                / len(reg_neighbors)
        else:
            yield_reg = 0
        # for conventionals
        if conv_neighbors:
            yield_conv = sum(n.get_yield() for n in conv_neighbors)\
                / len(conv_neighbors)
        else:
            yield_conv = 0

        return yield_reg, yield_conv

    def check_neighbors_soil(self, agent_i):
        # sorting agent_i neighbors by their current farming behavior 
        # (regenerative or conventional)
        # note: current behavoor is not necessarily = farmer type
        # TODO is there a way not to repeat this code snippet?
        conv_neighbors = agent_i.list_neighbors()[0]
        reg_neighbors = agent_i.list_neighbors()[1]

        # calculate average yield for neighbors, reg. and conv.
        # calculate average soil_quality for neighbors, reg and conv
        if reg_neighbors: 
            soil_reg = sum(n.get_soil_carbon() for n in reg_neighbors)\
                / len(reg_neighbors)

        else:
            soil_reg = 0
        # for conventionals
        if conv_neighbors:
            soil_conv = sum(n.get_soil_carbon() for n in conv_neighbors)\
                / len(conv_neighbors)
        else:
            soil_conv = 0

        return soil_reg, soil_conv

    # calculating the input of farmer's comparison to neighboring farmers
    # to attitide, differentiated for 2 farmer types
    def calc_attitude_social_learning(self, agent_i):
        # maybe split up method above? or explicitly refer to the valsneeded?
        average_yields = self.check_neighbors_yield(agent_i)
        average_soils = self.check_neighbors_soil(agent_i)
        # important: this is about behaviour (RA / CF, NOT AFT)
        yields_diff, yields_same = average_yields[not agent_i.behavior],\
            average_yields[agent_i.behavior]
        soils_diff, soils_same = average_soils[not agent_i.behavior],\
            average_soils[agent_i.behavior]
        # TODO is agent_i.behavior really getting me to the right return?

        # calc both yield and soil comparison, then weight
        # TODO think about sigmoid instead of heaviside?
        yield_comparison = yields_diff - agent_i.get_yield() *\
            np.heaviside(yields_diff - yields_same, 0)
        soil_comparison = soils_diff - agent_i.get_soil_carbon() *\
            np.heaviside(soils_diff - soils_same, 0)

        return self.sigmoid(agent_i.w_yield[agent_i.aft] * yield_comparison +
                            agent_i.w_soil[agent_i.aft] * soil_comparison)
        # if agent_i.aft == 1:
        #     return self.sigmoid(w_sust_yield*yield_comparison +
        #                         w_sust_soil*soil_comparison)
        # else:
        #     return self.sigmoid(w_trad_yield*yield_comparison +
        #                         w_trad_soil*soil_comparison)

    """The social learning part of TPB here looks at the average behavior,
    not performance, of neighboring agents"""
    # calculating descriptive social norm based on all neighboring farmers
    def calc_social_norm(self, agent_i):
        # TODO check if base model is neede for .neighbors
        social_norm = 0
        if self.acquaintance_network.neighbors(agent_i):
            neighbors = list(self.acquaintance_network.neighbors(agent_i))
            social_norm = sum(n.behaviour for n in neighbors)/len(neighbors)

        if agent_i.behaviour == 1:
            return self.sigmoid(0.5-social_norm)
        else:
            return self.sigmoid(social_norm-0.5)

    def next_landuse_update_time(self, t):
        return t + exponential(1 / self.landuse_update_rate)

    # TODO: this is just EXPLOIT, check if it can be removed completely
    # def update_landuse_style(self, unused_t):
    #    for w in self.worlds:
    #        for i in w.individuals:
    #            if uniform() < self_landuse_update_prob:
    #                # TODO adjust
    #                # i.behaviour = 1 or 0
    #                i.update_landuse()

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
