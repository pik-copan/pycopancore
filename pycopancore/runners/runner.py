"""Returns the trajectory of a setup given as a model object."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
#  Imports
#

from pycopancore.private import _AbstractRunner
from pycopancore import Event, Step
from scipy import integrate
import numpy as np

#
# Definition of class _AbstractRunner
#


class Runner(_AbstractRunner):
    """Runner-class, it owns the run function which calculates trajectories.

    Equations might be of type QDE, explicit, step and event, as stated in the
    process_types package.
    """

    def __init__(self,
                 *,
                 model
                 ):
        """Initiate an Instance of Runner.

        Parameters
        ----------
        model
        kwargs
        """
        super(Runner, self).__init__()
        self.model = model
        self.processes = model.processes
        self.explicit_processes = model.explicit_processes
        self.event_processes = model.event_processes
        self.step_processes = model.step_processes
        self.ode_processes = model.ODE_processes

    def complete_explicits(self, t):
        """Call all explicit functions to complete or update them.

        Parameters
        ----------
        self
        t

        Returns
        -------

        """
        # Iterate through explicit_processes:
        for (p, oc) in self.explicit_processes:
            for e in oc.entities:
                p.specification(e, t)

    def get_derivatives(self, value_array, t):
        """Update explicits, Get derivatives.

        Gets derivatives of all ode-functions and make them suitable for
        the odeint rhs

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
        """Pass this to odeint.

        This function returns all variables in a form to be compatible with
        ODEint from scipy.integrate

        Parameters
        ----------
        self
        t

        Returns
        -------

        """

        for (variable, oc) in self.model.ODE_variables:
            variable.clear_derivatives(entities=oc.entities)

        offset = 0  # this is a counter
        # call all varibles which are in the list ODE_variables which is
        # defined in model_components/base/model:
        for (variable, oc) in self.model.ODE_variables:
            # second counter to count how many entities are using the variable:
            next_offset = offset + len(oc.entities)
            # Write values to variables:
            variable.set_values(entities=oc.entities,
                                values=value_array[offset:next_offset])

            # set up the counter:
            offset = next_offset

            # call methods:
            for (process, oc) in self.ode_processes:
                for entity in oc.entities:
                    process.specification(entity, t)

        derivative_array = np.zeros(offset)

        # Calculation of derivatives:
        offset = 0  # Again, a counter
        for (variable, oc) in self.model.ODE_variables:
            next_offset = offset + len(oc.entities)
            # Get the calculated derivatives and write them to output array:
            derivative_array[offset:next_offset] = variable.get_derivatives(
                entities=oc.entities)

            offset = next_offset

        return derivative_array

    def run(self,
            *,
            t_0=0,
            t_1,
            dt
            ):
        """Run function.

        This is the run function which is a solver and uses all of the above
        functions. It is given a model object and returns a trejectory as
        a dictionary
        Parameters
        ----------
        self
        t
        dt

        Returns
        -------
        trajectory_dict: dict

        """
        # Define time:
        t = t_0

        # First create the dictionary to fill in the trajectory:
        trajectory_dict = {'t': np.zeros([0])}
        for (v, oc) in self.model.variables:
            trajectory_dict[v] = {}

        # Create dictionary to put in the discontinuities:
        next_discontinuities = {}

        # Complete/calculate explicit Functions, 2.2 in runner scheme
        self.complete_explicits(t_0)

        # Fill the dictionary with initial values, 2.3 in runner schmeme:
        for (event, oc) in self.event_processes:
            # print('    event specification:', event.specification)
            # print('    owning class', oc)
            eventtype = event.specification[0]
            rate_or_timfunc = event.specification[1]
            # TODO: Check if the following loop is correct:
            for entity in oc.entities:
                if eventtype == "rate":
                    next_time = np.random.exponential(1. / rate_or_timfunc)
                elif eventtype == "time":
                    next_time = rate_or_timfunc(t)
                else:
                    print("        Invalid specification of the Event: ",
                          event.name,
                          "        In entity:",
                          oc.entity)
                try:
                    next_discontinuities[next_time].append((event, entity))
                except KeyError:
                    next_discontinuities[next_time] = [(event, entity)]

        # Fill next_discontinuities with times of step and performn step if
        # necessary, also 2.3 in runner scheme
        for (step, oc) in self.step_processes:
            next_time_func = step.specification[0]
            method = step.specification[1]
            for entity in oc.entities:
                if next_time_func(entity, t) == t_0:
                    method(entity, t)
                    # calling next_time with function:
                    next_time = next_time_func(entity, t)
                # Same time for all entities? self. necessary?
                else:
                    next_time = next_time_func(entity, t)
                try:
                    next_discontinuities[next_time].append((step, entity))
                except KeyError:
                    next_discontinuities[next_time] = [(step, entity)]

        # Complete/calculate explicit Functions not neccessary, since it is
        # done in get_derivatives

        # Enter while loop
        while t < t_1:
            print('    t is', t)
            # Get next discontinuity to find the next timestep where something
            # happens
            # If there are no discontinuities, the next_discontinuities
            # dict is empty, therefore try is necessary:
            try:
                next_time = min(next_discontinuities.keys())
            except:
                next_time = t_1
            print('    next time is', next_time)
            # Divide time until discontinuity into timesteps of sice dt:
            npoints = np.ceil((next_time - t) / dt) + 1  # resolution
            ts = np.linspace(t, next_time, npoints)

            # Call Odeint if there are ODEs:
            if self.model.ODE_processes:
                # Compose initial value-array:
                offset = 0
                # Find out how many variables we have:
                for (variable, oc) in self.model.ODE_variables:
                    next_offset = offset + len(oc.entities)
                    offset = next_offset
                initial_array_ode = np.zeros(offset)
                offset = 0
                # Fill initial_array_ode with values:
                for (variable, oc) in self.model.ODE_variables:
                    next_offset = offset + len(oc.entities)
                    initial_array_ode[offset:next_offset] = \
                        variable.get_value_list(entities=oc.entities)
                    offset = next_offset

            # In Odeint, call get_derivatives to get the functions, which
            # odeint needs to integrate, step 3.1 in runner scheme, then return
            # the trajectory, 3.2 in runner scheme

                ode_trajectory = integrate.odeint(self.get_derivatives,
                                                  initial_array_ode,
                                                  ts)

            # Take the time steps used in odeint and calculate explicit
            # functions in retrospect, step 3.3 in runner scheme
            # Save them to an arraySave them to the trajectory_dict
            # This is only done if there are explicit processes!

                for i in range(len(ts)):
                    # write values to objects:
                    time = ts[i]
                    ode_values = ode_trajectory[i, :]
                    for (v, oc) in self.model.ODE_variables:
                        entities = oc.entities
                        v.set_values(entities=entities, values=ode_values)
                    # calculate explicits if existent
                    if self.model.explicit_processes:
                        self.complete_explicits(time)
                        # save values of explicits AND all other variables
                        # including t!
                        for (v, oc) in self.model.explicit_variables:
                            entities = oc.entities
                            values = v.get_value_list(entities)
                            for i in range(len(entities)):
                                value = np.array([values[i]])
                                entity = entities[i]
                                try:
                                    trajectory_dict[v][entity] = \
                                        np.concatenate((
                                            trajectory_dict[v][entity], value))
                                except KeyError:
                                    trajectory_dict[v][entity] = value
                    # Same with Event variables:
                    if self.model.event_processes:
                        for (v, oc) in self.model.event_variables:
                            entities = oc.entities
                            values = v.get_value_list(entities)
                            for i in range(len(entities)):
                                value = np.array([values[i]])
                                entity = entities[i]
                                try:
                                    trajectory_dict[v][entity] = \
                                        np.concatenate((
                                            trajectory_dict[v][entity], value))
                                except KeyError:
                                    trajectory_dict[v][entity] = value
                    # Same for step variables:
                    if self.model.step_processes:
                        for (v, oc) in self.model.step_variables:
                            entities = oc.entities
                            values = v.get_value_list(entities)
                            for i in range(len(entities)):
                                value = np.array([values[i]])
                                entity = entities[i]
                                try:
                                    trajectory_dict[v][entity] = \
                                        np.concatenate((
                                            trajectory_dict[v][entity], value))
                                except KeyError:
                                    trajectory_dict[v][entity] = value
            time_np = np.array(ts)
            trajectory_dict['t'] = np.concatenate((trajectory_dict['t'],
                                                   time_np))

            # save odes to trajectory dict
            if self.model.ODE_processes:
                offset = 0
                for (v, oc) in self.model.ODE_variables:
                    # print('variable, oc:', v, oc)
                    next_offset = offset + len(oc.entities)
                    for i in range(len(oc.entities)):
                        entity = oc.entities[i]
                        values = ode_trajectory[:, offset + i]
                        try:
                            trajectory_dict[v][entity] = np.concatenate((
                                trajectory_dict[v][entity], values))
                        except KeyError:
                            trajectory_dict[v][entity] = values
                    offset = next_offset

            # After all that is done, calculate what happens at the
            # discontinuity, step 3.4 in runner scheme
            # Delete the discontinuity from the dictionary and calculate when
            # the next one happens:
            t = next_time
            if next_discontinuities:
                for discontinuity in next_discontinuities.pop(t):
                    # print('        Entering the dicontinuity loop, t=', t)
                    # discontinuity is a tupel with (event/step, entity)
                    entity = discontinuity[1]
                    happening = discontinuity[0]
                    if isinstance(happening, Event):
                        eventtype = happening.specification[0]
                        rate_or_timfunc = happening.specification[1]
                        method = happening.specification[2]
                        # Perform the event:
                        method(entity, t)
                        # Add its next discontinuity:
                        if eventtype == "rate":
                            next_time = t + \
                                        np.random.exponential(1. /
                                                              rate_or_timfunc)
                        elif eventtype == "time":
                            next_time = rate_or_timfunc(t)
                        else:
                            print("Invalid specification of the Event: ",
                                  event.name,
                                  "In entity:",
                                  event.entity)
                        try:
                            next_discontinuities[next_time].append((happening,
                                                                    entity))
                        except KeyError:
                            next_discontinuities[next_time] = [(happening,
                                                                entity)]
                    elif isinstance(happening, Step):
                        method = happening.specification[1]
                        timefunc = happening.specification[0]
                        method(entity, t)
                        next_time = timefunc(entity, t)
                        try:
                            next_discontinuities[next_time].append((happening,
                                                                    entity))
                        except KeyError:
                            next_discontinuities[next_time] = [(happening,
                                                                entity)]

            # Complete state again, 3.5 in runner scheme:
            if self.model.explicit_processes:
                self.complete_explicits(t)

            # Store all information that has been calculated at time t ->
            # iterate through all process variables!
            for (v, oc) in self.model.process_variables:
                entities = oc.entities
                values = v.get_value_list(entities)
                for i in range(len(entities)):
                    entity = entities[i]
                    value = np.array([values[i]])
                    try:
                        trajectory_dict[v][entity] = np.concatenate((
                            trajectory_dict[v][entity], value))
                    except KeyError:
                        trajectory_dict[v][entity] = value

            t_np = np.array([t])
            trajectory_dict['t'] = np.concatenate((trajectory_dict['t'], t_np))

        # Store all information that has not been changed during calculations:
        for (v, oc) in self.model.variables:
            if (v, oc) not in self.model.process_variables:
                entities = oc.entities
                values = v.get_value_list(entities)
                for i in range(len(entities)):
                    entity = entities[i]
                    value = np.array([values[i]])
                    try:
                        trajectory_dict[v][entity] = np.concatenate((
                            trajectory_dict[v][entity], value))
                    except KeyError:
                        trajectory_dict[v][entity] = value

        return trajectory_dict
