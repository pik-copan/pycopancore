Software implementation
=======================

NEW: Structure as developed in last week of October 2016:
---------------------------------------------------------

Note: the suggested programming concepts are
*underlined*
in the text below.

Starting points and goals
~~~~~~~~~~~~~~~~~~~~~~~~~

*   Programming language is
    *Python*
    (maybe CPython)



*   Need suitable modularization to...

    *   clearly represent data model (entities with attributes, processes with parameters, ...)



    *   support easy division of labour (framework development, model component development, model composition, model application and analysis)





*   Ease of...

    *   Implementation. In particular, is shall be possible to…

        *   code simple formulae and equations without the need to write python methods, e.g. by using straightforward symbolic expressions





    *   Documentation, testing



    *   Rollout, installation, installation testing



    *   Application, code readability






I will now describe a
*data model*
, a
*package structure*
and some
*coding details*
that try to realize this based on the existing code and prototypes discussed last week.

Data model
~~~~~~~~~~

*   The real world consists of entities and processes:

    *   **Entities**
        * *
        (physical or social “things that are”) are represented by python
        *objects*
        .

        *   Each entity has an
            **entity**
            ** **
            **type**
            represented by a python
            *class*
            . The framework prescribes at least the following four types (but model components may add further entity types if that seems necessary):

            *   *Individual*



            *   *Cell*



            *   *Society*



            *   *World *





        *   Variable or invariable but heterogeneous
            **properties**
            of entities are represented by
            **model variables**
            which in turn are represented by python
            *class attributes*
            (i.e. attributes belonging to a whole class instead of an object that has this class as its type). Since such a class attribute represents the variable itself (rather than its value at some point in time – see below for that!) and shall be usable in symbolic expressions and as keys of dictionaries, it is itself an instance of a specific python
            *class “Variable”*
            that is derived from
            *sympy.Symbol*
            . and is potentially enriched so that it can hold additional
            *metadata*
            such as the represented model variable’s label, mathematical symbol, description text, data type (integer, real number, vector, matrix, graph, …), range of possible values, default initial value, etc.
            An example specification and usage of two variables for societies could read

            *   population = Variable(“domestic human population”)



            *   production = Variable(“domestic economic production”)



            *   (in a formula:)
                …
                Society.production / Society.population
                ...



            *   (as a key in a dictionary of statistical results after a simulation):
                …
                results.mean[Society.production]
                …





        *   In turn, each model variable must be assigned to an entity type (if in doubt, it can be assigned to the entity type “World”).



        *   The
            **value**
            that a model variable takes for a specific object (e.g. for a certain person) at a certain point in time is represented by a python
            *object attribute*
            of the
            *same name*
            as the class attribute representing the variable itself, and of a python type that corresponds to the variable’s data type (int, float, numpy.ndarray, igraph.Graph, etc.). An example usage could read (where
            *soc*
            is a specific object of type Society):

            *   (in an object method of class Society representing a war event:)
                self.population *= 1 – casualtyrate



            *   (in an object method of class Individual representing an imitation event, where
                j
                is another individual:)
                sigmoid(j.society.wellbeing - self.society.wellbeing)







    *   **Processes**
        * *
        (“things that happen”)

        *   A process’
            **type**
            and
            **metadata**
            are represented by a
            *python object*
            of type “Process”, belonging to one of the following subclasses of “Process”:

            *   *ODE*
                (ordinary differential equation)



            *   *Explicit*
                (an explicit equation having one or several variables as its LHS)



            *   *Implicit*
                (an implicit equation between several variables, e.g. representing a constraint or an economic equilibrium between prices)



            *   *ImmediateStep*
                or
                *DelayedStep*
                (representing a discontinuous change caused at a discrete time point and taking effect either immediately or right before the next occurrence of the same step)



            *   *InterpolatedStep*
                (representing a discretization of a continuous-time real-world process and a method for interpolating intermediate values)



            *   *Event*
                (with some subclasses such as
                *FixedRateEvent*
                ,
                *ScheduledEvent*
                ,
                *VariableRateEvent*
                )





        *   Most “Process” objects are “owned” by either the entity type that “causes” the process (e.g. one individual imitates another) or that has the process as part of its “internal dynamics” (e.g. vegetation growth on a cell).



        *   For some processes, this assignment will be ambiguous and it will rather make sense to consider them as processes happening “between” entities of the same or maybe of several types. Such a process will then instead be “owned” by a subclass of the special python
            *class “Dynamics”*
            . In view of the taxonomy of processes, it makes sense to at least provide three subclasses: “NAT”, “MET”, “CUL”. Processes originating in metabolism but causing a change in nature could then be owned by “NAT”, or one provides nine subclasses “NAT_NAT”, “NAT_MET”, “NAT_CUL”, …, collecting processes originating in one realm and affecting another.



        *   The “
            **ownership**
            ” of a process is represented via a
            *class attribute “proclist”*
            of the entity or dynamics class owning the process. This could read:

            *   (in Cell:)
                proclist = [ ODE(“vegetation growth”,...), Event(“drought”,...), ... ]




            *   (in CUL_MET:)
                proclist = [ Step(“voting on harvesting rate”, ...), ... ]





        *   The metadata and
            **logics**
            of a process (label, affected variables, rate of occurrence, RHS of equation, other things depending on process type...) are represented by attributes of the Process class that are listed as arguments when the Process object is generated as part of a proclist specification. Many of these attributes (e.g. those specifying the RHS of an equation or the occurrence rate of an event) can either contain a
            *symbolic expression*
            or the reference to an
            *object method *
            (that typically resides in the same class that owns the process). Since many processes will affect more than one variable, all these object methods are expected to return lists of values. It might be even more logical if the object methods directly store the derivative in the variable instead of returning a value. E.g., these two variants could read:

            *   (in Cell:)
                def do_drought(self, t):

                return [0.1 * self.vegetation]
                ...
                def do_growth(self, t):

                self.d_vegetation = rate \

                * (1 - self.vegetation/capacity) \

                * self.vegetation
                ...
                proclist = [

                ODE(“growth1”, [Cell.vegetation],

                [rate * (1 - Cell.vegetation/capacity)

                * Cell.vegetation]),

                ODE(“growth2”, [Cell.vegetation],

                do_growth),

                Event(“drought”, [Cell.vegetation],

                0.1, Cell.do_drought),

                ... ]










*   The model portfolio consists of model components and (composed) models:

    *   **Model components**
        * *

        *   A model component is a logically interdependent collection of entity variables, processes, and model parameters that represent a reusable building block for individual models could be contributed by someone else than the core framework development team or the final model user. E.g., a model component could represent

            *   environmental opinion formation



            *   bottom-up environmental policy making



            *   international coalition formation



            *   local resource dynamics, exploitation and resulting pollution



            *   …





        *   Since it must be possible to flexibly combine several model components each of which contribute attributes to the same entity and dynamics types, we use the python mechanism of
            *multiple inheritance via mixin classes*
            . Each model component hence consists of the following classes:

            *   (Up to) four
                *entity mixin classes*
                that will be mixed into the entity classes “Individual”, “Cell”, “Society”, and “World” and that contain the model component specific variables, processes, and methods for these entity types. E.g. the EXPLOIT model component would contain the mixin class “EXPLOIT_Individual” specifying the opinion imitation and network adaptation processes, and the mixin class “EXPLOIT_Society” specifying the metabolic consequences of these opinions on the societal level.



            *   (Up to) three (resp. nine)
                *dynamics mixin classes*
                , to be mixed into the dynamics classes “NAT”, “CUL”, “MET”, …. E.g. a trade model component could contain a mixin class “Trade_MET” specifying international trade processes.



            *   A class implementing the abstract class “AbstractModelComponent”, named with the name of the component, that contains as class attributes a number of Parameter objects (see below) and metadata such as:

                *   name, description, ...



                *   individual_mixin, cell_mixin, ... , NAT_mixin, … (references to the mixin classes provided by the model component)





            *   Since the above coding logic will often require that attributes of one mixin class be referenced by another mixin class
                *and vice versa*
                (e.g., when a process in EXPLOITIndividual references EXPLOITCell.resource_stock and a process in EXPLOITCell references EXPLOITIndividual.effort_level), one would run into an unresolvable dilemma if these classes live in different modules (files) that have to import each other (since cyclic imports are impossible). At the moment, it seems the natural solution to this is to actually define two classes for each mixin, first a “mixin interface” class defining all Variables and Parameters of the mixin (e.g. named with a leading underscore, e.g. _EXPLOITCell), and then deriving from it the actual mixin class. These can then either defined in separate files of which the second kind import the first, or all these classes are assembled in only one file per model component. In either case, it seems that a suitable package structure should lump everything belonging to one model component into one subpackage with an _init__.py module that imports all ingredients of the component into just one namespace per component, rather than lumping all individual mixin classes into one folder and then having to use lengthy import linesl (see suggested structure variants below). The model composer mainly needs to know what model components are available, and not which mixin classes, since she cannot mix the latter independently of mixing the components anyway.





        *   For each
            **parameter,**
            the model component class contains a
            *class attribute*
            of type “Parameter” (holding metadata similar to the type “Variable” described above) and an
            *object attribute*
            of the same name holding the parameter’s value in individual simulation runs.



        *   The framework provides a
            *“BaseModelComponent”*
            containing the mixin classes
            *“BaseIndividual”*
            , “BaseSociety”, …, “BaseNAT”, … that contain those entity variables (and potentially also some processes) that all models must contain (“the interface”).





    *   **Models**

        *   A model combines BaseModelComponent with any number of additional model components in a certain order that influences which components are allowed to
            *override*
            some processes also specified by other used components. To do this, a model is represented by a
            *python module*
            that…

            *   imports the model components it wants to use



            *   composes the entity type and dynamics classes “Individual”, “Society”, …, “NAT”, … in a suitable order from the mixin classes, by specifying lines of the form

                *   class Individual (EXPLOIT_Individual,

                    BaseIndividual): pass





            *   composes a
                *class “Model”*
                from “BaseModel” (containing basic simulation logics like a “run” method) and the used component classes, potentially providing further methods related to the intended model usage (e.g. some analysis or plotting methods):

                *   class Model (EXPLOIT, BaseModel):

                    …











*   **Applications**
    are represented via
    *scripts*
    *. *
    In particular, a script…

    *   imports a model



    *   configures it by calling the class method “Model.configure” (provided by BaseModel), which uses the inspect package to analyse the composed model, compose lists of variables, parameters, and processes, and store these lists back into the composite classes



    *   generate entities by calling their generators, which will use the above lists to instantiate all variables as instance attributes that will hold values (see above)



    *   instantiate the model by calling its generator, which will similarly instantiate all parameters as instance attributes that will hold values



    *   instantiate a suitable
        *Runner class*
        (e.g. ScipyOdeintRunner) that will prepare the model’s simulation with some combination of solvers



    *   call the runner’s
        *run()*
        method to perform one or more simulations





Package structure
~~~~~~~~~~~~~~~~~

Based on existing structure:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

copancore

individual_mixins

_base_individual.py

_EXPLOIT_individual.py
_voting_individual.py

base_individual.py

EXPLOIT_individual.py
voting_individual.py

…

cell_mixins

_base_cell.py

_logisticresource_cell.py

base_cell.py

logisticresource_cell.py

...

society_mixins

_base_society.py

_coalitionformation_society.py

base_society.py

coalitionformation_society.py

…

world_mixins

_base_world.py

_COPprocess_world.py

base_world.py

COPprocess_world.py

...

NAT_mixins

_base_NAT.py

base_NAT.py

…

MET_mixins

…

CUL_mixins

…

...

model_components

abstract_model_component.py

_COPprocess.py

_EXPLOIT.py

COPprocess.py

EXPLOIT.py

…

models

base_model.py

EXPLOIT_only.py

…

studies

template_script.py

Wiedermann2015.py

...

Alternative based on model_components:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

copancore

model_components

abstract_model_component.py

COPprocess

__init__.py

_COPprocess.py

_COPprocess_world.py

COPprocess.py

COPprocess_world.py

EXPLOIT

__init__.py

_EXPLOIT.py

_EXPLOIT_individual.py
_EXPLOIT_cell.py
EXPLOIT.py

EXPLOIT_individual.py
EXPLOIT_cell.py
…

models

base_model.py

EXPLOIT_only.py

…

studies

template_script.py

Wiedermann2015.py

...









Old thoughts:
-------------

After deciding for a suitable modularity structure, we should decide which programming language and framework is the most suitable, based on the candidate framework’s language features, numerical performance in large simulations, and our familiarity with it or the effort to learn it.
*Candidates*
are:

*   Python, Numpy, Scipy, Cython
    etc
    .



*   Matlab (with additional “Matlab toolboxes”?)



*   Mathematica and Wolfram SystemModeler (uses Modelica language)



*   Netlogo



*   Repast (http://repast.sourceforge.net/)



*   GAMS



*   C++ / C#



*   ...




Ideally, the framework should

*   Object-oriented



*   Support doc-tests, unit tests, test driven development etc.



Documentation automatically generated from in-code documentation (doxygen, sphinx, ...)

*   be easy to learn for newbees



*   provide fast enough solvers for combinations of deterministic differential equations and algebraic equations that can interact with individual stochastic events and
    maybe even allow for adding noise
    (Frank Hellmann is developing something along this line for Python)



*   support easy modularization via the definition of abstract interface classes and overriding implementation classes for the model components



*   support variables with physical units



*   be parallelizable on PIK’s cluster



*   be in terms of design suitable for scaling up to very large networks in perspective (100 millions of nodes or
    more
    )



*   allow for easy documentation (e.g. inline with tags from which HTML can be generated as in classdoc, epydoc or sphinx)



*   be compatible to PIK’s SimEnv framework for conducting and analysing numerical experiments



*   ...



*   probably
    *not*
    required: sophisticated (e.g. intertemporal) optimization as in GAMS


