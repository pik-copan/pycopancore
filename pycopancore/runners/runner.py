"""Returns the trajectory of a setup given as a model object."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license


# TODO: rename to ScipyODEintRunner

from .. import Event, Step, Variable
from ..private import _AbstractRunner, eval

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
        for p in self.explicit_processes:
            inst = p.owning_class.instances
            spec = p.specification
            if isinstance(spec, list):
                # evaluate symbolic expression and store result in
                # instances' attributes:
                for pos in range(len(spec)):
                    p.variables[pos].set_values(inst, eval(spec[pos], inst))
            else:
                # call process' implementation method which writes
                # to instances' attributes:
                for i in inst:
                    spec(i, t)

    def get_rhs_array(self, value_array, t, 
                      froms, tos, targetclasses, targetvars):
        """Return RHS of composite ODE system as an array.

        Will be passed to scipy.odeint"""
        # Call complete explicit functions, 3.1.2 in runner scheme
        self.complete_explicits(t)

        # copy values from input array into instance attributes
        # and clear instances' derivative attributes:
        for i in range(len(froms)):
            inst = targetclasses[i].instances
            targetvars[i].set_values(instances=inst,
                                     values=value_array[froms[i]:tos[i]])
            targetvars[i].clear_derivatives(instances=inst)

        # let all processes calculate their derivative terms:
        derivative_array = np.zeros(value_array.size)
        for p in self.ode_processes:
            spec = p.specification
            if isinstance(spec, list):
                # evaluate symbolic expression:
                for pos in range(len(spec)):
                    target = p.targets[pos]
                    summands = eval(spec[pos], p.owning_class.instances)
                    if isinstance(target, Variable):
                        # add result directly to
                        # output array (rather than in instances' derivative attrs.):
                        derivative_array[target._from:target._to] += summands
                    else:
                        # adds terms to instances' derivative attributes:
                        target.add_derivatives(p.owning_class.instances, summands)
            else:
                # call process' implementation method which adds terms
                # to instances' derivative attributes:
                for i in p.owning_class.instances:
                    spec(i, t)

        # add derivative terms from derivative attributes to output array:
        for i in range(len(froms)):
            derivative_array[froms[i]:tos[i]] += \
                targetvars[i].get_derivatives(instances=targetclasses[i].instances)

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
        self.trajectory_dict['t'] = []
        for v in self.model.variables:
            self.trajectory_dict[v] = {}

        # Create dictionary to put in the discontinuities:
        next_discontinuities = {}

        # Complete/calculate explicit Functions, 2.2 in runner scheme
        self.complete_explicits(t_0)

        # Fill the dictionary with initial values, 2.3 in runner schmeme:
        for event in self.event_processes:
            eventtype = event.specification[0]
            rate_or_timefunc = event.specification[1]
            # TODO: Check if the following loop is correct:
            # items are instances of process taxa or entities
            for item in event.owning_class.instances:
                if eventtype == "rate":
                    next_time = np.random.exponential(1. / rate_or_timefunc)
                elif eventtype == "time":
                    next_time = rate_or_timefunc(t)
                else:
                    print("        Invalid specification of the Event: ",
                          event.name,
                          "        In entity/process taxa:",
                          event.owning_class.instances)
                try:
                    next_discontinuities[next_time].append((event, item))
                except KeyError:
                    next_discontinuities[next_time] = [(event, item)]

        # Fill next_discontinuities with times of step and performn step if
        # necessary, also 2.3 in runner scheme
        for step in self.step_processes:
            next_time_func = step.specification[0]
            method = step.specification[1]
            # Here, items are instances of process taxa or entities
            for item in step.owning_class.instances:
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
            # Divide time until discontinuity into timesteps of size dt:
            npoints = np.ceil((next_time - t) / dt) + 1  # resolution
            ts = np.linspace(t, next_time, npoints)

            # Call Odeint if there are ODEs:
            if self.model.ODE_processes:

                # determine array layouts
                # and compose initial value-array:
                targetclasses = [(target.owning_class
                                  if isinstance(target, Variable)
                                  else target.get_target_class(target.reference_variable.owning_class.instances[0])
                                  ) for target in self.model.ODE_targets]
                targetvars = [(target if isinstance(target, Variable)
                               else target.get_target_variable(target.reference_variable.owning_class.instances[0])
                               ) for target in self.model.ODE_targets]
                lens = [len(c.instances) for c in targetclasses]
                tos = np.cumsum(lens)
                froms = np.concatenate(([0],tos[:-1]))
                arraylen = sum(lens)
                initial_array_ode = np.zeros(arraylen)
                for i, target in enumerate(self.model.ODE_targets):
                    target._from = froms[i]
                    target._to = tos[i]
                    initial_array_ode[froms[i]:tos[i]] = \
                        targetvars[i].get_values(instances=targetclasses[i].instances)

                # In Odeint, call get_rhs_array to get the RHS of the ODE system
                # as an array, step 3.1 in runner scheme, then return
                # the trajectory, 3.2 in runner scheme:

                ode_trajectory = integrate.odeint(self.get_rhs_array,
                                                  initial_array_ode,
                                                  ts,
                                                  args=(froms, tos, targetclasses, targetvars),
                                                  mxstep=10000  # FIXME: ??
                                                  )

                # Take the time steps used in odeint and calculate explicit
                # functions in retrospect, step 3.3 in runner scheme
                # Save them to an arraySave them to the trajectory_dict
                # This is only done if there are explicit processes:

                for pos, t in enumerate(ts):
                    # write values to objects:
                    ode_values = ode_trajectory[pos, :]
                    # read values from result vector in same order as written into it:
                    for i in range(len(lens)):
                        targetvars[i].set_values(
                                instances=targetclasses[i].instances,
                                values=ode_values[froms[i]:tos[i]])
                    # calculate explicits if existent
                    if self.model.explicit_processes:
                        self.complete_explicits(t)

                    self.save_to_traj(self.model.process_targets 
                                      - self.model.ODE_targets)

            # Also save t values
            self.trajectory_dict['t'] += list(ts)

            # save odes to trajectory dict
            for i in range(len(lens)):
                for pos, item in enumerate(targetclasses[i].instances):
                    values = list(ode_trajectory[:, froms[i] + pos])
                    try:
                        self.trajectory_dict[targetvars[i]][item] += values
                    except KeyError:
                        self.trajectory_dict[targetvars[i]][item] = values

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
                        rate_or_timefunc = happening.specification[1]
                        method = happening.specification[2]
                        # Perform the event:
                        method(item, t)
                        # Add its next discontinuity:
                        if eventtype == "rate":
                            next_time = t + \
                                        np.random.exponential(1. /
                                                              rate_or_timefunc)
                        elif eventtype == "time":
                            next_time = rate_or_timefunc(t)
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
            self.save_to_traj(self.model.process_targets)

            self.trajectory_dict['t'].append(t)

        # Store all information that has not been changed during calculations:
#        self.save_to_traj(self.model.variables - self.model.process_targets)

        return self.trajectory_dict

    def save_to_traj(self, targets):
        """Save to dictionary.

        Function to save a given list like self.model.targets
        to the trajectory dictionary. It saves to self.trajectory_dict. To use
        it do:
        trajectory_dict = save_to_traj(self.model.targets)

        Parameters
        ----------
        vars
        traj_dict

        Returns
        -------
        """
        for target in targets:
            v = target if isinstance(target, Variable) \
                    else target.get_target_variable(target.reference_variable.owning_class.instances[0])
            instances = v.owning_class.instances
            values = v.get_values(instances)
            for i, item in enumerate(instances):
                try:
                    self.trajectory_dict[v][item].append(values[i])
                except KeyError:
                    self.trajectory_dict[v][item] = [values[i]]

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
