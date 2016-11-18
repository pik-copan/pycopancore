Language, basic terminology, and main concepts
==============================================

Because of the interdisciplinary nature of this endeavour, finding a common *language* is a challenge 
bound to lead to misunderstandings and unfounded tacit assumptions.
In the copan\:CORE documentation and implementation, 
we therefore try to use common language wherever possible,
and explain our usage of *terms* that have different meanings in different disciplines as good as possible
using a combination of definitions and examples.


Entities, processes, attributes
-------------------------------

copan\:CORE treats the *real world* as consisting 
of numerous sufficiently well-distinguishable **entities** (e.g., a spot on the Earth surface, the EU, yourself, ...) 
that are involved in 
a number of sufficiently well-distinguishable **processes** (e.g., vegetation growth, economic production, opinion formation, ...)
which affect one or more of the entities' **attributes** (e.g., the spot's harvestable biomass, the EU's gross product, your opinion on fossil fuels, ...).
copan\:CORE classifies entities by **entity-types** (e.g., grid cell, society, individual, ..., see :doc:`../entity_types/index`),
and also allows to group processes according to a certain taxonomy (natural, social-metabolic, cultural, ..., see :doc:`../process_taxonomy/index`).

.. TODO: city taxonomy paper!


Two dimensions of classifying processes
---------------------------------------

On the *model level,* each process **belongs to** either a certain entity-type or to a certain process group.
When talking about processes, people from very different backgrounds widely use a subject-verb-object sentence structure
even when the subject is not a conscious being and the described action is not deliberate 
(e.g., "the oceans take up carbon from the atmosphere").
copan\:CORE therefore allows modelers to treat some processes as if they were "done by" a certain entity (the "subject" of the process) 
"to" itself and/or certain other entities (the "objects" of the process).
Other processes for which there appears to be no natural candidate entity to serve as the "subject"
can be treated as if they are happening "inside" or "on" some larger entity that contains or otherwise supports all actually involved entities.
In both cases, the process is treated as **belonging to some entity.**
Still other processes may best be treated as not belonging to any entity 
but rather as simply **belonging to some process group** (natural, metabolic, cultural, ...).

We deliberately do *not* specify sharp criteria whether a modeler should treat a certain process as being "done by" or "happening inside" an entity
since this is in part a question of style and academic discipline 
and there will inevitably be examples where this choice appears to be quite arbitrary
and will affect only the model's description, implementation, and maybe its running time, but not its results.
An example might be the photosynthesis part of the carbon cycle, 
which could be described by either saying "plants take carbon from the air" and attaching it to the plant as the subject
or by saying "plants' RuBisCO enzymes and atmospheric carbon dioxide react to form 3-phosphoglycerate" 
and attaching it to the grid cell it is happening on,
or by simply attaching it to the group of natural processes.

Independently of where processes belong to, they are also classified by **process-type** 
(continuous dynamics given by ordinary differential equations, 
immediate reactions given by algebraic equations, steps in discrete time, irregular or random events, ...,
see :doc:`../process_types/index`)
that correspond to different modeling and simulation/solving techniques.


Modularization into model components and models
-----------------------------------------------

TODO:

*model components*

*models*
