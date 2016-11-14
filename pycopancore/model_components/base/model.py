# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
"""

#
#  Imports
#

from pycopancore import Variable, ODE
from .interface import Model_
from . import Cell, Nature, Individual, Culture, Society, Metabolism
import inspect

#
#  Define class Cell
#


class Model (Model_):
    """
    """

    cell_mixin = Cell
    individual_mixin = Individual
    society_mixin = Society

    nature_mixin = Nature
    culture_mixin = Culture
    metablism_mixin = Metabolism

    @classmethod
    def configure(cls):
        """
        :return:
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

        print("\nConfiguring model", cls.name, "(", cls, ") ...")
        print("Analysing model structure...")
        parents = list(inspect.getmro(cls))[1:]
        cls.components = [c for c in parents if c is not Model_]

        for c in cls.components:
            interfaceclass = c.__bases__[0]
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
                        continue  # This was not in Jobsts Prototype (not sure yet,need to think about this)
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
                        continue  # This was not in Jobsts Prototype (not sure yet,need to think about this)
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
                        continue  # This was not in Jobsts Prototype (not sure yet,need to think about this)
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
                        continue  # This was not in Jobsts Prototype (not sure yet,need to think about this)
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
                        continue  # This was not in Jobsts Prototype (not sure yet,need to think about this)
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
                        continue  # This was not in Jobsts Prototype (not sure yet,need to think about this)
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

            for v in cls.processes:
                if isinstance(v, ODE):
                    cls.ODE_variables += v.variables
                    # TODO: Insert other process types

        print("...done")

    def __init__(self,
                 *,
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

        :param cells: List of cells
        :param individuals: List of individuals
        :param societies: List of societies
        :param nature: Instance of nature
        :param culture: Instance of culture
        :param metabolism: Instance of metabolism
        :param kwargs: other setup arguments
        """
        super(Model, self).__init__(**kwargs)