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
from pycopancore import Event, Explicit, Implicit, ODE, Step
from scipy import integrate
import numpy as np

#
# Definition of class _AbstractRunner
#


class RunnerPrototype2(_AbstractRunner):
    """
    This is the Runnerprototype. It shall be implemented:
    ODES
    Explicits
    Events
    Steps
    """

    def __init__(self,
                 *,
                 model
                 ):
        """

        Parameters
        ----------
        model
        kwargs
        """
        super(RunnerPrototype2, self).__init__()
        self.model = model
        self.processes = (model.individual_processes + model.cell_processes
                          + model.society_processes + model.nature_processes
                          + model.metabolism_processes + model.culture_processes
                          #  + model.processes
                          # model.processes already includes all of the above!
                          # See comment in model.configure
                          )
        self.explicit_processes = []
        self.event_processes = []
        self.step_processes = []
        self.ode_processes = []

        for process in self.processes:
            if isinstance(process, Explicit):
                self.explicit_processes.append(process)
            elif isinstance(process, Event):
                self.event_processes.append(process)
            elif isinstance(process, ODE):
                self.ode_processes.append(process)
            elif isinstance(process, Step):
                self.step_processes.append(process)
            else:
                print('process-type of', process, 'not specified')
                print(process.__class__.__name__)
                print(object.__str__(process))

    def complete_explicits(self, t):
        """
        A function to call all explicit functions to complete or update them

        Parameters
        ----------
        self
        t

        Returns
        -------

        """

        # Iterate through explicit_processes:
        for variable in self.model.explicit_variables:
            for process in self.explicit_processes:
                for entity in variable.entities:
                    process.specification(entity)
                # TODO: Do we need to return this as a matrix or is it included
                # TODO in the output of the odeint?

    def get_derivatives(self, value_array, t):
        """
        A function to get the derivatives of all ode-functions and make them
        suitable for the odeint rhs

        Parameters
        ----------
        self
        t

        Returns
        -------

        """
        # Call complete explicit functions
        self.complete_explicits(self)

        # Call ode_rhs
        return_array = self.ode_rhs(value_array, t)

        # return derivative_array
        return return_array

    def ode_rhs(self, value_array, t):
        """
        A function to pass to odeint

        Parameters
        ----------
        self
        t

        Returns
        -------

        """
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

            # call methods:
            for process in self.ode_processes:
                for entity in variable.entities:
                    process.specification(entity, t)

        derivative_array = np.zeros(offset)

        # Calculation of derivatives
        offset = 0  # Again, a counter
        for variable in self.model.ODE_variables:
            next_offset = offset + len(variable.entities)
            derivative_array[offset:next_offset] = variable.get_derivatives(
                entities=variable.entities)
            # Get the calculated derivatives and write them to output array
            offset = next_offset

        return derivative_array

    def run(self,
            t_0=0,
            t_1=None,
            dt=None
            ):
        """
        The run function

        Parameters
        ----------
        self
        t
        dt

        Returns
        -------

        """

        # Define time:
        t = t_0

        # First create the dictionary to fill in the trajectory:
        trajectory_dict = {}

        # Create dictionary to put in the discontinuities:
        next_discontinuities = {}

        # Fill the dictionary with initial values:
        for variable in self.model.event_variables:
            for event in self.event_processes:
                print('event specification:', event.specification)
                eventtype = event.specification[0]
                rate_or_timfunc = event.specification[1]
                # TODO: Check if the following loop is correct:
                for entity in variable.entities:
                    if eventtype == "rate":
                        next_time = np.random.exponential(1. / rate_or_timfunc)
                    elif eventtype == "time":
                        next_time = rate_or_timfunc(t)
                    else:
                        print("Invalid specification of the Event: ",
                              event.name,
                              "In entity:",
                              variable.entity)
                    try:
                        next_discontinuities[next_time].append((event, entity))
                    except KeyError:
                        next_discontinuities[next_time] = [(event, entity)]

        step_variables = []
        for step in self.step_processes:
            first_execution_time = step.specification[0]
            next_time_func = step.specification[1]
            method = step.specification[2]
            if first_execution_time == t_0:
                # loop over all variables of corresponding step
                for variable in self.model.step_variables:
                    for entity in variable.entities:
                        # also possible: variable.entities ?
                        method(entity)
                next_time = next_time_func(t)  # calling next_time with function
                # Same time for all entities? self. necessary?
            else:
                next_time = first_execution_time
            try:
                next_discontinuities[next_time].append(step)
            except KeyError:
                next_discontinuities[next_time] = [step]

        # Complete/calculate explicit Functions
        self.complete_explicits(t_0)

        # Enter while loop
        while t < t_1:

            # Get next discontinuity to find the next timestep where something
            # happens
            next_time = min(next_discontinuities.keys())

            # Divide time until discontinuity into timesteps of sice dt:
            npoints = np.ceil((next_time - t) / dt) + 1  # resolution
            ts = np.linspace(t, next_time, npoints)

            # Call Odeint:

            # Compose initial value-array:
            offset = 0
            # Find out how many variables we have:
            for variable in self.model.ODE_variables:
                next_offset = offset + len(variable.entities)
                offset = next_offset
            initial_array_ode = np.zeros(offset)
            offset = 0
            # Fill initial_array_ode with values
            for variable in self.model.ODE_variables:
                next_offset = offset + len(variable.entities)
                initial_array_ode[offset:next_offset] = \
                    variable.get_value_list(entities=variable.entities)
                offset = next_offset

            # In Odeint, call ODE-rhs to get the functions, which odeint needs
            # to integrate
            ode_trajectory = integrate.odeint(self.get_derivatives,
                                              initial_array_ode,
                                              ts)

            # Now: How do we calculate explicit functions during the odeint?
            # This must be done in get_derivatives, which needs to call
            # ode_rhs and complete_explicits!

            # Save ODE- and Explicit (?) variables to trajectory

            # After all that is done, calculate what happens at the
            # discontinuity
            # Delete the discontinuity from the dictionary and calculate when
            # the next one happens:
            t = next_time
            # I know this is sloppy, just had no other idea to do it:
            disco = next_discontinuities[t]
            for discontinuity in next_discontinuities.pop(t):
                if isinstance(discontinuity, Event):
                    entity = disco[1]
                    print('event specification:', event.specification)
                    eventtype = event.specification[0]
                    rate_or_timfunc = event.specification[1]
                    method = discontinuity.specification[2]
                    # Perform the event:
                    discontinuity_out = method(t)
                    # Add its next discontinuity:
                    if eventtype == "rate":
                        next_time = np.random.exponential(1. / rate_or_timfunc)
                    elif eventtype == "time":
                        next_time = rate_or_timfunc(t)
                    else:
                        print("Invalid specification of the Event: ",
                              event.name,
                              "In entity:",
                              event.entity)
                    try:
                        next_discontinuities[next_time].append((discontinuity,
                                                                entity))
                    except KeyError:
                        next_discontinuities[next_time] = [(discontinuity,
                                                            entity)]
                elif isinstance(discontinuity, Step):
                    method = discontinuity.specification[2]
                    timefunc = discontinuity.specification[1]
                    for variable in self.model.step_variables:
                        for entity in variable.entities:
                            # also possible: variable.entities ?
                            method(entity)
                    next_time = timefunc(self, t)
                    try:
                        next_discontinuities[next_time].append(discontinuity)
                    except KeyError:
                        next_discontinuities[next_time] = [discontinuity]
                # On this ident-level the discontinuity_out variables have to be
                # written into a discontinuity_trajectory_matrix

            # Store information that has been calculated in the trajectory_dict
            # It consists of the event/step information just calculated and the
            # information calculated by integrating and by doing explicit funcs

        return trajectory_dict
