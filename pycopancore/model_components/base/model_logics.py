"""base component's Model component mixin class and essential framework logics.

This class is the Model component mixin of the base model component and also
owns the configure method. This method is central to the framework since it
fuses together the used classes and puts information about process types and
variables in special list to be accessed by the runner.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import abstract
from ... import Variable, ReferenceVariable, SetVariable, \
                ODE, Explicit, Step, Event, OrderedSet
from ...private import _AbstractProcess

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
    """whether model was configured already"""

    components = None
    """ordered set of model components in method resolution order"""

    variables = None
    """ordered set of Variables occurring in the model"""
    explicit_targets = None
    """ordered set of Variables controlled by processes of type Explicit"""
    step_variables = None
    """ordered set of Variables changed by processes of type Step"""
    event_variables = None
    """ordered set of Variables changed by processes of type Event"""
    ODE_targets = None
    """ordered set of Variables or _AttributeReferences changed by processes
    of type ODE"""
    process_targets = None
    """ordered set of Variables or _AttributeReferences changed by any
    process"""

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

    mixin2composite = None
    """dict mapping mixins to derived composite classes"""

    def __init__(self):
        """Upon initialization of model: configure if not yet configured."""
        if not self.__class__._configured:
            self.configure()

    @classmethod
    def configure(cls, reconfigure=False, **kwargs):
        """Configure the model.

        This classmethod configures the model by analysing the model's and all
        its entity types' and process taxa's class inheritance structure to
        find all mixin classes (implementation and interface), analyse them
        to compile and output lists (actually OrderedSets) of variables and
        processes.

        Parameter
        ---------
        reconfigure : bool
            Flag that indicates if the model should be reconfigured even if
            it is already configured
        """
        if cls._configured and not reconfigure:
            raise ConfigureError("This model is already configured. "
                                 "Use optional argument 'reconfigure'")

        cls.variables = OrderedSet()  # ordered set (special type of list) of Variables

        # lists of process 'targets' by type (= Variables or _DottedReferences):
        cls.ODE_targets = OrderedSet()
        cls.explicit_targets = OrderedSet()
        cls.step_variables = OrderedSet()
        cls.event_variables = OrderedSet()
        cls.process_targets = OrderedSet()

        # lists of processes:
        cls.processes = OrderedSet()  # all processes
        # ...by type:
        cls.ODE_processes = OrderedSet()
        cls.explicit_processes = OrderedSet()
        cls.step_processes = OrderedSet()
        cls.event_processes = OrderedSet()

        # dict mapping mixin classes to corresponding composite class:
        cls.mixin2composite = {}

        # start the extensive log output:
        print("\nConfiguring model", cls.name, "(", cls, ") ...")
        print("Analysing model structure...\n")

        variable_pool = OrderedSet()  # temp. list of all variables found

        # Find all model components in this model.
        # These are among the ancestor classes of the composed model.
        # For each used component, there are two ancestor classes, one is the
        # interface class, the other is the corresponding implementation class
        # (typically both are named "Model" since they are the mixin classes
        # for the composite class of the name "Model")
        cls.components = OrderedSet(
                [c for c in list(inspect.getmro(cls))
                 # exclude things that are definitely not model components:
                 if c not in (object, abstract.Model, ModelLogics)
                 # exclude interface classes (which have an attribute "name"):
                 and not "name" in c.__dict__  # TODO: use a cleaner method than this to distinguish interfaces from implementation?
                 ])
        # iterate through all model components:
        for component in cls.components:
            component_interface = component.__bases__[0]  # the first base class of an impl. cl. is its interface
            print("Model component ", component_interface.name, "(", component,
                  ")...")
            # iterate through all entity-type and process taxon mixins this
            # model components defines:
            for mixin in component.entity_types + component.process_taxa:
                mixin_interface = mixin.__bases__[0]  # interface of this mixin
                if mixin in component.entity_types:
                    print("    Entity-type ", mixin)
                else:
                    print("    Process taxon ", mixin)
                # find and register all Variables defined directly in this
                # mixin's interface:
                for (k, v) in mixin_interface.__dict__.items():  # k is the attribute's name (here the variable name), v the attribute's value (here the Variable object)
                    if isinstance(v, Variable):
                        if v not in variable_pool:  # we found a new one
                            assert v.codename is None  # since Variables are assigned their codename attribute only here
                            # store codename in Variable object for convenience:
                            v.codename = k
                            variable_pool.add(v)
                            print("        Variable ", v)
                        else:  # same Var. has been registered in another component or mixin already:
                            print("        Variable ", v)
                            # make sure all mixins use the same codename
                            # for this Var.:
                            assert v.codename == k, \
                                "Variable was already registered by a " \
                                "different component or mixin using a " \
                                "different codename."
                # find and register all processes defined directly in this
                # mixin's "process" attribute:
                for p in mixin.processes:
                    assert isinstance(p, _AbstractProcess), \
                        "The 'processes' attribute of an implementation " \
                        "class must only contain process objects."
                    print("        Process ", p)
                    # other than variables, the same process cannot be named
                    # by more than one mixin:
                    assert p not in cls.processes, \
                        "Process was already registered by a different " \
                        "component or mixin."
                    cls.processes.add(p)

        # now iterate again through all composed entity-types and process taxa
        # and output all found variables:
        print("\nVariables:")
        for composed_class in cls.entity_types + cls.process_taxa:
            if composed_class in cls.entity_types:
                print("  Entity-type ", composed_class)
            else:
                print("  Process taxon ", composed_class)
            # find all parent classes and register in dict mixin2composite:
            parents = OrderedSet(list(inspect.getmro(composed_class)))
            for mixin in parents:
                cls.mixin2composite[mixin] = composed_class
            # iterate through all Variables and set their owning_class
            # to the correct composite class (rather than to the mixin class):
            variables = OrderedSet([(k, v) for c in parents
                                    for (k, v) in c.__dict__.items()
                                    if isinstance(v, Variable)])
            for (k, v) in variables:
                if isinstance(v, Variable):
                    print("    Variable ", v)
                    assert v in variable_pool, \
                        "Variable '{v!r}' was not defined in any component interface!".format(
                            **locals())
                    assert v.codename == k, \
                        "Variable '{v!r}' was registered under a different codename".format(**locals())
                    assert v.owning_class is None  # since it is only set here!
                    cls.variables.add(v)
                    v.owning_class = composed_class

        print("\nProcesses:")
        # iterate again through all composed entity-types and process taxa
        # to output all processes and check process targets:
        for composed_class in cls.entity_types + cls.process_taxa:
            if composed_class in cls.entity_types:
                print("  Entity-type ", composed_class)
            else:
                print("  Process taxon ", composed_class)
            parents = OrderedSet(list(inspect.getmro(composed_class)))
            for c in parents:
                if "processes" in c.__dict__ and c.processes is not None:  # since some implementation classes may not define any processes
                    for p in c.processes:
                        print("    Process ", p)
                        # all processes found here should have been seen
                        # already above, so we verify this:
                        assert p in cls.processes, \
                            "Process was not listed in any implementation " \
                            "class!"
                        assert p.owning_class is None  # since it is only set here!
                        p.owning_class = composed_class
                        # depending on process type, register in correct list
                        # and analyse process targets:
                        if isinstance(p, ODE):
                            cls.ODE_processes.add(p)
                            for target in p.targets:
                                if isinstance(target, Variable):
                                    # make sure the named process target
                                    # actually belongs to the same entity type
                                    # or taxon as the process:
                                    assert target.owning_class == \
                                           composed_class, \
                                           "ODE target Variable owned by " \
                                           "different entity-type/taxon! " \
                                           "(maybe try accessing it via a " \
                                           "ReferenceVariable)"
                                else:  # target is a _DotConstruct
                                    # make sure the possibly lengthy attribute
                                    # reference named as the process target
                                    # actually starts at the entity type
                                    # or taxon the process belongs to:
                                    assert target.owning_class == \
                                        composed_class, \
                                        "ODE target attribute reference " \
                                        "starts at a wrong " \
                                        "entity-type/taxon" \
                                        + str(target) \
                                        + str(target.owning_class) \
                                        + str(composed_class)
                            cls.ODE_targets += p.targets
                            cls.process_targets += p.targets
                        elif isinstance(p, Explicit):
                            # TODO: determine dependency structure among
                            # variable to set the right order of execution
                            # of explicit processes!
                            cls.explicit_processes.add(p)
                            for target in p.targets:
                                if isinstance(target, Variable):
                                    assert target.owning_class == \
                                        composed_class, \
                                        "Explicit target Variable owned " \
                                        "by different entity-type/taxon! " \
                                        "(maybe try accessing it via a " \
                                        "ReferenceVariable)"
                                else:  # it's a _DotConstruct
                                    assert target.owning_class == \
                                        composed_class, \
                                        "Explicit target attribute " \
                                        "reference starts at a wrong " \
                                        "entity-type/taxon:"
                            cls.explicit_targets += p.targets
                            cls.process_targets += p.targets
                        elif isinstance(p, Step):
                            cls.step_processes.add(p)
                            # TODO: do similar checks as for ODE targets!
                            cls.step_variables += p.variables
                            cls.process_targets += p.variables
                        elif isinstance(p, Event):
                            cls.event_processes.add(p)
                            # TODO: do similar checks as for ODE targets!
                            cls.event_variables += p.variables
                            cls.process_targets += p.variables
                        else:
                            raise Exception("unsupported process type")

        # replace refs to mixins by refs to corresponding composite class
        # in all Reference/SetVariables where possible.
        # This is necessary since (i) at the time the Reference/SetVariable is
        # defined, the composite class is not known, so the referenced type
        # is given by a mixin class, but (ii) when running the model, the
        # references needs to point to the correct composite class:
        for v in variable_pool:
            if isinstance(v, (ReferenceVariable, SetVariable)):
                v.type = cls.mixin2composite.get(v.type, v.type)

        cls._configured = True

        print("\nTargets affected by some process:", cls.process_targets)
        print("\n(End of model configuration)")

    def convert_to_standard_units(self):
        """Replace all variable values of type DimensionalQuantity to float.

        Using the standard unit. This is mainly done for performance reasons.
        """
        for v in self.variables:
            v.convert_to_standard_units()


class ConfigureError(Exception):
    """Define Error."""

    pass
