"""Test file for the simple extraction module."""

from pycopancore.model_components.simple_extraction.implementation import (
    Individual as I)
import pycopancore.models.exploit as M
import numpy as np

culture = M.Culture()
world = M.World(culture=culture)

random1 = np.random.random()
random2 = np.random.random()
random3 = np.random.random()

cell = M.Cell(stock=random1, capacity=1, growth_rate=random2, world=world)
individual = M.Individual(strategy=random3, imitation_tendency=0,
                          rewiring_prob=0.5,
                          cell=cell)


def test_get_harvest():
    """Check the get_harvest_rate function.
    
    The effort shall be 0.5 * self.cell.growth_rate * 
    (3 - 2 * self.strategy) = 
    0.5 * random2 * (3 - 2 * random3)
    Then the harvest is  random1 * 0.5 * random2 * (3 - 2 * random3)
    """
    solution = random1 * 0.5 * random2 * (3 - 2 * random3)
    assert I.get_harvest_rate(individual) == solution
