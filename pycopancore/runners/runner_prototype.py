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
from scipy import integrate
import numpy as np

#
# Definition of class _AbstractRunner
#


class RunnerPrototype(_AbstractRunner):
    """
    This is the Runnerprototype. It shall be implemented:
    ODES
    Explicits
    Events
    Steps
    """

    def __init__(self,
                 *,
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
        self.event_processes = []
        self.step_processes = []
        self.ode_processes = []

        for process in self.processes:
            if isinstance(process, Explicit):
                self.explicit_processes.append(process)
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
            list that includes all variables that shall be added to the
            trajectories

        Returns
        -------
        trajectory_dict: dict
            dictionary with time and output variables as keys and list
            with their values over the time integrated
        """

        t = t_0

        #
        # Calculation of next times at that upcoming events occur and storage in
        # next_discontinuities dict.
        #

        past_discontinuities = {}  # dict to store past discontinuities
        next_discontinuities = {}  # dict to store upcoming discontinuities
        for event in self.event_processes:
            eventtype = event.specification[0]
            rate_or_timfunc = event.specification[1]
            if eventtype == "rate":
                next_time = np.random.exponential(1. / rate_or_timfunc)
            elif eventtype == "time":
                next_time = rate_or_timfunc(t)
                # TODO : Do we actually want to implement individualized
                # TODO : ... discontinuities for single entities as well? If so
                # TODO : ... we could add "time_individual" as eventtype and a
                # TODO : ... for-loop.
            else:
                print("Invalid specification of the Event: ", event.name)
            try:
                next_discontinuities[next_time].append(event)
            except KeyError:
                next_discontinuities[next_time] = [event]

        #
        # Performing the first step if first_execution of specification list is
        # set to t = t_0 and storage of the next time. If first_execution is not
        # at t = t_0 storage of first_execution in next_time.
        # TODO: implementation of individualized next_times for entities

        step_variables = []  # list to store
        # loop over all step processes
        for step in self.step_processes:
            first_execution_time = step.specification[0]
            next_time_func = step.specification[1]
            method = step.specification[2]
            variables = step.variables  # cache variable list
            if first_execution_time == t_0:
                # loop over all variables of corresponding step
                i = 0
                for variable in variables:
                    # loop over all entities of corresponding variable
                    for entity in self.model.step_variable.entities:
                        # also possible: variable.entities
                        step_variable = method(entity, t)[1][i]
                        # returns variables that are returned in second index
                        step_variables.append(step_variable)
                    variable.set_values(self.model.step_variable.entities,
                                        step_variables)
                    # writes the calculated variable of entity into list
                    i += 1
                next_time = next_time_func(t)  # calling next_time with function
                # Same time for all entities? self. necessary?
            else:
                next_time = first_execution_time
            try:
                next_discontinuities[next_time].append(step)
            except KeyError:
                next_discontinuities[next_time] = [step]

        #
        # In the following while-loop piecewise integration, from discontinuity
        # to discontinuity is performed.
        #

        print('discontinuities', next_discontinuities)
        print('processes', self.processes)
        print('explicit_processes', self.explicit_processes)
        print('step_processes', self.step_processes)
        print('ode_processes', self.ode_processes)
        print('event_processes', self.event_processes)

        while t < t_1:

            next_time = min(next_discontinuities.keys())
            # find next discontinuity

            #
            # composition of initial_value array and integration of the ODEs.
            # Storage in ode_matrix.
            #

            # compose initial value array
            offset = 0
            for variable in self.model.ODE_variables:
                next_offset = offset + len(variable.entities)
                offset = next_offset
            initial_array_ode = np.zeros(offset)
            offset = 0
            for variable in self.model.ODE_variables:
                next_offset = offset + len(variable.entities)
                initial_array_ode[offset:next_offset] =\
                    variable.get_value_list(entities=variable.entities)
                offset = next_offset

            # odeint integration
            # TODO: implement explicit function in odeint does not work properly
            npoints = np.ceil((next_time - t) / dt) + 1  # resolution
            # assure required resolution
            ts = np.linspace(t, next_time, npoints)
            ode_matrix = integrate.odeint(self.odeint_rhs,
                                          initial_array_ode,
                                          ts)
            # This is a flat matrix. maybe make like explicit_matrix

            #
            # Computation and storage of explicit_variables in explicit_matrix
            #

            # building matrix_explicit to store variable outcomes
            shape1 = len(self.model.explicit_variables.entities)
            shape2 = len(self.explicit_processes)
            explicit_matrix = np.zeros(shape=(shape2, shape1))

            # call explicit functions TODO: adjust indices of explicit matrix
            j = 0
            for process in self.explicit_processes:
                    i = 0
                    for entity in self.model.explicit_variables.entities:
                        explicit_matrix[j, i] = process.specification(entity, t)
                        i += 1
                    j += 1

            #
            # Performing Discontinuity (events and steps) and storing variables
            # TODO: the whole calculation of the variables
            # TODO: storing them in "event_matrix" and "step_matrix"
            #

            t = next_time
            past_discontinuities[t] = []
            for discontinuity in next_discontinuities.pop(t):
                name = discontinuity.name
                variables = discontinuity.variables
                if isinstance(discontinuity, Event):
                    eventtype = discontinuity.specification[0]
                    rate_or_timfunc = discontinuity.specification[1]
                    method = discontinuity.specification[2]
                    event_variables = method(t)  # performing event TODO!!!
                    if eventtype == "rate":
                        next_time = (t + np.random.exponential(1. /
                                                               rate_or_timfunc))
                    elif eventtype == "time":
                        next_time = rate_or_timfunc(t)
                        # TODO : Do we actually want to implement individualized
                        # TODO : ... discontinuities for single entities as
                        # TODO : ... well? If so
                        # TODO : ... we could add "time_individual" as
                        # TODO : ...eventtype and a
                        # TODO : ... for-loop.
                    else:
                        print(eventtype, "is not implemented yet")
                    try:
                        next_discontinuities[next_time].append(discontinuity)
                    except KeyError:
                        next_discontinuities[next_time] = [discontinuity]
                # TODO: the following calculation of step_variables
                elif isinstance(discontinuity, Step):
                    method = discontinuity.specification[2]
                    next_time, step_variables = method(t)
                    try:
                        next_discontinuities[next_time].append(discontinuity)
                    except KeyError:
                        next_discontinuities[next_time] = [discontinuity]
                past_discontinuities[t].append(name)

            #
            # TODO 1: sorting out odeint calculation with calls of explicit_func
            #
            # TODO 2: finish the discontinuity calculation in the while-loop
            #
            # TODO 3: storing ode_matrix, explicit_matrix, step_matrix and
            # TODO 3: ... event_matrix into entity variables with set_values of
            # TODO 3: ... class "Variable"
            #
            # TODO 4: Creating Trajectory
            #
            #
            # TODO 5: Ŕeturn value of this function/method
            #
            # TODO 6: Add individualized next_times
            #

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
        # Construction of derivative array from ode_variables in the following
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
        # Call explicit functions
        #
        # TODO: I am not sure if that works properly. I tried to implement an
        # TODO: ... easy function in an ode in jupyter notebook and the outcomes
        # TODO: ... were pretty strange. Maybe we need another integrator for
        # TODO: ... this?

        for process in self.explicit_processes:
            for entity in self.model.explicit_variables.entities:
                process.specification(entity,t)

        #
        # Call derivatives of odes
        #

        for process in self.ode_processes:
            for entity in self.model.ODE_variables.entities:
                process.specification(entity, t)

        # Calculation of derivatives
        offset = 0  # Again, a counter
        for variable in self.model.ODE_variables:
            next_offset = offset + len(variable.entities)
            rhs_array[offset:next_offset] = variable.get_derivatives(
                entities=variable.entities)
            # Get the calculated derivatives and write them to output array
            offset = next_offset

        return rhs_array
