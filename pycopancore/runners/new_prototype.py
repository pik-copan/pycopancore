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
        self.processes = (model.processes)
        self.explicit_processes = model.explicit_processes
        self.event_processes = model.event_processes
        self.step_processes = model.step_processes
        self.ode_processes = model.ODE_processes

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
        for (p, oc) in self.explicit_processes:
            print('process = ', p)
            print('owning class =', oc)
            for entity in oc.entities:
                p.specification(entity, t)

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
        # Call complete explicit functions, 3.1.2 in runner scheme
        self.complete_explicits(self)

        # Call ode_rhs, 3.1.3 in runner scheme
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

        # Calculation of derivatives:
        offset = 0  # Again, a counter
        for variable in self.model.ODE_variables:
            next_offset = offset + len(variable.entities)
            # Get the calculated derivatives and write them to output array:
            derivative_array[offset:next_offset] = variable.get_derivatives(
                entities=variable.entities)

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

        # Complete/calculate explicit Functions, 2.2 in runner scheme
        self.complete_explicits(t_0)

        # Fill the dictionary with initial values, 2.3 in runner schmeme:
        for (event, oc) in self.event_processes:
            print('event specification:', event.specification)
            print('owning class', oc)
            eventtype = event.specification[0]
            rate_or_timfunc = event.specification[1]
            # TODO: Check if the following loop is correct:
            for entity in oc.entities:
                if eventtype == "rate":
                    next_time = np.random.exponential(1. / rate_or_timfunc)
                elif eventtype == "time":
                    next_time = rate_or_timfunc(t)
                else:
                    print("Invalid specification of the Event: ",
                          event.name,
                          "In entity:",
                          oc.entity)
                try:
                    next_discontinuities[next_time].append((event, entity))
                except KeyError:
                    next_discontinuities[next_time] = [(event, entity)]

        # Fill next_discontinuities with times of step and performn step if
        # necessary, also 2.3 in runner scheme
        for step in self.step_processes:
            first_execution_time = step.specification[0]
            next_time_func = step.specification[1]
            method = step.specification[2]
            if first_execution_time == t_0:
                # loop over all variables of corresponding step
                for variable in self.model.step_variables:
                    for entity in variable.entities:
                        # also possible: variable.entities ?
                        method(entity, t)
                        # calling next_time with function:
                        next_time = next_time_func(entity, t)
                # Same time for all entities? self. necessary?
            else:
                next_time = first_execution_time
            try:
                next_discontinuities[next_time].append(step)
            except KeyError:
                next_discontinuities[next_time] = [step]

        # Complete/calculate explicit Functions not neccessary, since it is
        # done in get_derivatives

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
            # Fill initial_array_ode with values:
            for variable in self.model.ODE_variables:
                next_offset = offset + len(variable.entities)
                initial_array_ode[offset:next_offset] = \
                    variable.get_value_list(entities=variable.entities)
                offset = next_offset

            # In Odeint, call Oget_derivatives to get the functions, which
            # odeint needs to integrate, step 3.1 in runner scheme, then return
            # the trajectory, 3.2 in runenr scheme
            ode_trajectory = integrate.odeint(self.get_derivatives,
                                              initial_array_ode,
                                              ts)

            # Now: Take the time steps used in odeint and calculate explicit
            # functions in retrospect, step 3.3 in runner scheme

            # TODO: Save ODE- and Explicit variables to trajectory, empty
            # TODO  buffer matrizes

            # After all that is done, calculate what happens at the
            # discontinuity, step 3.4 in runner scheme
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
                            method(entity, t)
                    next_time = timefunc(self, t)
                    try:
                        next_discontinuities[next_time].append(discontinuity)
                    except KeyError:
                        next_discontinuities[next_time] = [discontinuity]
                # On this ident-level the discontinuity_out variables have to be
                # written into a discontinuity_trajectory_matrix

            # Complete state again, 3.5 in runner scheme
            self.complete_explicits(t)

            # Store all information that has been calculated at time t ->
            # iterate thrugh all variables!


        return trajectory_dict
