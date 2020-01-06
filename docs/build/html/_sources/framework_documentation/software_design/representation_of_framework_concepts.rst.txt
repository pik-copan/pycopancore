Representing modeling framework concepts by object-oriented concepts
====================================================================


Entities, processes, variables
------------------------------

-  A model's **entity-types** are represented as classes that are derived from a common abstract class
   and are named with the common noun used for the respective type of entity (i.e., ``Cell``, ``SocialSysten``, ``Individual``, ...).

-  All individual **entities** (which can be many and whose number may change during a model run)
   are represented by objects that are instances of the class representing the respective entity-type.
   While the entity-type class holds some processes' and variables' metadata, the entity object holds their logics and values, see below.

-  Likewise, each **process taxon** is represented by a class derived from a common abstract class.
   In addition, each of these process taxon classes will have exactly one instance object.
   (As above, the class holds process and variable metadata and the object holds logics and values)

-  Also each formal **process-type** is represented by a class derived from a common abstract class
   (e.g., ``ODE``, ``Explicit``, ``Implicit``, ``Step``, ``Event``, ...).

-  Each individual **process** is represented by two things:

   -  The process' *metadata* (e.g., name, description, influenced variables, ...)
      are represented by an object that is an instance of the respective process-type class

   -  The process' *logics* (e.g., its defining equations or algorithm)
      are represented by 
      
      -  either a method that reads and writes the object attributes representing variable values and time derivatives (see below),
      
      -  or by *symbolic expressions* contained in the process' metadata object, 
         constructed from the class attributes representing the variables (see below).  

   If the process belongs to an entity-type, its metadata object is listed in this entity-type's *class attribute ``processes``*,
   and its logics methods are implemented as object methods inside this class, thus becoming methods of each individual entity object.

   Analogously,
   if the process instead belongs to a process taxon, its metadata object is listed in this taxon's class attribute ``processes``,
   and its logics methods are implemented as object methods inside this class, thus becoming methods of the unique instance object of this taxon class.

-  Also each individual **variable** is represented by two things:

   -  The variable's *metadata* are represented by an instance of the class ``Variable``.
      This object is assigned to a *class attribute* of the entity-type or process taxon the variable belongs to,
      using a descriptive and unique attribute name (e.g., ``atmospheric_carbon``).
      
   -  During model runs, the variable's current *value* and optionally *time derivative* are stored as *object attributes* as follows:

      -  If the variable belongs to a process taxon (which should rarely be the case),
         the value is stored in an attribute of the process taxon's unique object under the same name as the metadata object,
         and the derivative is stored in the same object using the same name prefixed with ``d_``.

      -  If the variable ``x`` belongs to an entity-type (which should mostly be the case),
         it can and often will have a different value and derivative in each entity of this type.
         The current value and derivative of ``x`` in some entity ``e`` are thus stored in the object attributes ``x`` and ``d_x`` of the object ``e``
         and can typically refered as ``e.x`` and ``e.d_x``.

-  A **symbolic expression** is represented by an instance of a superclass of ``Variable``, called e.g., ``Expr``, 
   which supports arithmetic operations whose results are again objects of this class. 
   Each symbolic expression has an "owning" entity type or process taxon and a "target" entity type or process taxon 
   which in simple cases coincide.
   E.g., the symbolic expression ``Cell.population / Cell.land_area`` has owning and target class ``Cell``.
   Symbolic expressions may however also be used to state that a process owned by one entity type, say ``SocialSystem``,
   influences variables from another entity type, say ``Cell``, using a certain relationship between the corresponding entities.
   E.g., the target variables of a process "taxation" owned by a dictatorial ``SocialSystem`` may be stated by the two expressions
   ``SocialSystem.residents.tax_load`` and ``SocialSystem.dictator.income``,
   both having owning type ``SocialSystem`` and target type ``Individual``.
   Finally, symbolic expressions may also perform aggregations across different entity types
   and also combine variables from different entity types, e.g. as in
   ``World.respiration_rate * World.sum.cells.terrestrial_carbon_stock``;
   due to the *aggregation keyword* ``sum``, the latter expression has target class ``World`` rather than ``Cell``.
   More complex aggregations can be written by using an *aggregation method*,
   e.g. ``World.sum(World.cells.population / World.cells.land_area)``;


Modularization
--------------

All of the above is true not only on the level of (composed) models
but already on the level of **model components**, though restricted to the types, processes and variables used in the respective component.
To avoid name clashes but still be able to use the same simple naming convention throughout in all model components,
we use *subpackages* of the main copan:\CORE package to represent model components as follows:

-  Each model component is represented by a subpackage, say ``P``, containing class definitions for all used entity-types and process taxons.

-  Each entity-type used in the model component's package, say ``A``,
   is represented by an **implementation class** invariably named ``A``,
   which can be referred to from outside the package as ``P.A``.

-  Since a method or symbolic expression that represent the logics of a process belonging to ``A``
   may need to refer to another entity-type's variables, say ``B.y``, and vice versa from ``B`` to ``A``,
   but as cyclical imports must be avoided,
   each package provides an additional **interface class** for each entity-type named exactly as the implementation class
   and collected in a special module ``P.interface``, so that it can be referred to as ``P.interface.A``.
   The interface class contains all variable metatada objects,
   and it is thus sufficient to import the respective interface class, say ``interface.A``,
   into another entity-type's implementation class, say ``B``,
   to let a process in ``B`` read and write variables from ``A``.
   Consequently, all processes must reside in the implementation class (``A``)
   rather than in the interface class (``interface.A``).

   In order to avoid redundancy, the entity-type ``A`` is thus defined inside package ``P`` as follows:

   -  The interface class ``P.interface.A`` defines the entity-type's variables
      and nothing else (in particular, no method declarations).

   -  The implementation class ``P.A`` is derived from this interface class
      and lists and defines the entity-type's processes and nothing else
      (in particular, it inherits the variables from the interface).
      If it needs access to another entity-types' variables, it imports the other interface classes.

Finally, a **model**'s composition from model components is represented via *multiple inheritance from mixin classes* as follows:

-  Each model is defined in a separate *module* (if the language has modules, otherwise a subpackage), say ``M``.

-  For each entity-type, say ``E``, that is defined in at least one of model component packages, say ``P1``, ``P2``, ...,
   the model defines a (composite) class ``M.E`` that derives from all the implementation classes of ``E`` contained in these packages.
   I.e., if packages ``P2`` and ``P5`` contain a definition of ``E``, then ``M.E`` derives from ``P2.E`` and ``P5.E``.
   If the programming language allows that a method occurs in more than one mixin class,
   this feature can be used to "overrule" specifications from one model component by another model component,
   and in that case the order of overruling must be specified in the definition of ``M.E``,
   typically by listing its mixin classes in a suitable order. [#]_


Tabular summary
---------------

==================== ================================ ====================================================================================================================================================
Modeling concept     Used object-oriented concept(s)  Comments
==================== ================================ ====================================================================================================================================================
Entity-type          Class                            of which the entity objects are instances
Entity               Object                           instance of class representing its entity-type
Process taxon        Class and unique object          used to hold Variables' metadata and values
Process-type         Class                            of which the process metadata objects are instances
Process' metadata    Object used as list entry        instance of class representing its process-type, listed in the *class* representing the entity-type or process taxon it belongs to
Process' logics      Object method                    of the entity or process taxon *object* it belongs to
Variable's metadata  Object used as class attribute   instance of class "Variable" and used as an attribute in the *interface class* representing the entity-type or process taxon it belongs to
Variable value       Object attribute                 of the entity or process taxon *object* it belongs to
Variable time deriv. Object attribute                 of the entity or process taxon *object* it belongs to, named with prefix ``d_``
Entity relationship  special Variable object          whose value is an instance or set of instances of a certain type
Model component      Package of mixin classes         one for each entity-type and process taxon used in the component, containing the processes and variables used in the component
Model                Collection of derived classes    mixed from the mixin classes provided by the components specified in the model's metadata
==================== ================================ ====================================================================================================================================================


.. [#]   If the programming language provides enough introspection features (like Python does),
         the framework may "recompile" the class ``M.E`` at runtime from the merged source code of ``P2.E`` and ``P5.E``
         for performance reasons, effectively "flattening" the class ``M.E`` into a class without superclasses.
