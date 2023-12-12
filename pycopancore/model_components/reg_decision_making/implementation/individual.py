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
import numpy as np

from math import prod
from enum import Enum
from random import sample, randint

from pycopancore.process_types import Step
from pycopancore.model_components.base import interface as B
import pycopancore.model_components.base as base

from .. import interface as I


class AFT(Enum):
    """Available Inputs"""
    progressive_minded: int = 0
    conservative_minded: int = 1

    @staticmethod
    def random():
        return sample(list(AFT), 1)[0]


class Individual (I.Individual, base.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    # aufgeführt: alle allgemeinen parameter, und AFT-spezifische parameter
    # für den "traditionalist" type
    def __init__(self,
                 *,
                 aft=AFT.random(),
                 config=None,
                 **kwargs):

        """Initialize an instance of Individual."""
        super().__init__(**kwargs)  # must be the first line

        self.aft = aft
        self.coupling_map = config.coupling_map.to_dict()
        self.__dict__.update(getattr(config.aftpar, self.aft.name).to_dict())

        self.init_coupled_vars()

        # average harvest date of the cell is used as a proxy for the order
        # of the agents making decisions in time through the year
        self.avg_hdate = self.cell_avg_hdate

        # soilc is the last "measured" soilc value of the farmer whereas the
        #   cell_soilc value is the actual status of soilc of the cell
        self.soilc = self.cell_soilc
        self.soilc_previous = self.soilc

        # Same applies for cropyield (as for soilc)
        self.cropyield = self.cell_cropyield
        self.cropyield_previous = self.cropyield
        # Maximal soilc and cropyield might be used in the future to assess
        #   soil potential
        # self.max_soilc = self.soilc
        # self.max_cropyield = self.cropyield

        # Randomize switch time at beginning of simulation to avoid
        #   synchronization of agents
        self.strategy_switch_time = randint(0, self.strategy_switch_duration)

    def init_neighbourhood(self):
        """Initialize the neighbourhood of the agent."""
        self.neighbourhood = [
            neighbour for cell_neighbours in self.cell.neighbourhood
            if len(cell_neighbours.individuals) > 0
            for neighbour in cell_neighbours.individuals
        ]

    @property
    def cell_cropyield(self):
        return self.cell.output.pft_harvestc.values.mean()

    @property
    def cell_soilc(self):
        return self.cell.output.soilc_agr_layer.values[:2].sum()

    @property
    def cell_avg_hdate(self):
        crop_idx = [
            i for i, item in enumerate(self.cell.output.hdate.band.values)  # noqa
            if any(x in item for x in self.cell.world.lpjml.config.cftmap)
        ]
        if np.sum(self.cell.output.cftfrac.isel(band=crop_idx).values) == 0:
            return 365
        else:
            return np.average(
                self.cell.output.hdate,
                weights=self.cell.output.cftfrac.isel(band=crop_idx)
            )

    @property
    def attitude(self):
        return self.weight_social_learning \
            * self.attitude_social_learning \
            + self.weight_own_land * self.attitude_own_land

    # calculating the input of farmer's own land evaluation to attitude
    # differentiated for 2 farmer types
    @property
    def attitude_own_land(self):
        # TODO differentiate for 2 AFTs
        # TODO think about to which tate agent compares current state...
        # state before last update or last year?
        # See definition for soilc and cell_soilc in init
        comparison_own_soil = self.soilc_previous / self.soilc  - 1
        # attitude_own_soil = sigmoid(self.soilc_previous / self.soilc  - 1)
        # See definition for cropyield and cell_cropyield in init
        # TODO check if using the same sigmoid really works for soil and yield
        # parameter ranges / units
        comparison_own_yield = self.cropyield_previous / self.cropyield  - 1 # noqa
        # attitude_own_yield = sigmoid(self.cropyield_previous / self.cropyield  - 1) # noqa
        # return attitude_own_soil, attitude_own_yield
        comparison_own_land = self.weight_yield * comparison_own_yield + \
                            self.weight_soil * comparison_own_soil
        if self.behaviour == 1:
            return np.heaviside(0.5-comparison_own_land, 0)
        else:
            return np.heaviside(comparison_own_land-0.5, 0)
        # if self.behaviour == 1:
        #     return np.heaviside(0.5-comparison_own_soil, 0), np.heaviside(0.5-comparison_own_yield, 0)
        # else:
        #     return np.heaviside(comparison_own_soil-0.5, 0), np.heaviside(comparison_own_yield-0.5, 0)

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
        # yield_comparison = yields_diff - self.cell_cropyield *\
        #     np.heaviside(yields_diff - yields_same, 0)
        # soil_comparison = soils_diff - self.cell_soilc *\
        #     np.heaviside(soils_diff - soils_same, 0)
        
        if yields_diff == 0:
            yield_comparison = 0
        else:
            yield_comparison = yields_diff / self.cropyield - 1
    
        if soils_diff == 0:
            soil_comparison = 0
        else:
            soil_comparison = soils_diff / self.soilc - 1

        # TODO make seperate yield and soil comparisons, if comparing yields
        # a number > 0 the inclination to switch grows. normalize these differences
        # found in comparison in some ways to make sure the difference in units
        # from yield and soil is reflected (not done currently, exploit legacy)
        # and then combine these 2 inclinations according to the weights
        # (sust. aft will give more importance to soil-based inclination). 
        # Last, derive an inclination to switch based both on soil and yield-
        # based switching inclinations

        # TODO was anderes machen ;) heaviside....
        # return sigmoid(self.weight_yield * yield_comparison +
        #                self.weight_soil * soil_comparison)
        comparison_social = self.weight_yield * yield_comparison + \
                            self.weight_soil * soil_comparison
        if self.behaviour == 1:
            return np.heaviside(0.5-comparison_social, 0)
        else:
            return np.heaviside(comparison_social-0.5, 0)

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
        #TODO heaviside function has default threshold of 0. sbouldn't it be 0.5 instead of 0? If there
        if self.behaviour == 1:
            return np.heaviside(0.5-social_norm, 0)
        else:
            return np.heaviside(social_norm-0.5, 0)

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
        # TODO think about a nicer way to access list_neighbours outputs
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
        self.avg_hdate = self.cell_avg_hdate
        # running average over strategy_switch_duration years to avoid rapid 
        #    switching by weather fluctuations
        self.cropyield = (1-1/self.strategy_switch_duration) * self.cropyield\
            + 1/self.strategy_switch_duration * self.cell_cropyield
        self.soilc = (1-1/self.strategy_switch_duration) * self.soilc\
            + 1/self.strategy_switch_duration * self.cell_soilc
        # make the execution of this here, or maybe even better somewhere
        # else, (where?) conditional on the strategy_switch_time, to not
        # do the whol decision making evaluation if the farmers are not
        # switching anyways, but still save info about soil and yield somewhere

        tpb = (self.weight_attitude * self.attitude
               + self.weight_norm * self.social_norm) # * self.pbc


        if tpb > 0.5:
            self.behaviour = int(not self.behaviour)
            # self.set_lpjml_var(map_attribute="behaviour")
            # freeze the current soilc and cropyield values that were used for
            #   the decision making in the next evaluation after
            #   self.strategy_switch_duration

        self.set_lpjml_var(map_attribute="behaviour")
        # freeze the current soilc and cropyield values that were used for
        #   the decision making in the next evaluation after
        #   self.strategy_switch_duration
        self.cropyield_previous = self.cropyield
        self.soilc_previous = self.soilc

        # set back counter for strategy switch
        self.strategy_switch_time = 0



    def set_lpjml_var(self, map_attribute):

        lpjml_var = self.coupling_map[map_attribute]

        if not isinstance(lpjml_var, list):
            lpjml_var = [lpjml_var]

        for single_var in lpjml_var:
            self.cell.input[single_var][:] = getattr(self, map_attribute)

    def init_coupled_vars(self):
        for attribute, lpjml_var in self.coupling_map.items():
            if not isinstance(lpjml_var, list):
                lpjml_var = [lpjml_var]

            for single_var in lpjml_var:
                if len(self.cell.input[single_var].values.flatten()) > 1:
                    continue
                    # setattr(
                    #     self, attribute, self.cell.input[single_var].mean()
                    # )
                setattr(
                    self, attribute, self.cell.input[single_var].item()
                )

    processes = []


def sigmoid(x):
    """The following part contains helping stuff"""
    return 0.5 * (np.tanh(x) + 1)

def heaviside_norm(x):
    if x < 0.5:
        return 0
    if x == 0.5:
        return 0.5
    if x > 0.5:
        return 1
