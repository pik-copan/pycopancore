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
from pycopancore.process_types import Event, Explicit, Implicit, ODE
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
        self.model = model
        self.processes = (model.individual_processes + model.cell_processes
                          + model.society_processes + model.nature_processes
                          + model.metabolism_processes + model.culture_processes
                          + model.processes)
        self.explicit_processes = []
        self.implicit_processes = []
        self.event_processes = []
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
            else:
                print('process-type not specidfied')
