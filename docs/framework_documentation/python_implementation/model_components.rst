Model component subpackages
===========================

Interface module
----------------

The interface module defines the attributes of all entity-types and process taxons contributed by this component.
Each attribute is an instance of ``Variable``, 
either one imported from the master data model or another component, or a new instance.

Basic structure of ``interface.py``, using only attributes from the master data model:

::

   from pycopancore import EntityType, ProcessTaxon
   from pycopancore import master_data_model as M
   
   class Cell (EntityType):
      <variable name> = M.Cell.<same variable name>
      <other variable name> = M.Cell.<same other variable name>
      <some alternative variable name> = M.Cell.<some original variable name>
      ...
      
   class Society (EntityType):
      ...
      
   class Nature (ProcessTaxon):
      ...
      
If some needed attribute is not defined in the master data model but in another component,
it can be imported from the other component's *interface* (not implementation!) module as follows:

::

   from pycopancore import EntityType, ProcessTaxon
   from pycopancore import master_data_model as M
   
   import pycopancore.model_components.<other component name>.interface as O
   
   class Cell (EntityType):
      <variable name> = O.Cell.<same variable name>
      <some alternative variable name> = O.Cell.<some original variable name>
      ...
      
      
Implementation class modules
----------------------------

For each entity-type used in the component, 
an implementation class module defines 
an implementation class derived from the corresponding interface class.

It specifies the metadata of the processes the component contributes to this entity-type
by listing instances of suitable process type classes (``ODE``, ``Event``, ...)
in the implementation class' ``processes`` attribute.

It defines these processes' logics by defining suitable instance methods 
which are referenced in the above process metadata or by specifying symbolic expressions in the metadata.

Basic structure of ``cell.py`` (similar for other entity-types):

::

   from pycopancore import ODE, Explicit, Event, ...
   
   import .interface
   
   class Cell (interface.Cell):

      processes = [
         ODE(..., rhs = <method name>),
         ODE(..., rhs = <some (list of) symbolic expression(s)>),
         Explicit(..., zero = <another method name>),
         Explicit(..., zero = <another (list of) symbolic expression(s)>),
         Event(..., rate = <still another symbolic expression>, action = <still another method name>),
         ...
      ]
      
      def <method name> (self, ...):
         ...
         return <right-hand side>

      def <another method name> (self, ...):
         ...
         return <what should be zero>

      def <still another method name> (self, ...):
         ...
         
      ...
      
TODO...
     