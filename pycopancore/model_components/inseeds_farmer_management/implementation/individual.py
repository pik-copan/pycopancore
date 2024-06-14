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
    def random(progressive_probability=0.5):
        return np.random.choice(
            [AFT.progressive_minded, AFT.conservative_minded],
            p=[progressive_probability, 1-progressive_probability]
        )

class Individual (I.Individual, base.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:
    def __init__(self,
                 *,
                 config=None,
                 **kwargs):

        """Initialize an instance of Individual."""
        super().__init__(**kwargs)  # must be the first line

        self.aft = AFT.random(config.progressive_probability)
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
        # self.strategy_switch_duration = randint(
        #     self.strategy_switch_duration/2,
        #     self.strategy_switch_duration/2 + self.strategy_switch_duration
        # )

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
        """Return the average crop yield of the cell."""
        if (self.cell.output.pft_harvestc.values.mean() == 0):
            return 1e-3
        else:
            return self.cell.output.pft_harvestc.values.mean()

    @property
    def cell_soilc(self):
        """Return the average soil carbon of the cell."""
        if (self.cell.output.soilc_agr_layer.values[0].item() == 0):
            return 1e-3
        else:
            return self.cell.output.soilc_agr_layer.values[0].item()

    @property
    def cell_avg_hdate(self):
        """Return the average harvest date of the cell."""
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
        """Calculate the attitude of the farmer following the TPB"""
        return self.weight_social_learning * self.attitude_social_learning \
            + self.weight_own_land * prod(self.attitude_own_land)

    @property
    def attitude_own_land(self):
        """Calculate the attitude of the farmer based on their own land"""
        # compare own soil and yield to previous values
        attitude_own_soil = sigmoid(
            self.soilc_previous / self.soilc  - 1
        )
        attitude_own_yield = sigmoid(
            self.cropyield_previous / self.cropyield  - 1
        )

        return attitude_own_soil, attitude_own_yield

    @property
    def attitude_social_learning(self):
        """Calculate the attitude of the farmer through social learning based
        on the comparison to neighbours using a different strategy"""

        # split variables (crop yield, soilc) status of neighbours into groups
        #   of different strategies applied and average them
        average_cropyields = self.split_neighbourhood_status("cropyield")
        average_soilcs = self.split_neighbourhood_status("soilc")

        # select the average of the neighbours that are using a different
        #   strategy
        yields_diff, yields_same = average_cropyields[not self.behaviour],\
            average_cropyields[self.behaviour]
        soils_diff, soils_same = average_soilcs[not self.behaviour],\
            average_soilcs[self.behaviour]

        # calculate the difference between the own status and the average
        #   status of the neighbours
        yield_comparison = yields_diff / self.cropyield - 1
        soil_comparison = soils_diff / self.soilc - 1

        # calculate the attitude of social learning based on the comparison
        return sigmoid(self.weight_yield * yield_comparison +
                       self.weight_soil * soil_comparison)

    @property
    def social_norm(self):
        """Calculate the social norm of the farmer based on the majority
        behaviour of the neighbours"""
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

    def split_neighbourhood(self, attribute):
        """split the neighbourhood of farmers after a defined boolean attribute
        (e.g. behaviour)
        """
        # init split into two neighbourhood lists
        first_nb = []
        second_nb = []

        # split the neighbourhood into two groups based on the attribute
        #   of the neighbours 
        for neighbour in self.neighbourhood:
            if getattr(neighbour, attribute) == 1:
                first_nb.append(neighbour)
            else:
                second_nb.append(neighbour)
        return first_nb, second_nb

    def split_neighbourhood_status(self, variable):
        """split the neighbourhood of farmers after a defined attribute
        (behaviour) and calculate the average of each group
        """
        # split the neighbourhood into two groups based on the behaviour
        first_nb, second_nb = self.split_neighbourhood("behaviour")

        # calculate the average of the variable for first group
        if first_nb:
            first_var = sum(getattr(n, variable) for n in first_nb)\
                / len(first_nb)
        # if there are no neighbours of the same strategy, set the average
        #   to 0
        else:
            first_var = 0

        # calculate the average of the variable for second group
        if second_nb:
            second_var = sum(getattr(n, variable) for n in second_nb)\
                / len(second_nb)
        # if there are no neighbours of the same strategy, set the average
        #   to 0
        else:
            second_var = 0

        return first_var, second_var

    def update_behaviour(self, t):
        """Update the behaviour of the farmer based on the TPB"""
        # update the average harvest date of the cell
        self.avg_hdate = self.cell_avg_hdate

        # running average over strategy_switch_duration years to avoid rapid 
        #    switching by weather fluctuations
        self.cropyield = (1-1/(self.strategy_switch_duration/2)) * self.cropyield\
            + 1/(self.strategy_switch_duration/2) * self.cell_cropyield
        self.soilc = (1-1/(self.strategy_switch_duration/2)) * self.soilc\
            + 1/(self.strategy_switch_duration/2) * self.cell_soilc

        # If strategy switch time is down to 0 calculate TPB-based strategy
        # switch probability value
        if self.strategy_switch_time <= 0:
            tpb = (self.weight_attitude * self.attitude
                + self.weight_norm * self.social_norm) * self.pbc

            if tpb > 0.5:
                # switch strategy
                self.behaviour = int(not self.behaviour)

                # decrease pbc after strategy switch
                self.pbc = max(self.pbc - 0.25, 0.5)

                # set back counter for strategy switch
                self.strategy_switch_time = randint(
                    round(self.strategy_switch_duration/2),
                    round(self.strategy_switch_duration/2 + self.strategy_switch_duration)
                )

            # increase pbc if tpb is near 0.5 to learn from own experience
            elif tpb <= 0.5 and tpb > 0.4:
                self.pbc = min(self.pbc + 0.25/self.strategy_switch_duration, 1)

            # set the values of the farmers attributes to the LPJmL variables
            self.set_lpjml_var(map_attribute="behaviour")


        else:
            # decrease the counter for strategy switch time each year
            self.strategy_switch_time -= 1

        # freeze the current soilc and cropyield values that were used for
        #   the decision making in the next evaluation after
        #   self.strategy_switch_duration
        self.cropyield_previous = self.cropyield
        self.soilc_previous = self.soilc

    def set_lpjml_var(self, map_attribute):
        """Set the mapped variables from the farmers to the LPJmL input"""
        lpjml_var = self.coupling_map[map_attribute]

        if not isinstance(lpjml_var, list):
            lpjml_var = [lpjml_var]

        for single_var in lpjml_var:
            self.cell.input[single_var][:] = getattr(self, map_attribute)

    def init_coupled_vars(self):
        """Initialize the mapped variables from the LPJmL output to the farmers
        """
        for attribute, lpjml_var in self.coupling_map.items():
            if not isinstance(lpjml_var, list):
                lpjml_var = [lpjml_var]

            for single_var in lpjml_var:
                if len(self.cell.input[single_var].values.flatten()) > 1:
                    continue
                setattr(
                    self, attribute, self.cell.input[single_var].item()
                )

    processes = []


def sigmoid(x):
    """The following part contains helping stuff"""
    return 0.5 * (np.tanh(x) + 1)
