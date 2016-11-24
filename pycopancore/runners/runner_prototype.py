# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is a model module. It only import components of the base mixins
"""

#
#  Imports
#

from pycopancore.private import _AbstractRunner
from pycopancore.process_types import Event, Explicit, Implicit, ODE, Step
from pycopancore.models import base_only

#
# Definition of class _AbstractRunner
#


class RunnerPrototype(_AbstractRunner):
    """
    This is the Runnerprototype. It shall be implemented:
    ODES
    Explicits
    Implicits
    Events
    Steps
    """

    def __init__(self,
                 model,
                 **kwargs):
        """

        Parameters
        ----------
        model
        kwargs
        """
        super(RunnerPrototype, self).__init__(**kwargs)
        self.model = model
        self.processes = (model.individual_processes + model.cell_processes
                          + model.society_processes + model.nature_processes
                          + model.metabolism_processes + model.culture_processes
                          + model.processes)
        self.explicit_processes = []
        self.implicit_processes = []
        self.event_processes = []
        self.step_processes = []
        self.ode_processes = []

        for process in self.processes:
            if isinstance(process, Explicit):
                self.explicit_processes.append(process)
            if isinstance(process, Implicit):
                self.implicit_processes.append(process)
            if isinstance(process, Event):
                self.event_processes.append(process)
            if isinstance(process, ODE):
                self.ode_processes.append(process)
            if isinstance(process, Step):
                self.step_processes.append(process)
            else:
                print('process-type not specidfied')

    def run(self,
            t_0=0,
            t_1=None,
            dt=None,
            output_variables=None
            ):
        """
        This is the run-function, which calls all process-types to
        be solved

        Parameters
        ----------
        t_0 : float
            starting time
        t_1 : float
            end-time
        dt: float
            time resolution
        output_variables : list
            list that includes all variables that shall be returned

        Returns
        -------
        trajectory_dict: dict
            dictionary with time and output variables as keys and list
            with their values over the time integrated
        """

        #
        # First: get initial values from model
        # Second: Call discontinuity_finder to get next discontinuity
        # Third: Calculate Values for timesteps of dt until next
        # discontinuity is met
        # Forth: Save them, repeat until end-time is met
        # Fifth: Return values
        #

    def odeint_prepare(self,
                       values):
        """
        Function to to be passed to odeint.
        Parameters
        ----------
        values

        Returns
        -------
        some_array : array
            Array with all the derivatives to be passed to odeint
        """

        #
        # This shall be the same as odeint_rhs in jobst prototype in the
        # scipy_ODE_only_runner file. I do not yet understand it..
        # What is this offset thing?
        #

    def discontinuitiy_finder(self):
        """
        Function to find and sort the discontinuities in event and
        step type processes
        Returns
        -------
        discontinuity_dict : dict
            Dictionary with times as keys and the associated process as
            entry
        """

        #
        # First: Assemble all non-continuos functions
        # Second: Call their distrinutions to see who is producing the next
        # discontinuity
        # Third: Return discontinuity-dictionary
        #
