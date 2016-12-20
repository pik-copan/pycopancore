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
from pycopancore.model_components import abstract
from . import Cell, Nature, Individual, Culture, Society, Metabolism
import inspect

#
#  Define class Model
#


class Model (Model_, abstract.Model):
    """
    This is the base.model file. It serves two purposes:
    1. Be a the model class of the base component, providing the information
    about which mixins are to be used of the component AND:
    2. Provide the configure method.
    The configure method has a very central role in the COPAN:core framework,
    it is called before letting run a model. It then searches which model class
    is used from the model module. It will then go through all components
    listed there and collect all variables and processes of said components.
    """

    #
    # Definitions of class attributes
    #

    entity_types = [Cell, Individual, Society]
    process_taxa = [Nature, Culture, Metabolism]

    #
    #  Definitions of internal methods
    #

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
        self.culture = culture

        for (v, oc) in self.variables:
            if v.entity_type == Society:
                v.entities = self.societies
            elif v.entity_type == Cell:
                v.entities = self.cells
            elif v.entity_type == Individual:
                v.entities = self.individuals

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

        cls.entity_variables = []
        cls.taxon_variables = []

        cls.variables = []  # save in pairs: (variable, owning_class)
        cls.processes = []  # save in pairs: (process, owning_class)

        cls.variables_dict = {}

        cls.ODE_variables = []
        cls.explicit_variables = []
        cls.step_variables = []
        cls.event_variables = []

        cls.ODE_processes = []
        cls.explicit_processes = []
        cls.step_processes = []
        cls.event_processes = []

        print("\nConfiguring model", cls.name, "(", cls, ") ...")
        print("Analysing model structure...")
        parents = list(inspect.getmro(cls))[1:]
        cls.components = [c for c in parents
                          if c is not abstract.Model
                          and abstract.Model in inspect.getmro(c)
                          ]
        print('components are:', cls.components)
        for c in cls.components:
            interfaceclass = c.__bases__[0]
            print("Model component:", interfaceclass.name, "(", c, ")...")
            # Iterate through all mixins of the component:
            for et in c.entity_types:
                print('     entity-type', et)
                cparents = list(inspect.getmro(et))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    print("         variable:", v)
                    # check if same var. object was already registered:
                    if v in [v2 for (v2, et2) in cls.variables]:
                        print("already registered by another component")
                        assert v._codename == k, ('with Codename', k)
                    if k in cls.variables_dict:
                        print("already registered by another component")
                        assert cls.variables_dict[k] == v, \
                            'Codename already in use by another variable'
                    v._codename = k
                    cls.variables_dict[k] = v
                    cls.variables.append((v, et))

                for p in et.processes:
                    print("         process:", p)
                    cls.processes.append((p, et))

            # Iterate through all process taxon mixins:
            for pt in c.process_taxa:
                print('     process taxon', pt)
                cparents = list(inspect.getmro(pt))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    print("         variable:", v)
                    # check if same var. object was already registered:
                    if v in [v2 for (v2, et2) in cls.variables]:
                        print("already registered by another component")
                        assert v._codename == k, ('with Codename', k)
                    if k in cls.variables_dict:
                        print("already registered by another component")
                        assert cls.variables_dict[k] == v, \
                            'Codename already in use by another variable'
                    v._codename = k
                    cls.variables_dict[k] = v
                    cls.variables.append((v, pt))

                for p in pt.processes:
                    print("         process:", p)
                    cls.processes.append((p, pt))

            for (process, owning_class) in cls.processes:
                if isinstance(process, ODE):
                    cls.ODE_variables += [(v, owning_class)
                                          for v in process.variables]
                    cls.ODE_processes += [(process, owning_class)]
                elif isinstance(process, Explicit):
                    cls.explicit_variables += [(v, owning_class)
                                               for v in process.variables]
                    cls.explicit_processes += [(process, owning_class)]
                elif isinstance(process, Step):
                    cls.step_variables += [(v, owning_class)
                                           for v in process.variables]
                    cls.step_processes += [(process, owning_class)]
                elif isinstance(process, Event):
                    cls.event_variables += [(v, owning_class)
                                            for v in process.variables]
                    cls.event_processes += [(process, owning_class)]
                else:
                    print('process-type of', process, 'not specified')
                    print(process.__class__.__name__)
                    print(object.__str__(process))
            # TODO: Why is python always appending 2 processes?

        print("...done")
