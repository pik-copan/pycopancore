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
from pycopancore.model_components.base import interface as B
from pycopancore import Event, Explicit
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
                 random_rewire=0.05,
                 farm_size=None,
                 gross_income=None,
                 **kwargs):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)  # must be the first line
        self.profession = profession
        self.nutrition_need = nutrition_need
        self.migration_threshold = migration_threshold
        self.migration_steepness = migration_steepness
        self.second_degree_rewire_prob = second_degree_rewire_prob
        self.outspokenness = outspokenness
        self.random_rewire = random_rewire
        self.gross_income = gross_income
        self.farm_size = farm_size

        self._subjective_income_rank = None
        self.liquidity = liquidity
        self.nutrition = nutrition

        if self.profession == 'farmer':
            assert self.cell.characteristic == 'farmland'
        if self.profession == 'townsman':
            assert self.cell.characteristic == 'city'

    def calc_farm_size(self):
        """Get the farm size."""
        # Check, if not already been calculated:
        if self.farm_size is None:
            # If townsman, individual has no farm:
            if self.social_system.municipality_like is True:
                self.farm_size = 0
            # If farmer, distribute farm size:
            if self.social_system.municipality_like is False:
                # Let social_system distribute farm size
                self.farm_size = self.social_system.calc_gross_income_or_farmsize()
        # return self.farm_size

    def calc_gross_income(self):
        """Get the gross income."""
        # Check if not already been calculated:
        if self.gross_income is None:
            # Check if farmer or townsman:
            if self.social_system.municipality_like is True:
                # Let social_system distribute income:
                self.gross_income = self.social_system.calc_gross_income_or_farmsize()
            # If not townsman, income = 0
            if self.social_system.municipality_like is False:
                self.gross_income = 0
        # return self.gross_income

    # process-related methods:
    def social_update_timer(self, t):
        """Calculate when a social update takes place"""
        return t + np.random.exponential(self.outspokenness)
    # outspokenness = 1 means in average once a year, 0.1 = 10 times a year,
    # 10 means once every 10 years in average.

    def social_update(self, unused_t):
        """Do social update.

        Either migration or de- and re-friending takes place. 
        In case of a fully connected network only migration takes place.
        """
        # First: determine if fully connected network:
        if self.culture.fully_connected_network:
            # Network is fully connected:
            chosen_one = random.choice(self.culture.acquaintance_network.nodes())
            if self.decide_migration(chosen_one):
                # in case of preferential migration, checks are done
                if self.preferential_migration:
                    self.preferential_migrate(chosen_one.cell)
                else:
                    # Migrate
                    self.migrate(chosen_one.cell)
        else:  # Not fully connected:
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
                if (chosen_profession == self.profession
                        and random.random() <= self.random_rewire):
                    # Noise: Rewire to a random individual
                    random_guy = random.choice(tuple(self.world.individuals))
                    if (random_guy not in self.acquaintances):
                        # Add edge:
                        self.culture.acquaintance_network.add_edge(self, random_guy)
                        # remove old edge:
                        self.culture.acquaintance_network.remove_edge(self,
                                                                      chosen_one)

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
        # print('delta util', delta_utility)
        # Tanh function:
        tanh = 0.5 * (1 + math.tanh(delta_utility / 2))
        if random.random() <= tanh:
            # Migrate if enough liquidity
            if self.liquidity > neighbour.social_system.migration_cost:
                # Next line is causing liquidities to drop below 0 if the
                # social_system update takes place:
                # self.liquidity -= neighbour.social_system.migration_cost
                return True
            else:
                # Not enough money to migrate
                return False
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

    def preferential_migrate(self, cell):
        """Calls migragte in case of preferential migration."""
        # 3 cases: city-city, farmland-farmland, city-farmland/vice versa
        # first, check city-city
        if (self.cell.social_system.municipality_like and
                cell.social_system.municipality_like):
            if random.random() < 0.2:  # need of  number that makes sense
                self.migrate(cell)
        # second, check farmlad farmland
        elif (not self.cell.social_system.municipality_like and
              not cell.social_system.municipality_like):
            if random.random() < 0.2:  # need of  number that makes sense
                self.migrate(cell)
        # third: check city-farmland/farmland-city
        else:
            # check if neighbours
            if ((cell.location[0] ^ self.cell.location[0])
                    ^ (cell.location[1] ^ self.cell.location[1])):
                # cells are neighbouring
                if random.random() < 1:
                        self.migrate(cell)

    def migrate(self, cell):
        """Migrate to Cell.

        Parameters
        ----------
        cell: exodus.cell
            cell to migrate to.
        """
        # Change cell and social_system (done in base.individual):
        self.cell = cell
        # Change Profession:
        if cell.social_system.municipality_like is False:
            self.profession = 'farmer'
        elif cell.social_system.municipality_like is True:
            self.profession = 'townsman'
        else:
            raise TypeError('Neither Municipality nor County!')
        # Set Values to None, so they can be recalculated:
        self.farm_size = None
        self.gross_income = None
        self.calc_gross_income()
        self.calc_farm_size()

    def calculate_harvest(self, unused_t):
        """Calculate the harvest of an Individual."""
        self.harvest = self.farm_size * self.cell.average_precipitation * 1000000

    def calculate_utility(self, unused_t):
        """Calculate utility if an Individual."""
        try:
            self.utility = math.sqrt(
                self.liquidity * self.nutrition
                / self.social_system.average_liquidity / 1240)
            # 1240 m^3 is the annual need, maybe need to incorporate it
        # The folloeing should not happen but do so on the cluster:
        except ValueError:
            print('liquidity could not be calculated! Setting it to 0')
            print(self.liquidity, self.nutrition,
                  self.social_system.average_liquidity)
            self.utility = 0
        except TypeError:
            print('liquidity could not be calculated! Setting it to 0')
            print(self.liquidity, self.nutrition,
                  self.social_system.average_liquidity)
            self.utility = 0

    def calculate_sri(self, unused_t):
        """Calculate subjective income rank of individual"""
        sri = stats.lognorm.cdf(self.liquidity,
                                s=self.social_system.liquidity_sigma,
                                loc=self.social_system.liquidity_loc,
                                scale=self.social_system.liquidity_median)
        self.subjective_income_rank = sri

    processes = [
        Event("social update",
              [B.Individual.social_system,
               # B.Individual.culture.acquaintance_network TOO BIG TO SAVE!
               I.Individual.farm_size,
               I.Individual.gross_income,
               I.Individual.liquidity
               ],
              ["time", social_update_timer, social_update]),
        Explicit("Calculate harvest",
                 [I.Individual.harvest],
                 calculate_harvest),
        Explicit("Calculate Utility",
                 [I.Individual.utility],
                 calculate_utility),
        #Explicit("Calculate Subjective Income Rank",
        #         [I.Individual.subjective_income_rank],
        #         calculate_sri)
    ]  # TODO: instantiate and list process objects here
