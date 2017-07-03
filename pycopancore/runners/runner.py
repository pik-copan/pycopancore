"""Returns the trajectory of a setup given as a model object."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license


# TODO: rename to ScipyODERunner

from .. import Event, Step, Variable
from ..private import _AbstractRunner, _DotConstruct, eval, unknown
from .hooks import Hooks

from scipy import integrate
import numpy as np

from time import time
# import sys

# from profilehooks import coverage, profile


class Runner(_AbstractRunner):
    """Runner-class, it owns the run function which calculates trajectories.

    Equations might be of type QDE, explicit, step and event, as stated in the
    process_types package.
    """

    _current_iteration = None
    """counter for expression evaluation cache"""

    def __init__(self,
                 *,
                 model,  # TODO: allow this to be given without name!
                 termination_calls=False
                 ):
        """Instantiate an Instance of Runner.

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

        self._current_iteration = 0

#    @profile  # generates time profiling information
    def apply_explicits(self, t):
        """Call all explicit functions to complete or update them.

        Parameters
        ----------
        self
        t

        Returns
        -------

        """
        # TODO: call them in an order that respects dependencies among
        # variables! for this, determine dependency structure in
        # modellogics.configure!
        for p in self.explicit_processes:
            spec = p.specification
            if isinstance(spec, list):
                # evaluate symbolic expressions and store result:
                for i, target in enumerate(p.targets):
                    values = eval(spec[i],
                                  self._current_iteration)
                    # note that values may have different length than
                    # p.owning_class.instances due to broadcasting effects
                    target.fast_set_values(values)
            else:
                # call process' implementation method for each of it's
                # owning class' (!) instances. This will store values in
                # the target (!) instances' attributes:
                for inst in p.owning_class.instances:
                    spec(inst, t)

#    @profile  # generates time profiling information
    def get_rhs_array(self,
                      t, value_array
                      # When using odeint this is needed:
                      # value_array, t
                      ):
        """Return RHS of composite ODE system as an array.

        Will be passed to scipy.odeint.
        """
        self._current_iteration += 1  # marks evaluation caches as outdated

        # Call complete explicit functions, 3.1.2 in runner scheme
        self.apply_explicits(t)

        # copy values from input array into instance attributes,
        # clear target instances' derivative attributes:
        for target in self.model.ODE_targets:
            var = target.target_variable
            var.fast_set_values(values=value_array[target._from:target._to])
            var.clear_derivatives()

        # let all processes calculate their derivative terms:
        derivative_array = np.zeros(value_array.size)
        for p in self.ode_processes:
            spec = p.specification
            if isinstance(spec, list):
                # evaluate symbolic expressions:
                for i, target in enumerate(p.targets):
                    summands = eval(spec[i], self._current_iteration)
                    if isinstance(target, Variable):
                        # add result directly to output array
                        # (rather than in instances' derivative attrs.):
                        derivative_array[target._from:target._to] += summands
                    else:
                        # summands may have different length than
                        # p.owning_class.instances due to broadcasting effects,
                        # hence we cannot simply copy it into the
                        # derivative_array array chunk at
                        # target._from:target._to.
                        # instead, we add terms directly to target instances'
                        # derivative attributes where they will be read from
                        # later:
                        target.add_derivatives(summands)
                        # TODO: use an njitted function add2array(array,
                        # positions, values) and expr._target_positions based
                        # on a new entity attribute _index
                        # that marks the position in the ordered set entities.
                        # when an entity is removed from this set, move the one
                        # at the last position to the freed position.
            else:
                # call process' implementation method for each of it's
                # owning class' (!) instances. This will add terms to
                # the target (!) instances' derivative attributes:
                for inst in p.owning_class.instances:
                    spec(inst, t)

        # add derivative terms from derivative attributes to output array:
        for target in self.model.ODE_targets:
            derivative_array[target._from:target._to] += \
                target.target_variable.get_derivatives(
                instances=target.target_class.instances)

        return derivative_array

    # @profile
    def run(self,
            *,
            t_0=0,
            t_1,
            dt  # TODO: rename to "resolution" since it is only an upper bound?
            # TODO: add some kwargs for choosing solver and setting solver
            # params
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
        print("\nRunning from", t_0, "to", t_1, "at resolution at least",
              dt, "...")

        # Define time:
        t = t_0

        # Convert to standard units, so that no DimensionalQuantities are left
        self.model.convert_to_standard_units()

        # First create the dictionary to fill in the trajectory:
        self.trajectory_dict = {v: {} for v in self.model.variables}
        self.trajectory_dict['t'] = [t]

        # fill trajectory with initial states
        self.save_to_traj(self.model.process_targets)

        # Create dictionary to put in the discontinuities:
        next_discontinuities = {}

        # Complete/calculate explicit Functions, 2.2 in runner scheme
        print("  Initial application of Explicit processes...")
        self.apply_explicits(t_0)

        # TODO: add hooks to runner scheme
        # apply all pre-hooks
        if Hooks._pre_hooks:
            print("  Executing pre-hooks ...")
            Hooks.execute_hooks(Hooks.Types.pre, self.model, t_0)

        # Find first occurrence times of events, 2.3 in runner schmeme:
        print("  Finding times of first occurrence of Events...")
        for event in self.event_processes:
            print("    Event process", event, "...")
            eventtype = event.specification[0]
            rate_or_timefunc = event.specification[1]
            # TODO: Check if the following loop is correct:
            # items are instances of process taxa or entities
            for inst in event.owning_class.instances:
                if eventtype == "rate":
                    next_time = np.random.exponential(1. / rate_or_timefunc)
                    # TODO: if rate_or_timefunc is a function,
                    # it must be used in ode integration to integrate
                    # its cumulative distribution function, and when the
                    # latter crosses a threshold that we randomly draw
                    # here, solout must terminate (see below).
                elif eventtype == "time":
                    next_time = rate_or_timefunc(t)
                else:
                    print("        Invalid specification of the Event: ",
                          event.name,
                          "        In entity/process taxa:",
                          event.owning_class.instances)
                try:
                    next_discontinuities[next_time].append((event, inst))
                except KeyError:
                    next_discontinuities[next_time] = [(event, inst)]
                print("      time", next_time, ":", inst)

        # Fill next_discontinuities with times of step and performn step if
        # necessary, also 2.3 in runner scheme
        print("  Executing Steps and finding times of next execution...")
        for step in self.step_processes:
            print("    Step process", step, "...")
            next_time_func = step.specification[0]
            method = step.specification[1]
            # Here, items are instances of process taxa or entities
            for inst in step.owning_class.instances:
                if next_time_func(inst, t) == t_0:
                    method(inst, t)
                    # calling next_time with function:
                    next_time = next_time_func(inst, t)
                # Same time for all instances? self. necessary?
                else:
                    next_time = next_time_func(inst, t)
                try:
                    next_discontinuities[next_time].append((step, inst))
                except KeyError:
                    next_discontinuities[next_time] = [(step, inst)]
                print("      time", next_time, ":", inst)

        # Complete/calculate explicit Functions not neccessary, since it is
        # done in get_derivatives

        # prepare ODE solver:
        solver = integrate.ode(self.get_rhs_array)
        times = []
        sol = []
        if False:  # apparently dopri5 is faster than vode...
            # bdf or adams doesn't seem to make any difference:
            solver.set_integrator("vode", max_step=dt, method="bdf")
        else:
            solver.set_integrator("dopri5", max_step=dt,
                                  verbosity=1,
                                  nsteps=10000
                                  )

            def solout(thet, y):
                """Save Solution of solver."""
                times.append(thet)
                sol.append(y.copy())
                # TODO: this is the place to implement termination
                # due to events without a priori known occurrence
                # time! if solout returns 0 (or -1?), solver will
                # terminate. Similarly for vode above
                print("      t =", thet, "            ", end='\r')
            solver.set_solout(solout)

        # Enter while loop
        while t < t_1:
            # Get next discontinuity to find the next timestep where something
            # happens
            # If there are no discontinuities, the next_discontinuities
            # dict is empty, therefore try is necessary:
            if self.terminate():
                print('Break out of while-loop at time ', t)
                break
            try:
                next_time = min(next_discontinuities.keys())  # TODO: speed-up?
            except ValueError:
                next_time = t_1

            # Call Odeint if there are ODEs:
            if self.model.ODE_processes:

                print("  Running from", t, "to", next_time, "...")

                # clear all targets _DotConstructs' caches of target instances
                # since events and steps may have changed instance references:
                for target in self.model.ODE_targets \
                        + self.model.explicit_targets:
                    target._target_instances = unknown

                # determine array layouts
                # and compose initial value-array:
                print("    Composing initial value array...")
                lens = [len(target.target_class.instances)
                        for target in self.model.ODE_targets]
                tos = np.cumsum(lens)
                froms = np.concatenate(([0], tos[:-1]))
                arraylen = sum(lens)
                initial_array_ode = np.zeros(arraylen)
                for i, target in enumerate(self.model.ODE_targets):
                    target._from = froms[i]
                    target._to = tos[i]
                    initial_array_ode[froms[i]:tos[i]] = \
                        target.target_variable.eval(
                        instances=target.target_class.instances)

                # In Odeint, call get_rhs_array to get the RHS of the ODE
                # system as an array, step 3.1 in runner scheme, then return
                # the trajectory, 3.2 in runner scheme:

                print("    Calling ODE solver...")
                _starttime = time()

# OLD VERSION USING odeint WAS MUCH SLOWER:
#                # Divide time until discontinuity into timesteps of size dt:
#                npoints = np.ceil((next_time - t) / dt) + 1  # resolution
#                ts = np.linspace(t, next_time, npoints)
#
#                ode_trajectory = integrate.odeint(
#                                                  self.get_rhs_array,
#                                                  initial_array_ode,
#                                                  ts,
#                                                  mxstep=10000  # FIXME: ??
#                                                  )

# NEW VERSION WITH ODE IS MUCH FASTER:
                times = []
                sol = []
                if False:  # apparently dopri5 is faster than vode...
                    solver.set_initial_value(initial_array_ode, t)
                    while solver.t < next_time:
                        solver.integrate(next_time, step=True)
                        times.append(solver.t)
                        sol.append(solver.y)
                        # TODO: implement possible termination? see below...
                        print("        ", solver.t, end='\r')
                else:
                    solver.set_initial_value(initial_array_ode, t)
                    solver.integrate(next_time)
                ts = np.array(times)
                ode_trajectory = np.array(sol)

                # TODO: capture solver failures!

                print("      ...took", time() - _starttime, "seconds and",
                      len(times), "time steps")

                # Save t values to output dict:
                self.trajectory_dict['t'] += list(ts)

                print("    Saving returned matrix to output dict...")
                # save trajectory of ODE variables to output dict:
                tlen = len(self.trajectory_dict['t'])
                for i, target in enumerate(self.model.ODE_targets):
                    for pos, inst in enumerate(target.target_class.instances):
                        values = list(
                            ode_trajectory[:, target._from + pos])
                        try:
                            if len(self.trajectory_dict[
                                    target.target_variable][inst]) < tlen:
                                self.trajectory_dict[
                                    target.target_variable][inst] += values
                        except KeyError:
                            self.trajectory_dict[
                                target.target_variable][inst] = values

                # Take the time steps used in odeint and calculate explicit
                # functions in retrospect, step 3.3 in runner scheme
                # Save them to an arraySave them to the trajectory_dict
                # This is only done if there are explicit processes:

                if len(self.explicit_processes) > 0:
                    print("    Applying Explicit processes to simulated "
                          "trajectory...")
                    for pos, t in enumerate(ts):
                        # copy values from returned matrix to instances'
                        # attributes:
                        ode_values = ode_trajectory[pos, :]
                        # read values from result vector in same order as
                        # written into it:
                        for i, target in enumerate(self.model.ODE_targets):
                            target.target_variable.fast_set_values(
                                ode_values[target._from:target._to])
                        self.apply_explicits(t)
                        # complete the output dictionary:
    #                    print("    Completing output dict for time",t)
                        self.save_to_traj(self.model.process_targets)

            # After all that is done, calculate what happens at the
            # discontinuity, step 3.4 in runner scheme
            # Delete the discontinuity from the dictionary and calculate when
            # the next one happens:
            if len(next_discontinuities) > 0:

                t = next_time
                self.trajectory_dict['t'].append(t)

                print("  Executing Steps and Events at", t, "...")

                for discontinuity in next_discontinuities.pop(t):
                    # print('        Entering the dicontinuity loop, t=', t)
                    # discontinuity is a tupel with (event/step,
                    # entity/process taxon object)
                    inst = discontinuity[1]
                    process = discontinuity[0]
                    if isinstance(process, Event):
                        print("    Event", process, "@", inst, "...")
                        eventtype = process.specification[0]
                        rate_or_timefunc = process.specification[1]
                        method = process.specification[2]
                        # Perform the event:
                        method(inst, t)
                        # Add its next discontinuity:
                        if eventtype == "rate":
                            next_time = t + \
                                np.random.exponential(1. /
                                                      rate_or_timefunc)
                        elif eventtype == "time":
                            next_time = rate_or_timefunc(t)
                        else:
                            print("Invalid specification of the Event: ",
                                  process.name,
                                  "In entity/process taxon:",
                                  inst)
                        try:
                            next_discontinuities[next_time].append((process,
                                                                    inst))
                        except KeyError:
                            next_discontinuities[next_time] = [(process,
                                                                inst)]
                        print("      next time", next_time)
                    elif isinstance(process, Step):
                        print("    Step", process, "@", inst, "...")
                        method = process.specification[1]
                        timefunc = process.specification[0]
                        # Item is an entity or a process taxon object
                        method(inst, t)
                        next_time = timefunc(inst, t)
                        try:
                            next_discontinuities[next_time].append((process,
                                                                    inst))
                        except KeyError:
                            next_discontinuities[next_time] = [(process,
                                                                inst)]
                        print("      next time", next_time)

                # Complete state again, 3.5 in runner scheme:
                print("    Applying Explicit processes to changed state...")
                if self.model.explicit_processes:
                    self.apply_explicits(t)

                # Store all information that has been calculated at time t ->
                # iterate through all process variables!
                print("    Completing output dict...")
                self.save_to_traj(self.model.process_targets)

            # TODO: add hooks to runner scheme
            # apply all mid-hooks
            if Hooks._mid_hooks:
                print("  Executing mid-hooks ...")
                Hooks.execute_hooks(Hooks.Types.mid, self.model, t_0)

        # TODO: add hooks to runner scheme
        # apply all post-hooks
        if Hooks._post_hooks:
            print("  Executing post-hooks ...")
            Hooks.execute_hooks(Hooks.Types.post, self.model, t_0)

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
        tlen = len(self.trajectory_dict["t"])
        for target in targets:
            var = target.target_variable
            instances = target.target_class.instances
            values = var.eval(instances)
            for i, inst in enumerate(instances):
                try:
                    if len(self.trajectory_dict[var][inst]) < tlen:
                        self.trajectory_dict[var][inst].append(values[i])
                except KeyError:
                    self.trajectory_dict[var][inst] = [values[i]]

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
                inst = signal[1]
                if method(inst):
                    return True
        return False
