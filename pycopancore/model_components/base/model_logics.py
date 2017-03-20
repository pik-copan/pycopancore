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
from .. import abstract
from ... import Variable, ODE, Explicit, Step, Event, OrderedSet
from ...private import _AbstractEntityMixin, _AbstractProcessTaxonMixin

import inspect


class ModelLogics (object):
    """Model logics class.

    Provide the configure method.
    The configure method has a very central role in the COPAN:core framework,
    it is called before letting run a model. It then searches which model class
    is used from the model module. It will then go through all components
    listed there and collect all variables and processes of said components.
    """

    _configured = False

    components = None
    """ordered set of model components in method resolution order"""

    variables = None
    """ordered set of Variables"""
    explicit_variables = None
    """ordered set of Variables controlled by processes of type Explicit"""
    step_variables = None
    """ordered set of Variables changed by processes of type Step"""
    event_variables = None
    """ordered set of Variables changed by processes of type Event"""
    ODE_targets = None
    """ordered set of Variables or _AttributeReferences changed by processes of type ODE"""
    process_targets = None
    """ordered set of Variables or _AttributeReferences changed by any process"""

    processes = None
    """ordered set of processes"""
    ODE_processes = None
    """ordered set of processes of type ODE"""
    explicit_processes = None
    """ordered set of processes of type Explicit"""
    step_processes = None
    """ordered set of processes of type Step"""
    event_processes = None
    """ordered set of processes of type Event"""

    def __init__(self):
        if not self.__class__._configured:
            self.configure()

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
        if cls._configured and not reconfigure:
            raise ConfigureError("This model is already configured. "
                                 "Use optional argument 'reconfigure'")

        cls.variables = OrderedSet()  # set of Variables (no longer of pairs!)
        cls.explicit_variables = OrderedSet()
        cls.step_variables = OrderedSet()
        cls.event_variables = OrderedSet()
        cls.ODE_targets = OrderedSet()
        cls.process_targets = OrderedSet()  # Variables or _AttributeReferences

        cls.processes = OrderedSet()  # set of Processes (no longer of pairs!)
        cls.ODE_processes = OrderedSet()
        cls.explicit_processes = OrderedSet()
        cls.step_processes = OrderedSet()
        cls.event_processes = OrderedSet()

        print("\nConfiguring model", cls.name, "(", cls, ") ...")
        print("Analysing model structure...")

        variable_pool = OrderedSet()
        # find and iterate through model components:
        cls.components = OrderedSet(
                [c for c in list(inspect.getmro(cls))  # exclude self
                 if c not in (object, abstract.Model, ModelLogics)
                 and not "name" in c.__dict__  # exclude interface classes (which have an attribute "name")
                 ])
        for component in cls.components:
            component_interface = component.__bases__[0]
            print("Model component ", component_interface.name, "(", component, ")...")
            # iterate through all entity-type and process taxon mixins this model components defines:
            for mixin in component.entity_types + component.process_taxa:
                mixin_interface = mixin.__bases__[0]
                if mixin in component.entity_types:
                    print("    Entity-type ", mixin)
                else:
                    print("    Process taxon ", mixin)
                # find and register all Variables defined directly in this mixin's interface:
                for (k, v) in mixin_interface.__dict__.items():
                    if isinstance(v, Variable):
                        if v not in variable_pool:
                            assert v.codename is None
                            v.codename = k
                            variable_pool.add(v)
                            print("        Variable ", v)
                        else:
                            print("        Variable ", v)
                            assert v.codename == k, \
                                "Variable was already registered by a different component using a different codename"
                # find and register all processes defined directly in this mixin:
                for p in mixin.processes:
                    print("        Process ", p)
                    assert p not in cls.processes, \
                            "Process was already registered by a different component"
                    cls.processes.add(p)

        # now iterate through all composed entity-types and process taxa:
        for composed_class in cls.entity_types + cls.process_taxa:
            if composed_class in cls.entity_types:
                print("Entity-type ", composed_class)
            else:
                print("Process taxon ", composed_class)
            # find all parent classes:
            parents = OrderedSet(list(inspect.getmro(composed_class)))
            # iterate through all Variables and set their owning_class:
            vars = OrderedSet([(k, v) for c in parents
                               for (k, v) in c.__dict__.items()
                               if isinstance(v, Variable)])
            for (k, v) in vars:
                if isinstance(v, Variable):
                    print("    Variable ", v)
                    assert v in variable_pool, \
                        "Variable was not defined in any component interface!"
                    assert v.codename == k, \
                        "Variable was registered under a different codename"
                    assert v.owning_class is None
                    cls.variables.add(v)
                    v.owning_class = composed_class
            for c in parents:
                if "processes" in c.__dict__ and c.processes is not None:
                    for p in c.processes:
                        print("    Process ", p)
                        assert p in cls.processes, \
                            "Process was not listed in any implementation class!"
                        p.owning_class = composed_class
                        if isinstance(p, ODE):
                            cls.ODE_processes.add(p)
                            for target in p.targets:
                                if isinstance(target, Variable):
                                    assert target.owning_class == composed_class, \
                                        "ODE target Variable owned by different entity-type/taxon! (maybe try accessing it via a ReferenceVariable)"
                                else:  # it's an _AttributeReference
                                    assert target.reference_variable.owning_class == composed_class, \
                                        "ODE target attribute reference starts at a wrong entity-type/taxon"
                            cls.ODE_targets += p.targets
                            cls.process_targets += p.targets
                        elif isinstance(p, Explicit):
                            cls.explicit_processes.add(p)
                            cls.explicit_variables += p.variables
                            cls.process_targets += p.variables
                        elif isinstance(p, Step):
                            cls.step_processes.add(p)
                            cls.step_variables += p.variables
                            cls.process_targets += p.variables
                        elif isinstance(p, Event):
                            cls.event_processes.add(p)
                            cls.event_variables += p.variables
                            cls.process_targets += p.variables
                        else:
                            raise Exception("unsupported process type")

        cls._configured = True
        print("...done")

    def convert_to_standard_units(self):
        """Replace all variable values of type DimensionalQuantity to float.

        Using the standard unit.
        """
        for v in self.variables:
            v.convert_to_standard_units()


class ConfigureError(Exception):
    """Define Error."""

    pass
