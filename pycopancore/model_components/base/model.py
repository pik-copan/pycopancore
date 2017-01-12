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

from pycopancore import Variable, ODE, Explicit, Step, Event, \
    _AbstractEntityMixin, _AbstractDynamicsMixin
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
                 **kwargs
                 ):
        """
        Initializes an instance of Model.

        Parameters
        ----------
        kwargs: dict
            entities being a dict containing entities as entries and their
            class as key
        """

        super().__init__()

        self._process_taxon_objects = {pt: pt() for pt in self.process_taxa}
        self.entities_dict = kwargs['entities']

        # TODO:
        # is it necessary to make all items in self.entities_dict known
        # to the object itself?

        # TODO:
        # Is this really what owning_classes is about???
        # Tell all variables and proceses which entities they have,
        # so set v/p.owning_classes:
        for (p, oc) in self.processes:
            p.owning_classes = self.entities_dict[oc]
        for (v, oc) in self.variables:
            v.owning_classes = self.entities_dict[oc]

        print('     base model instantiated')

    def __repr__(self):
        """
        Return a string representation of the object of class base.Model.
        """
        # Is it necessary to list all objects? Or are classes sufficient?
        keys_entities = []
        keys_process_taxa = []
        for key, item in self.entities_dict:
            keys_entities.append(key)
        for key, item in self._process_taxon_objects:
            keys_process_taxa.append(key)
        return (super().__repr__() +
                ('base.model object with entities %r /'
                 'and process taxa %r'
                 ) % (keys_entities,
                      keys_process_taxa
                      )
                )

    #
    #  Definitions of further methods
    #

    @property
    def entities(self):
        """
        A function to return a dictionary with classes as key and entities as
        entries

        Returns
        -------
        A dictionary with classes as key and entites as entries
        """
        # Is it better to have the owning class as key or the subclass, so
        # for example base.Cell or base_and_dummy.Cell?

        return self.entities_dict

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

        # First analyse by component:
        parents = list(inspect.getmro(cls))[1:]
        cls.components = [c for c in parents
                          if c is not abstract.Model
                          and abstract.Model in inspect.getmro(c)
                          ]
        print('\nComponents:', cls.components)
        for c in cls.components:
            interfaceclass = c.__bases__[0]
            print("Model component:", interfaceclass.name, "(", c, ")...")
            # Iterate through all mixins of the component:
            for etmixin in c.entity_types:
                print('    Entity-type:', etmixin)
                cparents = list(inspect.getmro(etmixin))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    print("        Variable:", v)
                    # check if same var. object was already registered:
                    if v in cls.variables_dict.values():
                        print("            already registered by another "
                              "component")
                        assert v._codename == k, ('with Codename', k)
                    if k in cls.variables_dict.keys():
                        print("            already registered by another "
                              "component")
                        assert cls.variables_dict[k] == v, \
                            'Codename already in use by another variable'
                    v._codename = k
                    cls.variables_dict[k] = v

                for p in etmixin.processes:
                    print("        Process:", p)

            # Iterate through all process taxon mixins:
            for pt in c.process_taxa:
                print('    Process taxon:', pt)
                cparents = list(inspect.getmro(pt))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    print("        Variable:", v)
                    # check if same var. object was already registered:
                    if v in cls.variables_dict.values():
                        print("          already registered by another "
                              "component")
                        assert v._codename == k, ('with Codename', k)
                    if k in cls.variables_dict.keys():
                        print("          already registered by another "
                              "component")
                        assert cls.variables_dict[k] == v, \
                            'Codename already in use by another variable'
                    v._codename = k
                    cls.variables_dict[k] = v

                for p in pt.processes:
                    print("        Process:", p)

        # Now analyse by entity type and process taxon in order to find correct
        # owning classes:
        print('\nEntity types:', cls.entity_types)
        print('Process taxa:', cls.process_taxa)
        for owning_class in cls.entity_types + cls.process_taxa:
            print('    Entity-type/Process taxon:', owning_class)
            parents = list(inspect.getmro(owning_class))
            components = [c for c in parents
                          if issubclass(c, (_AbstractEntityMixin,
                                            _AbstractDynamicsMixin))
                          and c not in (_AbstractEntityMixin,
                                        _AbstractDynamicsMixin)
                          ]
            for mixin in components:
                print('        Mixin:', mixin)
                cparents = list(inspect.getmro(mixin))
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                for (k, v) in cvardict.items():
                    v.owning_classes.append(owning_class)
                    if (v, owning_class) not in cls.variables:
                        print("        Variable:", v)
                        cls.variables.append((v, owning_class))
                for p in mixin.processes:
                    p.owning_classes.append(owning_class)
                    if (p, owning_class) not in cls.processes:
                        print("        Process:", p)
                        cls.processes.append((p, owning_class))

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

        print("...done")
