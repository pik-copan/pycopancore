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
import numpy as np

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

        # 1. output_variables, out_functions
        # 2. Find next times/discontinuities of all events into dict
        # 3. Find next times/discontinuities of all steps and perform them
        # if they have attribute 'immediate' -> implement into abstract_step
        # 4. Enter while-loop until t_1
        # 4.a Calculate all explicit funtions up to the next discontinuity
        # 4.b Take next discontinuity and integrate all ODEs in intervals dt
        # 4.c Perform the thing that caused the next discontinuity
        #   - if step of type 'immediate', calculate it
        #   - if step of type '?' then do whatever is needed
        #   - if event, do the event
        #   - calculate the thing's next discontinuity and add it to the dict
        # 4.d Do until t_1 is met, write out_vars into trajectory dict
        # 5. Return out_vars from trajectory dict

    def odeint_rhs(self,
                   value_array,
                   t):
        """
        Function to to be passed to odeint as callable.
        Parameters
        ----------
        value_array : array
            input array with values to be computed
        t : float
            time

        Returns
        -------
        rhs_array : array
            Array with all the derivatives to be passed to odeint
        """

        #
        # This shall be the same as odeint_rhs in jobst prototype in the
        # scipy_ODE_only_runner file. I do not yet understand it..
        # What is this offset thing?
        #

        offset = 0  # this is a counter
        for variable in self.model.ODE_variables:
            # call all varibles which are in the list ODE_variables which is
            # defined in model_components/base/model
            next_offset = offset + len(variable.entities)
            # second counter to count how many entities are using the variable
            variable.set_values(entities=variable.entities,
                                values=value_array[offset:next_offset])
            # Write values to variables
            variable.clear_derivatives(entities=variable.entities)
            # Delete old derivatives if there are any
            offset = next_offset
            # set up the counter
        rhs_array = np.zeros(offset)
        # create the output-array as a flat array to give to odeint

        #
        # Now calculate the derivatives by calling the functions in the
        # model-components
        #

        for process in self.processes:
            for entity in self.model.ODE_variables.entities:
                process.specification(entity, t)

        # Now Return the derivatives just calculate
        offset = 0  # Again, a counter
        for variable in self.model.ODE_variables:
            next_offset = offset + len(variable.entities)
            rhs_array[offset:next_offset] = variable.get_derivatives(
                entities=variable.entities)
            # Get the calculated derivatives and write them to output array
            offset = next_offset

        return rhs_array
