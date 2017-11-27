Model component subpackages
===========================

This section describes the package implementing a single model component.
Each such package is a subpackage of ``pycopancore.model_components``.


Subpackage structure
--------------------

A component subpackage contains one interface module, one model module,
and one implementation class module for each entity-type and process taxon that the component contributes to:

::

   <component name>
      implementation
        cell.py
        culture.py
        environment.py
        individual.py
        social_metabolism.py
        social system.py
      interface.py
      model.py


Interface module
----------------

The interface module defines the attributes of all entity-types and process taxons contributed by this component.
Each attribute is an instance of the class ``Variable`` 
or one of its subclasses such as ``ReferenceVariable`` (for references to at most one other entity, e.g. ``CEO``)
or ``SetVariable`` (for references to sets of entities, e.g. ``residents``),
either one imported from the master data model or another component, or a new instance.

Basic structure of ``interface.py``, using attributes imported from the data model and self-defined variables:

::

   from pycopancore.master_data_model import C, ...

   class Model:
      name = '<model name>'
      description = '<model description>'
      requires = []
      ...

   class Cell:
      <variable name> = C.<same variable name>
      ...

   class SocialSystem:
      ...

   class Environment:
      ...


Variables from the master data model must be used under the exact same name as they occur there.
In turn, the modeling board must ensure
that variable names in the master data model are reasonably short without losing distinguishability and descriptiveness.

If some needed attribute is not (yet) defined in the master data model
but is already defined in another component that this component necessarily *requires*
(i.e., if the component may not be meaningfully used in any model without the other component),
then the preferred choice is to import the attribute from the other component's *interface* (not implementation!) module as follows:

::

   import pycopancore.model_components.<other component name>.interface as O

   class Cell:
      <variable name> = O.Cell.<same variable name>
      ...

   ...

However, if the import is not possible since the other component's interface itself already imports this component's interface
(either directly or indirectly via a sequence of imports), which would lead to an unallowed import cycle,
then the respective attribute shall not specified in this component's interface at all.
Instead, the implementation classes of this component shall reference the other component's attribute directly
via the *other* component's interface (see below).

Finally, if the needed attribute is not defined in either the master data model nor any components this component requires,
it must be defined (instead of imported) as an instance of the ``Variable`` class, specifying the variable's metadata.

We encourage using variable metadata from established catalogues of variables
such as the `CF Conventions Standard Names`_ for climate-related quantities
or the `World Bank's CETS list`_ of socio-economic indicators wherever possible,
ideally via the ``Variable`` class' subclasses ``CFVariable``, ``CETSVariable``, etc.,
but renaming the variable according to copan\:CORE's naming standards if necessary
(e.g. for a ``CETSVariable`` or for a ``CFVariable`` with too lengthy names).

:: _`CF Conventions Standard Names`: http://cfconventions.org/Data/cf-standard-names/37/build/cf-standard-name-table.html

:: _`World Bank's CETS list`: https://datahelpdesk.worldbank.org/knowledgebase/articles/201175-how-does-the-world-bank-code-its-indicators

Example:

::

   from pycopancore import Variable, ReferenceVariable, SetVariable
   import pycopancore.base.interface as B 
   ...

   class Cell:
      <variable name> = Variable("<label>", <other metadata>...)
      owner = ReferenceVariable("owning firm", type=B.Firm)
      residents = SetVariable("resident individuals", type=B.Individual)
      ...

   ...


Implementation class modules
----------------------------

For each entity-type and process taxon that the component contributes to,
an implementation class module defines the corresponding implementation class.

The latter is derived from the corresponding interface class that was defined in the interface module.

In its ``processes`` attribute, the implementation class specifies
the metadata of all processes the component contributes to this entity-type or process taxon,
by listing instances of suitable process type classes (``ODE``, ``Event``, ...).

It also defines these processes' logics by defining suitable instance methods
which are referenced in the above process metadata,
or by specifying symbolic expressions directly in the metadata.

Finally, an entity-type implementation class (but not a process taxon implementation class)
may override three special instance methods provided by the general base class ``Entity``
that are called upon initialization (e.g. birth or foundation),
"deactivation" (e.g. death, termination, collapse, loosing independence),
and possibly at "reactivation" (e.g., rebirth, regaining independence) of the entity,
usually at initialization and termination of the whole model,
and possibly also as a consequence of certain events belonging to the entity itself or to other entities (e.g. a parent). [#del]_

The basic structure of an implementation class module, here ``cell.py``
(similar for other entity-types and process taxons), is this:

::

   # import used process-types:
   from pycopancore import ODE, Explicit, Event, Step, ...

   # import the interface to be able to derive implementation class from interface class:
   import .interface

   # import base class for basic (de-)activation logics:
   from pycopancore import Entity

   class Cell (interface.Cell):

      # define process logics:

      def <method name> (self, t):
         ...

      def <another method name> (self, t):
         ...

      def <event method name> (self, t):
         ...

      def <step method name> (self, t):
         ...
         return next_t

      # specify process metadata:

      processes = [
         ODE(..., <method name>),
         ODE(..., <some (list of) symbolic expression(s)>),
         Explicit(..., <another method name>),
         Explicit(..., <another (list of) symbolic expression(s)>),
         Event(..., <rate symbolic expression>, <event method name>),
         Step(..., <step method name>),
         ...
      ]


Implementation instance methods
-------------------------------

Implementation instance methods typically do not return variable values but manipulate entity attributes directly.
For an explicit equation, step or event, they overwrite variable attributes, e.g. ``self.welfare = consumption/population``
while for an ordinary differential equation, they *add* to time derivative attributes, e.g.
``self.d_population += birth_flow``.
Only implicit equation methods return a value that the runner tries to make zero,
e.g. ``return supply - demand`` if the equation is "supply = demand".

In case of process taxons, please note that although those classes have only one instance,
the process logics is still implemented via instance methods (i.e., taking ``self`` as first argument)
rather than via class or static methods.
Likewise, the taxon's attribute values are stored in the sole instance's attributes,
while their metadata are stored in the respective class attributes, just as for entities and entity-types.


.. [#del]   Note that upon deactivation, an entity object is *not* deleted but remains in memory
            not only since it may later be reactivated
            but mainly since it remains needed for several operations
            such as accessing its history during a model run's later analysis etc.
