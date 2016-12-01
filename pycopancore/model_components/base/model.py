# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Here the docstring is missing
"""

#
#  Imports
#

from pycopancore import Variable, ODE, Explicit, Step, Event
from .interface import Model_
from . import Cell, Nature, Individual, Culture, Society, Metabolism
import inspect

#
#  Define class Model
#


class Model (Model_):
    """
    Again, a docstring is missing
    """

    #
    # Definitions of class attributes
    #

    cell_mixin = Cell
    individual_mixin = Individual
    society_mixin = Society

    nature_mixin = Nature
    culture_mixin = Culture
    metabolism_mixin = Metabolism

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 # *,
                 cells=None,
                 individuals=None,
                 societies=None,
                 nature=None,
                 culture=None,
                 metabolism=None,
                 **kwargs
                 ):
        """
        Initializes an instance of Model.

        Parameters
        ----------
        cells
        individuals
        societies
        nature
        culture
        metabolism
        kwargs
        """
        super(Model, self).__init__(**kwargs)

        self.nature = nature
        self.individuals = individuals
        self.metabolism = metabolism
        self.individuals = individuals
        self.cells = cells
        self.societies = societies

        # This is defined if model.configure was called before
        for v in self.variables:
            if v.entity_type == Individual:
                v.entities = self.individuals
            elif v.entity_type == Cell:
                v.entities = self.cells
            elif v.entity_type == Society:
                v.entities = self.societies

    #
    #  Definitions of further methods
    #

    @property
    def entities(self):
        """
        A function to return the entities to that corresponding variables are
        assigned from the Model instance.

        Returns
        -------
        A list of all to the corresponding Variable assigned entities
        """
        return self.individuals + self.societies + self.cells

    @classmethod
    def configure(cls):
        """
        This classmethod configures the mixin models by allocating variables
        and processes to designated lists.
        """

        cls.society_variables_dict = {}
        cls.society_processes = []
        cls.cell_variables_dict = {}
        cls.cell_processes = []
        cls.individual_variables_dict = {}
        cls.individual_processes = []
        cls.metabolism_processes = []
        cls.metabolism_variables_dict = {}
        cls.nature_processes = []
        cls.nature_variables_dict = {}
        cls.culture_processes = []
        cls.culture_variables_dict = {}
        cls.other_variables_dict = {}
        cls.variables = []
        cls.processes = []

        cls.ODE_variables = []
        cls.explicit_variables = []
        cls.step_variables = []
        cls.event_variables = []

        print("\nConfiguring model", cls.name, "(", cls, ") ...")
        print("Analysing model structure...")
        parents = list(inspect.getmro(cls))[1:]
        cls.components = [c for c in parents
                          if c is not Model_
                          and Model_ in inspect.getmro(c)
                          ]
        for c in cls.components:
            interfaceclass = c.__base__
            print("Model component:", interfaceclass.name, "(", c, ")...")

            if c.cell_mixin is not None:
                cparents = list(inspect.getmro(c.cell_mixin))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    print("Cell variable:", v)
                    if k in cls.cell_variables_dict:
                        print("already registered by another component")
                        continue  # This was not in Jobsts Prototype
                        # (not sure yet,need to think about this)
                    v.entity_type = Cell
                    v._codename = k
                    cls.cell_variables_dict[k] = v

                for p in c.cell_mixin.processes:
                    print("Cell process:", p)
                    cls.cell_processes.append(p)

            if c.individual_mixin is not None:
                iparents = list(inspect.getmro(c.individual_mixin))
                ivardict = {k: v
                            for cp in iparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in ivardict.items():
                    print("Individual variable:", v)
                    if k in cls.individual_variables_dict:
                        print("already registered by another component")
                        continue  # This was not in Jobsts Prototype
                        # (not sure yet,need to think about this)
                    v.entity_type = Individual
                    v._codename = k
                    cls.individual_variables_dict[k] = v

                for p in c.individual_mixin.processes:
                    print("Individual process:", p)
                    cls.individual_processes.append(p)

            if c.society_mixin is not None:
                sparents = list(inspect.getmro(c.society_mixin))
                svardict = {k: v
                            for cp in sparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in svardict.items():
                    print("Society variable:", v)
                    if k in cls.society_variables_dict:
                        print("already registered by another component")
                        continue  # This was not in Jobsts Prototype
                        # (not sure yet,need to think about this)
                    v.entity_type = Society
                    v._codename = k
                    cls.society_variables_dict[k] = v

                for p in c.society_mixin.processes:
                    print("Society process:", p)
                    cls.society_processes.append(p)

            if c.nature_mixin is not None:
                nparents = list(inspect.getmro(c.nature_mixin))
                nvardict = {k: v
                            for cp in nparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in nvardict.items():
                    print("Nature variable:", v)
                    if k in cls.nature_variables_dict:
                        print("already registered by another component")
                        continue  # This was not in Jobsts Prototype
                        # (not sure yet,need to think about this)
                    v.entity_type = Nature
                    v._codename = k
                    cls.nature_variables_dict[k] = v

                for p in c.nature_mixin.processes:
                    print("Nature process:", p)
                    cls.nature_processes.append(p)

            if c.culture_mixin is not None:
                cparents = list(inspect.getmro(c.culture_mixin))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    print("Culture variable:", v)
                    if k in cls.culture_variables_dict:
                        print("already registered by another component")
                        continue  # This was not in Jobsts Prototype
                        # (not sure yet,need to think about this)
                    v.entity_type = Culture
                    v._codename = k
                    cls.culture_variables_dict[k] = v

                for p in c.culture_mixin.processes:
                    print("Culture process:", p)
                    cls.culture_processes.append(p)

            if c.metabolism_mixin is not None:
                mparents = list(inspect.getmro(c.metabolism_mixin))
                mvardict = {k: v
                            for cp in mparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in mvardict.items():
                    print("Metabolism variable:", v)
                    if k in cls.metabolism_variables_dict:
                        print("already registered by another component")
                        continue  # This was not in Jobsts Prototype
                        # (not sure yet,need to think about this)
                    v.entity_type = Metabolism
                    v._codename = k
                    cls.metabolism_variables_dict[k] = v

                for p in c.metabolism_mixin.processes:
                    print("Metabolism process:", p)
                    cls.metabolism_processes.append(p)

            cls.variables = (list(cls.cell_variables_dict.values()) +
                             list(cls.individual_variables_dict.values()) +
                             list(cls.society_variables_dict.values()) +
                             list(cls.nature_variables_dict.values()) +
                             list(cls.culture_variables_dict.values()) +
                             list(cls.metabolism_variables_dict.values()))
            cls.processes = (cls.cell_processes +
                             cls.individual_processes +
                             cls.society_processes +
                             cls.nature_processes +
                             cls.culture_processes +
                             cls.metabolism_processes)

            for process in cls.processes:
                if isinstance(process, ODE):
                    cls.ODE_variables += process.variables
                if isinstance(process, Explicit):
                    cls.explicit_variables += process.variables
                if isinstance(process, Step):
                    cls.step_variables += process.variables
                if isinstance(process, Event):
                    cls.event_variables += process.variables

        print("...done")
