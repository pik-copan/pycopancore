"""base component's Model component mixin class and essential framework logics.

This class is the Model component mixin of the base model component and also
owns the configure method. This method is central to the framework since it
fuses together the used classes and puts information about process types and
variables in special list to be accessed by the runner.
"""

# TODO: for clarity, move framework logics into separate class this class
# inherits from

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# only used in this component, not in others:
from pycopancore.model_components import abstract
from pycopancore import Variable, ODE, Explicit, Step, Event
from pycopancore.private import \
    _AbstractEntityMixin, _AbstractProcessTaxonMixin
import inspect

#
#  Define class Model
#


class ModelLogics (object):
    """Model logics class.

    Provide the configure method.
    The configure method has a very central role in the COPAN:core framework,
    it is called before letting run a model. It then searches which model class
    is used from the model module. It will then go through all components
    listed there and collect all variables and processes of said components.
    """

    _configured = False

    def __init__(self):
        if not self.__class__._configured:
            self.configure(self.__class__)

    @classmethod
    def configure(cls, mc, reconfigure=False, **kwargs):
        """Configure the model.

        This classmethod configures the chosen mixin model of the 'models'
        package by allocating all required variables and processes to
        designated
        lists.

        Parameter
        ---------
        mc : class
            The model class which the configure method is configuring.
        reconfigure : bool
            Flag that indicates if the model should be reconfigured
        """
        if mc._configured and not reconfigure:
            raise ConfigureError("This model is already configured. "
                                 "Use optional argument 'reconfigure'")

        mc.variables = []  # save in pairs: (variable, owning_class)
        mc.processes = []  # save in pairs: (process, owning_class)

        mc.variables_dict = {}

        mc.process_variables = []

        mc.ODE_variables = []
        mc.explicit_variables = []
        mc.step_variables = []
        mc.event_variables = []

        mc.ODE_processes = []
        mc.explicit_processes = []
        mc.step_processes = []
        mc.event_processes = []

        print("\nConfiguring model", mc.name, "(", mc, ") ...")
        print("Analysing model structure...")

        # Construction of a list for the subsequent for-loop. It contains all
        # model mixins the model component inherits from. Only model mixins
        # that inherit from 'abstract.model' are considered. The abstract model
        # itself is excluded as well as the model component:
        parents = list(inspect.getmro(mc))[1:]
        mc.components = [c for c in parents
                         if c is not abstract.Model
                         and abstract.Model in inspect.getmro(c)
                         ]
        print('\nComponents:', mc.components)

        # The for-loop goes through all model mixins as outlined above:
        for c in mc.components:
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
                    if v in mc.variables_dict.values():
                        print("            already registered by another "
                              "component")
                        assert v._codename == k, ('with Codename', k)
                    # check if same codename was already registered if not,
                    # same assertion error as above:
                    if k in mc.variables_dict.keys():
                        print("            already registered by another "
                              "component")
                        assert mc.variables_dict[k] == v, \
                            'Codename already in use by another variable'
                    v._codename = k
                    mc.variables_dict[k] = v

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
                    if v in mc.variables_dict.values():
                        print("          already registered by another "
                              "component")
                        assert v._codename == k, ('with Codename', k)
                    if k in mc.variables_dict.keys():
                        print("          already registered by another "
                              "component")
                        assert mc.variables_dict[k] == v, \
                            'Codename already in use by another variable'
                    v._codename = k
                    mc.variables_dict[k] = v

                for p in pt.processes:
                    print("        Process:", p)

        # Now analyse by entity type and process taxon in order to find correct
        # owning classes:
        print('\nEntity types:', mc.entity_types)
        print('Process taxa:', mc.process_taxa)
        for owning_class in mc.entity_types + mc.process_taxa:
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
                    if (v, owning_class) not in mc.variables:
                        print("        Variable:", v)
                        mc.variables.append((v, owning_class))
                for p in mixin.processes:
                    p.owning_classes.append(owning_class)
                    if (p, owning_class) not in mc.processes:
                        print("        Process:", p)
                        mc.processes.append((p, owning_class))

        for (process, owning_class) in mc.processes:
            if isinstance(process, ODE):
                mc.ODE_processes += [(process, owning_class)]
            elif isinstance(process, Explicit):
                mc.explicit_processes += [(process, owning_class)]
            elif isinstance(process, Step):
                mc.step_processes += [(process, owning_class)]
            elif isinstance(process, Event):
                mc.event_processes += [(process, owning_class)]
            else:
                print('process-type of', process, 'not specified')
                print(process.__class__.__name__)
                print(object.__str__(process))
            for v in process.variables:
                # Find the tuple (var,owc) in cls.variables with var == v
                # to get the owning class of the variable, not necessarily
                # the owning class of the process.
                for (var, owc) in mc.variables:
                    if var == v:
                        voc = owc
                # Add the tuple (v, voc) to process_variables
                mc.process_variables += [(v, voc)]

                # Add the tuple (v, voc) to the process-type_variables
                # and (process, owning_class) to process-type_variables
                if isinstance(process, ODE):
                    mc.ODE_variables += [(v, voc)]
                elif isinstance(process, Explicit):
                    mc.explicit_variables += [(v, voc)]
                elif isinstance(process, Step):
                    mc.step_variables += [(v, voc)]
                elif isinstance(process, Event):
                    mc.event_variables += [(v, voc)]

        mc._configured = True
        print("...done")

    def convert_to_standard_units(self):
        """Replace all variable values of type DimensionalQuantity to float.

        Using the standard unit.
        """
        for var in self.variables:
            var.convert_to_standard_units()


class ConfigureError(Exception):
    """Define Error."""

    pass
