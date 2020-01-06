Software design (independent of programming language)
=====================================================

This section describes the programming language-independent parts of 
how the :doc:`abstract description<../abstract_level/index>` of the modeling framework is realized as computer software.
For the current implementation concept in the Python programming language, see :doc:`here<../python_implementation/index>`.

.. (Later this may switch from Python to Cython or to C++!)

As it corresponds closely with the *entity-centric* view of the abstract framework,
**object-orientation** is our main design principle.
All parts of the software are organized in packages, subpackages, modules, and classes.

The only exception are those parts of the software that are written by model end-users to perform actual studies, 
which will typically be in the form of scripts 
following a mainly *imperative programming* style that uses the classes provided by the framework.


Contents:

.. toctree::
   :maxdepth: 2

   object_orientation
   representation_of_framework_concepts
   simulation_and_analysis
