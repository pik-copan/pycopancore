Programming language-independent copan\:CORE software design
============================================================

This section describes the programming language-independent parts of 
how the abstract :doc:`../modeling_framework/index` is realized as computer software.
For the current implementation concept in the Python programming language, see :doc:`../python_implementation/index`.

.. (Later this may switch from Python to Cython!)

TODO:

-  motivate object-oriented approach


Common concepts of object-oriented programming languages
--------------------------------------------------------

-  An **object** is an *instance* of a certain **class**.

-  A **class** is a collection of like objects.
   It is usually named by a common noun in the singular.

-  Objects and classes can have **attributes** and **methods**:

   -  *Object attributes* (aka *instance attributes*) store data about individual objects.
   
   -  *Class attributes* store data (e.g., metadata) about the class itself.
   
   -  *Object methods* (aka *instance methods*) represent the actions an object "can do" or that can be "done to" an object.
   
   -  *Class methods* represent actions that can be done to the class itself.

   An attribute ``x`` or method ``f`` of a class ``A`` or object ``a`` can typically be referred to as 
   ``A.x``, ``A.f``, ``a.x``, ``a.f``, respectively (*dot notation*).

-  A class is often **derived** from one or more *superclasses* (maybe in several levels).
   Their attributes and methods are then **inherited** by the derived class but can also be **overwritten** by subclasses.
   
-  If a class is derived from more than one superclass (*multiple inheritance*)
   which are not meant to be instantiated directly, the latter are often called **mixin classes**.

-  Some classes don't have methods
   or have only *method declarations* that contain no implementation 
   and are meant to be overwritten by an "implementation method" in a derived "implementation subclass". 
   Such classes are typically called "abstract" or "interface" classes, but this terminology is not completely well-defined.
   They are normally not instantiated directly but rather used to derive "implementation" subclasses that are then instantiated.
   There are a number of more ore less complex "design patterns" describing common practices of how this can be used.

-  **Packages** and **Modules** are somehow meaningful collections of classes (and maybe other things) that form a separate *namespace*.
   A class ``A`` in a package or module ``P`` can typically be referred to as ``P.A``.
   Packages and subpackages can typically form a hierarchical structure similarly (and often implemented as) a file folder structure,
   with modules typically representing the deepest level of this hierarchy, similar to files within a folder structure.
   To be able to refer to things from package ``A`` within package ``B``, 
   one typically needs to *import* them from ``A`` to ``B``, and most programming languages forbit cyclical imports.
   A similar need for importing often exists if a class needs access to another class' attributes and methods.


Representing modeling framework concepts by object-oriented concepts
--------------------------------------------------------------------

-  A model's **entity-types** are represented as classes that are derived from a common abstract class called ``Entity`` 
   and are named with the common noun used for the respective type of entity (i.e., ``Cell``, ``Society``, ``Individual``, ...).
  
-  All individual **entities** (which can be many and whose number may change during a model run) 
   are represented by objects that are instances of the class representing the respective entity-type.
   While the entity-type class holds some processes' and variables' metadata, the entity object holds their logics and values, see below.
   
-  Likewise, each **process taxon** is represented by a class derived from the abstract class ``ProcessTaxon``.
   In addition, each of these process taxon classes will have exactly one instance object.
   (As above, the class holds process and variable metadata and the object holds logics and values)

-  Also each formal **process-type** is represented by a class derived from the abstract class ``ProcessType``
   (e.g., ``ODE``, ``Explicit``, ``Implicit``, ``Step``, ``Event``, ...). 

-  Each individual **process** is represented by two things:

   -  The process' *metadata* (e.g., name, description, influenced variables, degree of smoothness, rate of occurrence, ...)
      are represented by an object that is an instance of the respective process-type class
      
   -  The process' *logics* (e.g., its defining equations or algorithm)
      are represented by one or more methods that read and write the object attributes representing variable values and time derivatives (see below).
      In sufficiently simple cases, the equations can alternatively be specified directly in the process' metadata object 
      via *symbolic expressions* constructed from the class attributes representing the variables (see below). 

   If the process belongs to an entity-type, its metadata object is listed in this entity-type's *class attribute ``processes``*,
   and its logics methods are implemented as object methods inside this class, thus becoming methods of each individual entity object.
   
   Analogously, 
   if the process instead belongs to a process taxon, its metadata object is listes in this taxon's class attribute "processes",
   and its logics methods are implemented as object methods inside this class, thus becoming methods of the unique instance object of this taxon class.

-  Also each individual **variable** is represented by two things:

   -  The variable's *metadata* are represented by an instance of the class ``Variable``.
      This object is assigned to a *class attribute* of the entity-type or process taxon the variable belongs to,
      using a descriptive and unique attribute name (e.g., ``atmospheric_carbon``).
      The same object may also be used in symbolic expressions stating process equations 
      (e.g. ``diffusion_rate * (atmospheric_carbon - maritime_carbon)``),
      and for this reason the class "Variable" implements methods that represent the allowed algebraic operations (``+``, ``-``, ``*``, ...)
      and return objects representing these symbolic expressions.

   -  During model runs, the variable's current *value* and optionally *time derivative* are stored as *object attributes* as follows:
   
      -  If the variable belongs to a process taxon (which should rarely be the case), 
         the value is stored in an attribute of the process taxon's unique object under the same name as the metadata object,
         and the derivative is stored in the same object using the same name prefixed with ``d_``.
         
      -  If the variable ``x`` belongs to an entity-type (which should mostly be the case),
         it can and often will have a different value and derivative in each entity of this type.
         The current value and derivative of ``x`` in some entity ``e`` are thus stored in the object attributes ``x`` and ``d_x`` of the object ``e``
         and can typically refered as ``e.x`` and ``e.d_x``.  

-  All of the above is true not only on the level of (composed) models
   but already on the level of **model components**, though restricted to the types, processes and variables used in the respective component.
   To avoid name clashes but still be able to use the same simple naming convention throughout in all model components, 
   we use *subpackages* of the main copan:\CORE package to represent model components as follows:
   
   -  Each model component is represented by a subpackage, say ``P``, containing class definitions for all used entity-types and process taxons.
   
   -  Each entity-type used in the model component's package, say ``A``, 
      is represented by an **implementation class** invariably named ``A``, 
      which can be referred to from outside the package as ``P.A``.
      
   -  A method, say ``f``, that represent the logics of a process belonging to ``A`` 
      may need to refer to another entity-type's variables, say ``B.y``, and vice versa from ``B`` to ``A``,
      but cyclical imports must be avoided, 
      each package provides an additional **interface class** for each entity-type, 
      either named with a prefix ``I_`` or named as the implementation class and collected in a special module ``P.interface``,
      so that it can be referred to as either ``P.I_A`` or ``P.interface.A``.
      The interface classes contains all variables, 
      and it is thus sufficient to import the respective interface class, say ``I_A``,
      into another entity-type's implementation class, say ``B``, 
      to let a process method in ``B`` read and write variables from ``A``.
      Consequently, all process methods' implementations must be in the implementation class (``A``) 
      rather than in the interface class (``I_A``).
      
      In order to avoid redundancy, the entity-type ``A`` is thus defined inside package ``P`` as follows:
      
      -  The interface class ``P.I_A`` or ``P.interface.A``, derived from the abstract class ``EntityInterface``, 
         defines the entity-type's variables and nothing else (in particular, no method declarations).
         
      -  The implementation class ``P.A`` is derived from this interface class
         and lists and defines the entity-type's processes and nothing else
         (in particular, it inherits the variables from the interface).
         If it needs access to another entity-types' variables, it imports the other interface classes.

-  Finally, a **model**'s composition from model components is represented via *multiple inheritance from mixin classes* as follows:

   -  Each model is defined in a separate *module* (if the language has modules, otherwise a subpackage), say ``M``.

   -  For each entity-type, say ``E``, that is defined in at least one of model component packages, say ``P1``, ``P2``, ...,
      the model defines a (composite) class ``M.E`` that derives from all the implementation classes of ``E`` contained in these packages.
      I.e., if packages ``P2`` and ``P5`` contain a definition of ``E``, then ``M.E`` derives from ``P2.E`` and ``P5.E``.
      If the programming language allows that a method occurs in more than one mixin class,
      this feature can be used to "overrule" specifications from one model component by another model component,
      and in that case the order of overruling must be specified in the definition of ``M.E``, 
      typically by listing its mixin classes in a suitable order.[#]_
      
   
==================== ================================ ====================================================================================================================================================
Modeling concept     Used object-oriented concept(s)  Comments
==================== ================================ ====================================================================================================================================================
Entity-type          Class derived from "Entity"      of which the entity objects are instances
Entity               Object                           instance of class representing its entity-type
Process taxon        Class and unique object          used to hold Variables' metadata and values
Process-type         Class derived from "Process"     of which the process metadata objects are instances
Process' metadata    Object used as list entry        instance of class representing its process-type, listed in the *class* representing the entity-type or process taxon it belongs to
Process' logics      Object method                    of the entity or process taxon *object* it belongs to
Variable's metadata  Object used as class attribute   instance of class "Variable" and used as an attribute in the *class* representing the entity-type or process taxon it belongs to
Variable value       Object attribute                 of the entity or process taxon *object* it belongs to
Variable time deriv. Object attribute                 of the entity or process taxon *object* it belongs to, named with prefix ``d_``
Model component      Package of mixin classes         one for each entity-type and process taxon used in the component, containing the processes and variables used in the component
Model                Collection of derived classes    mixed from the mixin classes provided by the components specified in the model's metadata
==================== ================================ ====================================================================================================================================================


TODO: Simulation and analysis logic
-----------------------------------

- Runners

- Skripts


.. [#]   If the programming language provides enough introspection features (like Python does),
         the framework may "recompile" the class ``M.E`` at runtime from the merged source code of ``P2.E`` and ``P5.E``
         for performance reasons, effectively "flattening" the class ``M.E`` into a class without superclasses.
