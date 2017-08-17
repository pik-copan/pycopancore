"""Individual entity type class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
from pycopancore.model_components.base import interface as B
from pycopancore import Event
import math
import random
import numpy as np
from scipy import stats


class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 profession=None,
                 nutrition_need=1240,
                 liquidity=None,
                 nutrition=None,
                 migration_threshold=0.7,
                 migration_steepness=5,
                 second_degree_rewire_prob=0.3,
                 outspokenness=None,
                 **kwargs):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)  # must be the first line
        self.profession = profession
        self.nutrition_need = nutrition_need
        self.migration_threshold = migration_threshold
        self.migration_steepness = migration_steepness
        self.second_degree_rewire_prob = second_degree_rewire_prob
        self.outspokenness = outspokenness

        self._subjective_income_rank = None
        self._farm_size = None
        self._gross_income = None
        self.liquidity = liquidity
        self.nutrition = nutrition

        # At last, check for validity of all variables that have been
        # initialized and given a value:

        # Following method is defined in abstract_entity_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()

        if self.profession == 'farmer':
            assert self.cell.characteristic == 'farmland'
        if self.profession == 'townsman':
            assert self.cell.characteristic == 'city'

    @property
    def harvest(self):
        """Get the amount of water a farmer is harvesting"""
        # Return harvest in unit cubic meters per year. Since Farm size is in
        # square kilometers, a factor of 1000*1000 is necessary:
        return self.farm_size * self.cell.average_precipitation * 1000000

    @property
    def utility(self):
        """Get the Cobb-Douglas utility of an individual"""
        return math.sqrt(self.subjective_income_rank * self.nutrition / 1240)
        # TODO: Add parameter to compensate for frequency of market clearing!
        # 1240 m^3 is the annual need

    @property
    def farm_size(self):
        """Get the farm size."""
        # Check, if not already been calculated:
        if self._farm_size is None:
            # If townsman, individual has no farm:
            if self.society.municipality_like is True:
                self._farm_size = 0
            # If farmer, distribute farm size:
            if self.society.municipality_like is False:
                # Let society distribute farm size
                self._farm_size = self.society.gross_income_or_farmsize
        return self._farm_size

    @farm_size.setter
    def farm_size(self, value):
        """Set farm size."""
        self._farm_size = value

    @property
    def gross_income(self):
        """Get the gross income."""
        # Check if not already been calculated:
        if self._gross_income is None:
            # Check if farmer or townsman:
            if self.society.municipality_like is True:
                # Let society distribute income:
                self._gross_income = self.society.gross_income_or_farmsize
            # If not townsman, income = 0
            if self.society.municipality_like is False:
                self._gross_income = 0
        return self._gross_income

    @gross_income.setter
    def gross_income(self, value):
        """Set gross income"""
        self._gross_income = value

    @property
    def subjective_income_rank(self):
        """Get subjective income rank of individual."""
        # Calculate place in liquidity cdf:
        sri = stats.lognorm.cdf(self.liquidity,
                                s=self.society.liquidity_sigma,
                                loc=self.society.liquidity_loc,
                                scale=self.society.liquidity_median)
        self._subjective_income_rank = sri
        return self._subjective_income_rank

    # process-related methods:
    def social_update_timer(t):
        """Calculate when a social update takes place"""
        return t + np.random.exponential(1)
    # TODO: this should be dependent on self.outspokenness. How do I do this?
    # In this case: t + np.random.exponential(self.outspokenness)

    def social_update(self, unused_t):
        """Do social update.

        Either migration or de- and re-friending takes place"""
        # Chose Acquaintance, if existent:
        if self.acquaintances:
            chosen_one = random.choice(self.acquaintances)
            # Get the Chosen One's Profession:
            chosen_profession = chosen_one.profession
            # Check, whether same profession, therefore define
            # if migration or rewiring takes place or nothing
            if chosen_profession != self.profession:
                # Compare utility and decide if migration takes place:
                if self.decide_migration(chosen_one):
                    # Migrate
                    self.migrate(chosen_one.cell)
                else:
                    self.rewire(chosen_one)

    def decide_migration(self, neighbour):
        """Decide, if rewire or migration takes place.

        Parameters
        ----------
        neighbour: exodus.individual
            Object of type individual that has different profession than the
            self object.

        Returns
        -------
        bool:
            True if migration takes place
        """
        # Difference in utility:
        delta_utility = neighbour.utility - self.utility
        print('delta util', delta_utility)
        # Sigmoidal function, normalized so that sigmoid(1) = 1:
        sigmoid = 1 / (1 + math.exp(- self.migration_steepness * (
            delta_utility - self.migration_threshold))) * (1 + math.exp(
                - self.migration_steepness * (1 - self.migration_threshold)))
        if random.random() <= sigmoid:
            # Migrate
            return True
        else:
            # Rewire
            return False

    def rewire(self, neighbour):
        """Do rewiring.

        Detaches from neighbour and rewires to a neighbour of degree n.
        Parameters
        ----------
        neighbour: exodus.individual
            neighbour from which to detach
        """
        # Remove edge:
        self.culture.acquaintance_network.remove_edge(self, neighbour)
        # Chose another random neighbour
        # Check if individuals has acquaintances:
        if not self.acquaintances:
            # If so, connect to random one in model:
            random_one = random.choice(tuple(self.world.individuals))
            self.culture.acquaintance_network.add_edge(self, random_one)
        random_neighbour = random.choice(self.acquaintances)
        third_degree_neighbors = []
        break_cond = False
        # Iterate through second degree neighbours of random neighbour:
        for n in random_neighbour.acquaintances:
            # Attach with second_degree_rewire_prob, if not already connected
            # or if not just detached:
            if (random.random() < self.second_degree_rewire_prob
                    and n != neighbour
                    and n not in self.acquaintances):
                self.culture.acquaintance_network.add_edge(self, n)
                break_cond = True
                break
            # If rewiring did not take place, add his neighbours to third
            # degree neighbour list:
            if (n != neighbour
                    and n not in self.acquaintances):
                for nn in n.acquaintances:
                    third_degree_neighbors.append(nn)
        # Iterate through 3 degree neighbours, if ne neighbour was not found:
        if break_cond is False:
            for n in third_degree_neighbors:
                # Attach with second_degree_rewire_prob^2, if not already
                # connected or if not just detached:
                if (random.random() < (self.second_degree_rewire_prob**2)
                        and n != neighbour
                        and n not in self.acquaintances):
                    self.culture.acquaintance_network.add_edge(self, n)
                    break_cond = True
                    break
        # if nobody has connected yet, chose any random individual:
        if break_cond is False:
            # tuple is necessary since self.world.individuals is a set,
            # therefore random.choice alone does not work!
            random_guy = random.choice(tuple(self.world.individuals))
            if (random_guy != neighbour
                    and random_guy not in self.acquaintances):
                self.culture.acquaintance_network.add_edge(self, random_guy)
            else:
                print('this is very unlikely, nobody has been found, '
                      'individual loses a connection.')

    def migrate(self, cell):
        """Migrate to Cell.

        Parameters
        ----------
        cell: exodus.cell
            cell to migrate to.
        """
        # Change cell and society (done in base.individual):
        self.cell = cell
        # Change Profession:
        if cell.society.municipality_like is False:
            self.profession = 'farmer'
        elif cell.society.municipality_like is True:
            self.profession = 'townsman'
        else:
            raise TypeError('Neither Municipality nor County!')
        # Set Values to None, so they can be recalculated:
        self._subjective_income_rank = None
        self._farm_size = None
        self._gross_income = None
        # TODO: Change farmland/income of everybody else too?

    processes = [
        Event("social update",
              [B.Individual.society, B.Culture.acquaintance_network],
              ["time", social_update_timer, social_update])
    ]  # TODO: instantiate and list process objects here
