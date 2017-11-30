Abstract description of the copan\:CORE modeling framework
==========================================================

This section describes the copan\:CORE World-Earth modeling framework, 
its concepts and overall data model in abstract and mathematical terms.
For its realization in computer software, see :doc:`../software_design/index`, and 
for the current implementation in the Python programming language, see :doc:`../python_implementation/index`.

**The goal of the copan\:CORE World-Earth modeling framework is to support the development and use of dynamical models
of those processes that are important for the fate of environment and humanity on a global scale on various time scales,
to gain a better understanding of their feedbacks, important parameters, and possible emergent dynamics,
and to help answering research questions about its resilience and possibilities of sustainable management and policy.**

Since the global system consists of entities and processes of quite different type 
-- environmental, social-metabolic/economic, cultural, etc. --
such modeling tasks typically require people from *various disciplines,* 
coming from different schools of thought and using different *modeling techniques*
such as ordinary differential equations, algebraic equations, discrete-time stochastic processes, 
agent-based modeling, complex adaptive networks, etc.

At the same time, the *complexity* of the global system suggests that 
rather than trying to specify a complete model of all its components to answer all possible research questions,
it is more appropriate to follow a **modular** approach 
that provides an extensible set of *model components* from which *specific models* for specific research questions can be composed.

copan\:CORE and its Python implementation *pycopancore* thus provide a **framework**
in which researchers and developers from the World-Earth modeling community and related communities 
can collaboratively design and implement model components 
and then use those to compose and study specific models for specific research questions.


Contents:

.. toctree::
   :maxdepth: 2

   language_terminology_concepts
   entity_types/index
   process_taxonomy/index
   process_types/index