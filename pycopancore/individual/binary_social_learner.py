# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Binary_Social_Learner is a subclass of 'Individual'. It defines a more specific
instance of Individual such that they can interact due to the ExploitLike
model.
"""

#
#  Imports
#
from abstract_individual import Individual

#
#  Define class MicroAgents
#


class BinarySocialLearner(Individual):
    """
    Binary_Social_Learner is a subclass of 'Individual'. It defines a more
    specific instance of Individual such that they can interact due to
    the ExploitLike model.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 individual_strategy,
                 individual_rationality,
                 stock_fraction,
                 capacity_fraction
                 ):

        """
        Initializes an instance of BinarySocialLearner:
        The objects of BinarySocialLearner define a more specific micro agent
        with parameters that are necessary to interact due to the ExploitLike
        model.

        Parameters
        ----------
        individual_strategy: integer
            Denotes the strategy of each individual (1: sus, 0: unsus)
        individual_rationality: float
            Parameter concerning the social imitation due to rational behaviour
        stock_fraction: float
            Number in between 0 and 1 that gives the fraction of the total
            stock of which the individual is responsible for.
        capacity_fraction: float
            Number in between 0 and 1 that gives the fraction of the total
            capacity each individual is assigned to.
        """

    def __str__(self):
        """
        Returns a string representation of the instance
        """
        return (super(BinarySocialLearner, self).__str__() +
                ('strategy % s, \
                 rationality % s, \
                 stock_fraction % s, \
                 capacity_fraction % s'
                 ) % (
                self.strategy,
                self.rationality,
                self.stock_fraction,
                self.capacity_fraction)
                )

    #
    #  Definitions of further methods
    #

    def set_strategy(self, strategy):
        """
        A function to set the strategy of the SocialBinaryLeaner
        """
        self.strategy = strategy

    def set_rationality(self, rationality):
        """
        A function to set the  rationality of the SocialBinaryLearner
        """
        self.rationality = rationality
