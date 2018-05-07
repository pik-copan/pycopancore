C++ implementation
==================

This section describes how the computer software described in the :doc:`../software_design/index` is planned to be
also implemented in the C++ programming language in the future.


Most implementation details should be easily portable from Python to C++,
including multiple inheritance,
with a few exceptions discussed shortly here.


Multiple inheritance
--------------------

To overcome the problem that same-named members declared in two base classes are NOT the same member in C++,
we need to put each variable into its own class 
that is then virtually (!) inherited by all components that use the variable,
so that the final composed entity-type class contains only one copy of the variable.


Introspection / reflection
--------------------------

To realize the modularization needs of copan:CORE,
the implementation needs to make use of a suitable reflection mechanism in C++
that allows the following operations at runtime,
similar to what is currently done in the ModelLogics and Variable classes
of the Python implementation:

1. Identify and compare the types of any objects 
2. For any class, get the list of parent classes and variables names
3. Get and set existing variables by their name stored in a string

The currently apparently most standard reflection mechanism in C++, RTTI,
allows to perform tast 1 but not 2 and 3.

Apparently there is no standard reflection mechanism in C++ yet 
but according to 
http://jackieokay.com/2017/05/06/reflection2.html
there are two likely candidates existing as prototypes:

- reflexpr: http://matus-chochlik.github.io/mirror/doc/html/index.html
- cpp3k clang-reflect: https://github.com/asutton/clang-reflect

clang-reflect seems to be the more actively developed and clean approach so far,
implementing the proposal 
http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0590r0.pdf
that makes use of the reflection operator $ to access the metadata of a
type or object.
It seems that clang-reflect supports 2. and 3. via the functions
$T.bases() and $T.member_variables().
It is possible that we have to store entities' and taxa's variable values
in a "variables" struct inside the entity/taxon instead of directly as member variables though.



Symbolic expressions
--------------------
Seems possible in principle, see http://issc.uj.ac.za/symbolic/symbolic.html

Dot constructs can be realized by overloading operators similar to properties.

Other elements
--------------
Variables can be realized as macros that are given the codenames as arguments.

Processes can also be realized as macros that are given the method code as argument.

Each model component gets its own namespace so that entity type classes can have the same name.
In model composition one can then use short namespace aliases.

Use static data members and static member functions for instance-independent functionality.

Pitfalls
--------
- const
- pass-by-reference
- virtual functions

Conventions
-----------
probably follow most of https://google.github.io/styleguide/cppguide.html 
with the obvious exceptions:

- we DO use multiple inheritance
- wo DO allow parameters passed by reference not labeled const to allow dot notation.


