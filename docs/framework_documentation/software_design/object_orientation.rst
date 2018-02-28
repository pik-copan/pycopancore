Common concepts of object-oriented programming languages
========================================================

-  An **object** is an *instance* of a certain **class**.

-  A **class** is a collection of like objects.
   It is usually named by a common noun in the singular.

-  Objects and classes can have **attributes** and **methods**:

   -  *Object attributes* (aka *instance attributes*) store static or variable data about individual objects.

   -  *Class attributes* store static or variable data (e.g., metadata) about the class itself.

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
   There are a number of more or less complex "design patterns" describing common practices of how this can be used.

-  **Packages** and **Modules** are somehow meaningful collections of classes (and maybe other things) that form a separate *namespace*.
   A class ``A`` in a package or module ``P`` can typically be referred to as ``P.A``.
   Packages and subpackages can typically form a hierarchical structure similarly (and often implemented as) a file folder structure,
   with modules typically representing the deepest level of this hierarchy, similar to files within a folder structure.
   To be able to refer to things from package ``A`` within package ``B``,
   one typically needs to *import* them from ``A`` to ``B``, and most programming languages forbid cyclical imports.
   A similar need for importing often exists if a class needs access to another class' attributes and methods.
