"""Central module in copan:core.

This module is the model of the base component and also owns the configure
method. This method is central to the framework since it fuses together
the used classes and puts information about process types and variables
in special list to be accessed by the runner.
"""

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

from pycopancore import Variable, ODE, Explicit, Step, Event, \
    _AbstractEntityMixin, _AbstractProcessTaxonMixin
from .interface import Model_
from pycopancore.model_components import abstract
from . import World, Cell, Nature, Individual, Culture, Society, \
    Metabolism
import inspect

#
#  Define class Model
#


class Model (Model_, abstract.Model):
    """Defnie the base.model class.

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

    entity_types = [World, Cell, Individual, Society]
    process_taxa = [Nature, Culture, Metabolism]

    #
    #  Definitions of internal methods
    #

    __configured = False

    def __new__(cls, *args, reconfigure=False, **kwargs):
        """Perform __new__ method.

        Only when an instance of Model is created for the first time the
        method configure is called.
        """
        # reconfigure = kwargs['reconfigure']
        # reconfigure = kwargs.get('reconfigure', False)
        if not cls.__configured or reconfigure:
            cls.configure()
        return super(Model, cls).__new__(cls)

    def __init__(self,
                 **kwargs
                 ):
        """Initialize an instance of Model.

        Parameters
        ----------
        kwargs: Not in Use right now
        """
        super().__init__(**kwargs)

        self._process_taxon_objects = {pt: pt() for pt in self.process_taxa}
        self.entities_dict = {}
        for c in self.entity_types:
            self.entities_dict[c] = c.instances

        # TODO:
        # is it necessary to make all items in self.entities_dict known
        # to the object itself?

        # TODO:
        # Is this really what owning_classes is about???
        # Tell all variables and proceses which entities they have,
        # so set v/p.owning_classes:
        # for (p, oc) in self.processes:
        #     p.owning_classes = self.entities_dict[oc]
        # for (v, oc) in self.variables:
        #     v.owning_classes = self.entities_dict[oc]

        print('     base model instantiated')

    def __repr__(self):
        """Return a string representation of the base.Model."""
        # Is it necessary to list all objects? Or are classes sufficient?
        keys_entities = []
        keys_process_taxa = []
        for key, item in self.entities_dict:
            keys_entities.append(key)
        for key, item in self._process_taxon_objects:
            keys_process_taxa.append(key)
        return (super().__repr__() +
                ('base.model object with entities {} /'
                 'and process taxa {}'.format(keys_entities, keys_process_taxa)
                 )
                )

    #
    #  Definitions of further methods
    #

    @classmethod
    def configure(cls, reconfigure=False, **kwargs):
        """Configure the model.

        This classmethod configures the chosen mixin model of the 'models'
        package by allocating all required variables and processes to
        designated
        lists.

        Parameter
        ---------
        reconfigure : bool
            Flag that indicates if the model should be reconfigured
        """
        if cls.__configured and not reconfigure:
            raise ConfigureError("This model is already configured. "
                                 "Use optional argument 'reconfigure'")

        cls.variables = []  # save in pairs: (variable, owning_class)
        cls.processes = []  # save in pairs: (process, owning_class)

        cls.variables_dict = {}

        cls.process_variables = []

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

        # Construction of a list for the subsequent for-loop. It contains all
        # model mixins the model component inherits from. Only model mixins
        # that inherit from 'abstract.model' are considered. The abstract model
        # itself is excluded as well as the model component:
        parents = list(inspect.getmro(cls))[1:]
        cls.components = [c for c in parents
                          if c is not abstract.Model
                          and abstract.Model in inspect.getmro(c)
                          ]
        print('\nComponents:', cls.components)

        # The for-loop goes through all model mixins as outlined above:
        for c in cls.components:
            interfaceclass = c.__bases__[0]
            print("Model component:", interfaceclass.name, "(", c, ")...")
            # Iterate through all entity type components the model mixin uses:
            for etmixin in c.entity_types:
                print('    Entity-type:', etmixin)
                # getting mixins of the entity type components:
                # TODO: we only need to iterate through interfaces since
                # TODO: ...variables are only defined there:
                cparents = list(inspect.getmro(etmixin))
                # writing variable codenames k and corresponding values v into
                # a dictionary that is needed to check that variables of
                # different components do only overwrite if they are meant to
                # be the same:
                cvardict = {k: v
                            for cp in cparents
                            for (k, v) in cp.__dict__.items()
                            if isinstance(v, Variable)
                            }
                # check if variables and their codenames are unique:
                for (k, v) in cvardict.items():
                    print("        Variable:", v)
                    # check if same var. object was already registered. If its
                    # codename k is different to a previous assigned codename
                    # an assertion error is the output:
                    if v in cls.variables_dict.values():
                        print("            already registered by another "
                              "component")
                        assert v._codename == k, ('with Codename', k)
                    # check if same codename was already registered if not,
                    # same assertion error as above:
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
                                            _AbstractProcessTaxonMixin))
                          and c not in (_AbstractEntityMixin,
                                        _AbstractProcessTaxonMixin)
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
                cls.ODE_processes += [(process, owning_class)]
            elif isinstance(process, Explicit):
                cls.explicit_processes += [(process, owning_class)]
            elif isinstance(process, Step):
                cls.step_processes += [(process, owning_class)]
            elif isinstance(process, Event):
                cls.event_processes += [(process, owning_class)]
            else:
                print('process-type of', process, 'not specified')
                print(process.__class__.__name__)
                print(object.__str__(process))
            for v in process.variables:
                # Find the tuple (var,owc) in cls.variables with var == v
                # to get the owning class of the variable, not necessarily
                # the owning class of the process.
                for (var, owc) in cls.variables:
                    if var == v:
                        voc = owc
                # Add the tuple (v, voc) to process_variables
                cls.process_variables += [(v, voc)]

                # Add the tuple (v, voc) to the process-type_variables
                # and (process, owning_class) to process-type_variables
                if isinstance(process, ODE):
                    cls.ODE_variables += [(v, voc)]
                elif isinstance(process, Explicit):
                    cls.explicit_variables += [(v, voc)]
                elif isinstance(process, Step):
                    cls.step_variables += [(v, voc)]
                elif isinstance(process, Event):
                    cls.event_variables += [(v, voc)]

        cls.__configured = True
        print("...done")


class ConfigureError(Exception):
    """Define Error."""

    pass
