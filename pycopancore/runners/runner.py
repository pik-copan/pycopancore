"""Returns the trajectory of a setup given as a model object."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license


# TODO: rename to ScipyODEintRunner

from ..private import _AbstractRunner
from .. import Event, Step

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
                 model,  # TODO: allow this to be given without name!
                 termination_calls=False
                 ):
        """Initiate an Instance of Runner.

        Parameters
        ----------
        model
        termination_calls : list
            List of lists of callables and instances on which they are to be
            called to determine if the runner should terminate in special
            cases prior to the time limit.
        kwargs
        """
        super(Runner, self).__init__()
        self.model = model
        self.processes = model.processes
        self.explicit_processes = model.explicit_processes
        self.event_processes = model.event_processes
        self.step_processes = model.step_processes
        self.ode_processes = model.ODE_processes
        self.trajectory_dict = {}
        self.termination_calls = termination_calls

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
            for e in oc.instances:
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
            variable.clear_derivatives(instances=oc.instances)

        offset = 0  # this is a counter
        # call all varibles which are in the list ODE_variables which is
        # defined in model_components/base/model:
        for (variable, oc) in self.model.ODE_variables:
            # second counter to count how many instances of process_taxa or
            # entities are using the variable:
            next_offset = offset + len(oc.instances)
            # Write values to variables:
            variable.set_values(instances=oc.instances,
                                values=value_array[offset:next_offset])

            # set up the counter:
            offset = next_offset

            # call methods:
            for (process, oc) in self.ode_processes:
                # Items may be entities like Cells or Process Taxa objects
                # like Culture
                for item in oc.instances:
                    process.specification(item, t)

        derivative_array = np.zeros(offset)

        # Calculation of derivatives:
        offset = 0  # Again, a counter
        for (variable, oc) in self.model.ODE_variables:
            next_offset = offset + len(oc.instances)
            # Get the calculated derivatives and write them to output array:
            derivative_array[offset:next_offset] = variable.get_derivatives(
                instances=oc.instances)

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

        self.model.convert_to_standard_units()  # so that no DimensionalQuantities are left

        # First create the dictionary to fill in the trajectory:
        self.trajectory_dict['t'] = np.zeros([0])
        for (v, oc) in self.model.variables:
            self.trajectory_dict[v] = {}

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
            # items are instances of process taxa or entities
            for item in oc.instances:
                if eventtype == "rate":
                    next_time = np.random.exponential(1. / rate_or_timfunc)
                elif eventtype == "time":
                    next_time = rate_or_timfunc(t)
                else:
                    print("        Invalid specification of the Event: ",
                          event.name,
                          "        In entity/process taxa:",
                          oc.instances)
                try:
                    next_discontinuities[next_time].append((event, item))
                except KeyError:
                    next_discontinuities[next_time] = [(event, item)]

        # Fill next_discontinuities with times of step and performn step if
        # necessary, also 2.3 in runner scheme
        for (step, oc) in self.step_processes:
            next_time_func = step.specification[0]
            method = step.specification[1]
            # Here, items are instances of process taxa or entities
            for item in oc.instances:
                if next_time_func(item, t) == t_0:
                    method(item, t)
                    # calling next_time with function:
                    next_time = next_time_func(item, t)
                # Same time for all instances? self. necessary?
                else:
                    next_time = next_time_func(item, t)
                try:
                    next_discontinuities[next_time].append((step, item))
                except KeyError:
                    next_discontinuities[next_time] = [(step, item)]

        # Complete/calculate explicit Functions not neccessary, since it is
        # done in get_derivatives

        # Enter while loop
        while t < t_1:
            # print('    t is', t)
            # Get next discontinuity to find the next timestep where something
            # happens
            # If there are no discontinuities, the next_discontinuities
            # dict is empty, therefore try is necessary:
            if self.terminate():
                print('Break out of while-loop at time ', t)
                break
            try:
                next_time = min(next_discontinuities.keys())
            except ValueError:
                next_time = t_1
            # print('    next time is', next_time)
            # Divide time until discontinuity into timesteps of sice dt:
            npoints = np.ceil((next_time - t) / dt) + 1  # resolution
            ts = np.linspace(t, next_time, npoints)

            # Call Odeint if there are ODEs:
            if self.model.ODE_processes:
                # Compose initial value-array:
                offset = 0
                # Find out how many variables we have:
                for (variable, oc) in self.model.ODE_variables:
                    next_offset = offset + len(oc.instances)
                    offset = next_offset
                initial_array_ode = np.zeros(offset)
                offset = 0
                # Fill initial_array_ode with values:
                for (variable, oc) in self.model.ODE_variables:
                    next_offset = offset + len(oc.instances)
                    initial_array_ode[offset:next_offset] = \
                        variable.get_values(instances=oc.instances)
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
                        # take all entities or process taxa objects:
                        items = oc.instances
                        v.set_values(instances=items, values=ode_values)
                    # calculate explicits if existent
                    if self.model.explicit_processes:
                        self.complete_explicits(time)
                        # save values of explicits:
                        self.save_to_traj(self.model.explicit_variables)

                    # Same with Event variables:
                    if self.model.event_processes:
                        self.save_to_traj(self.model.event_variables)

                    # Same for step variables:
                    if self.model.step_processes:
                        self.save_to_traj(self.model.step_variables)

            # Also save t values
            time_np = np.array(ts)
            self.trajectory_dict['t'] = np.concatenate((
                                            self.trajectory_dict['t'],
                                            time_np))

            # save odes to trajectory dict
            if self.model.ODE_processes:
                offset = 0
                for (v, oc) in self.model.ODE_variables:
                    # print('variable, oc:', v, oc)
                    next_offset = offset + len(oc.instances)
                    for i, item in enumerate(oc.instances):
                        item = oc.instances[i]
                        values = ode_trajectory[:, offset + i]
                        try:
                            self.trajectory_dict[v][item] = np.concatenate((
                                self.trajectory_dict[v][item], values))
                        except KeyError:
                            self.trajectory_dict[v][item] = values
                    offset = next_offset

            # After all that is done, calculate what happens at the
            # discontinuity, step 3.4 in runner scheme
            # Delete the discontinuity from the dictionary and calculate when
            # the next one happens:
            t = next_time
            if next_discontinuities:
                for discontinuity in next_discontinuities.pop(t):
                    # print('        Entering the dicontinuity loop, t=', t)
                    # discontinuity is a tupel with (event/step,
                    # entity/process taxon object)
                    item = discontinuity[1]
                    happening = discontinuity[0]
                    if isinstance(happening, Event):
                        eventtype = happening.specification[0]
                        rate_or_timfunc = happening.specification[1]
                        method = happening.specification[2]
                        # Perform the event:
                        method(item, t)
                        # Add its next discontinuity:
                        if eventtype == "rate":
                            next_time = t + \
                                        np.random.exponential(1. /
                                                              rate_or_timfunc)
                        elif eventtype == "time":
                            next_time = rate_or_timfunc(t)
                        else:
                            print("Invalid specification of the Event: ",
                                  happening.name,
                                  "In entity/process taxon:",
                                  item)
                        try:
                            next_discontinuities[next_time].append((happening,
                                                                    item))
                        except KeyError:
                            next_discontinuities[next_time] = [(happening,
                                                                item)]
                    elif isinstance(happening, Step):
                        method = happening.specification[1]
                        timefunc = happening.specification[0]
                        # Item is an entity or a process taxon object
                        method(item, t)
                        next_time = timefunc(item, t)
                        try:
                            next_discontinuities[next_time].append((happening,
                                                                    item))
                        except KeyError:
                            next_discontinuities[next_time] = [(happening,
                                                                item)]

            # Complete state again, 3.5 in runner scheme:
            if self.model.explicit_processes:
                self.complete_explicits(t)

            # Store all information that has been calculated at time t ->
            # iterate through all process variables!
            self.save_to_traj(self.model.process_variables)

            t_np = np.array([t])
            self.trajectory_dict['t'] = np.concatenate((
                                            self.trajectory_dict['t'],
                                            t_np))

        # Store all information that has not been changed during calculations:
        non_process_vars = [(v, oc) for (v, oc) in self.model.variables
                            if (v, oc) not in self.model.process_variables]
        self.save_to_traj(non_process_vars)

        return self.trajectory_dict

    def save_to_traj(self, liste):
        """Save to dictionary.

        Function to save a given list like self.model.variables
        to the trajectory dictionary. It saves to self.trajectory_dict. To use
        it do:
        trajectory_dict = save_to_traj(self.model.variables)

        Parameters
        ----------
        liste
        traj_dict

        Returns
        -------
        """
        for (v, oc) in liste:
            instances = oc.instances
            values = v.get_values(instances)
            for i, item in enumerate(instances):
                value = np.array([values[i]])
                try:
                    self.trajectory_dict[v][item] = np.concatenate((
                        self.trajectory_dict[v][item], value))
                except KeyError:
                    self.trajectory_dict[v][item] = value

    def terminate(self):
        """Determine if the runner should stop.

        Apply all callables specified in self.termination_calls on their
        respective instances. If one of them indicates a termination condition
        by returning True, then return True. Else return False.

        Returns
        -------
        boolean : True, if the runner should stop according to one of the
            callables in self.termination_calls.
            False, if there are no such callables or if they all return False.
        """
        if self.termination_calls:
            for signal in self.termination_calls:
                method = signal[0]
                item = signal[1]
                if method(item):
                    return True
        return False
