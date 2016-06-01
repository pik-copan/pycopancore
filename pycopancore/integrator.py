# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Integrates copan:core model dynamics and organizes model runs.
"""

#
#  Imports
#


#
#  Define class Integrator
#

class Integrator(object):
    """
    Integrates copan:core model dynamics and organizes model runs.

    Parameters
    ----------
    ecosphere : int
        an ecosphere object
    ....

    """

    #
    #  Definitions of internal methods
    #

    def __init__(self, ecosphere, anthroposphere, step_size):
        """
        Initialize an instance of Integrator.

        """
        #  Pseudocode:
        #
        #  Initialize ecosphere
        #  Initialize anthroposphere

        #  Set internal variables
        self.ecosphere = ecosphere
        self.anthroposphere = anthroposphere
        self.step_size = step_size

    #
    #  Definitions of further methods
    #

    def run(self, n_steps, condition=None):
        """
        Integrate model for multiple steps.

        TODO: Time management including stochastic updates in anthroposphere.

        Parameters
        ----------
        n_steps : int
            number of simulation steps to run
        condition : func, optional
            returns true if simulation shall end
        """
        for i in xrange(n_steps):
            #  Integrate ecosphere for one time step
            #  Update Anthroposphere stochastically for acting agent
            pass

    def step(self):
        """
        Integrate model for one single step.
        """
        self.run(n_steps=1)

    def time_management(self):
        """
        Provide time management for model integration.
        """
