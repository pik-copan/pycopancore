Language, basic terminology, and concepts
=========================================

Because of the interdisciplinary environment of this endeavour, 
finding a common *language* is a challenge bound to lead to misunderstandings and probably unfounded tacit assumptions.
In the copan\:CORE documentation and implementation,
we therefore try to use simple non-disciplinary language wherever possible,
and explain our usage of *terms* that have different meanings in different disciplines as good as possible
using a combination of definitions and examples.


Entities, processes, attributes
-------------------------------

copan\:CORE treats the *real world* as consisting
of numerous sufficiently well-distinguishable **entities**
("things that are", e.g., a spot on the Earth surface, the EU, yourself, ...) [#]_
that are involved in a number of sufficiently well-distinguishable **processes**
("things that happen", e.g., vegetation growth, economic production, opinion formation, ...)
which affect one or more **attributes**
("how things are", e.g., the spot's harvestable biomass, the EU's gross product, 
your opinion on fossil fuels, the ocean-atmosphere diffusion coefficient...).

copan\:CORE classifies entities by **entity-types**
("kinds of things that are", e.g., grid cell, social system, individual, ..., see :doc:`./entity_types/index`),
and allows to group (some or all) processes into **process taxons**
(environmental, social-metabolic, cultural, ..., see :doc:`./process_taxonomy/index`).


Processes and attributes "belong to" entity-types or process taxons
-------------------------------------------------------------------

On the *model level,* each process and each attribute 
**belongs to** either a certain entity-type or a certain process taxon.
When talking about processes, 
people from very different backgrounds widely use a subject-verb-object sentence structure
even when the subject is not a conscious being and the described action is not deliberate
(e.g., "the oceans take up carbon from the atmosphere").
copan\:CORE therefore allows modelers to treat some processes 
as if they were "done by" a certain entity (the "subject" of the process)
"to" itself and/or certain other entities (the "objects" of the process).
Other processes for which there appears to be no natural candidate entity to serve as the "subject"
can be treated as if they are happening "inside" or "on" some larger entity 
that contains or otherwise supports all actually involved entities.
In both cases, the process is treated as **belonging to some entity-type.**
Still other processes may best be treated as not belonging to any entity
but rather as simply **belonging to a process taxon** (environment, social metabolism, culture, ...) [#]_.

We deliberately do *not* specify sharp criteria for
whether a modeler should treat a certain process as being "done by" or "happening inside" an entity
since this is in part a question of style and academic discipline
and there will inevitably be examples where this choice appears to be quite arbitrary
and will affect only the model's description, implementation, and maybe its running time, but not its results.
An example might be the photosynthesis part of the carbon cycle,
which could be described by either saying "plants take carbon from the air" and attaching it to the plant as the subject
or by saying "plants' RuBisCO enzymes and atmospheric carbon dioxide react to form 3-phosphoglycerate"
and attaching it to the grid cell it is happening on,
or by simply attaching it to the taxon of environmental processes.

Similarly, attributes may be modeled as "belonging to" some entity-type
(e.g. "total population" or "territory" might be modeled as attributes of the "social system" entity-type)
or to some process taxon
(e.g. "diffusion coefficient" might be modeled as an attribute of the "environment" process taxon).
We suggest to model most quantities as entity-type attributes
and model only those quantities as process taxon attributes which represent global constants.


Formal process-types and data-types
-----------------------------------

Independently of where processes belong to,
they are also distinguished by their formal **process-type**
(continuous dynamics given by ordinary differential equations,
(quasi-)instantaneous reactions given by algebraic equations, steps in discrete time, irregular or random events, ...,
see :doc:`./process_types/index`)
that correspond to different modeling and simulation/solving techniques.

Similarly, attributes have **data-types**
(mostly physical or socio-economic *simple quantities* of various dimensions and units,
but also *more complex* data-types such as "network").
See also metadata_ below.


Modularization into model components and models
-----------------------------------------------

copan\:CORE aims at supporting a plug-and-play approach to modeling
and a corresponding division of labour between several user groups (or **roles**)
by dividing the overall model-based research workflow into several tasks:

- if there is already a model that fits your research question, use it in your study
  (role: :doc:`../../tutorials/model_end_users`)

- if not, decide what model components the question at hand needs

- if all components exist, compose a new model from them
  (role: :doc:`../../tutorials/model_composers`)

- if not, design and implement missing model components
  (role: :doc:`../../tutorials/model_component_developers`)

- if some required entity attributes are not yet in the master data model (see below), add them to your component

- suggest well-tested entity attributes, entity-types, or model components 
  to be included in the master data model or master component repository
  (role: :doc:`../../tutorials/modeling_board_members`)

As a consequence, we distinguish between model components and (composed) models.

A **model component** specifies:

- a meaningful collection of *processes* that belong so closely together
  that it would not make sense to include some of them without the others into a model
  (e.g., plant photosynthesis and respiration, or capital investment and depreciation, 
  or individuals' choice of profession and residence)

- the entity *attributes* that those processes deal with,
  referring to attributes listed in the master data model whenever possible
  (e.g., a cell's terrestrial carbon stock, a social system's capital stock, an individual's skill level)

- if really necessary, any additional *entity-types* not existing in the master data model, and their attributes
  (e.g., an entity-type "lake" with certain attributes)

A **model** specifies:

- which model *components* to use

- if necessary, which components are allowed to *overrule* parts of which other components
  (e.g., a "climate policy" component might need to overrule the process "fossil fuel extraction" 
  that was specified by a component "energy sector")

- if necessary, any attribute *identities*: whether some attributes should be considered to be the same thing
  (e.g., in a complex model, an attribute "harvestable biomass" used by the "energy sector" component as input
  may need to be distinguished from an attribute "total vegetation" governed by a "vegetation dynamics" component,
  but a simple model that has no "land use" component that govern their relationship may want to identify the two)

The **master data model** defines entity types, process taxons, and attributes which the modeling board members
deem...

- likely to occur in many different models or model components

- sufficiently well-defined and well-named
  (in particular, specific enough to avoid most ambiguities but avoiding a too discipline-specific language)

The **master component repository** contains model components which the modeling board members
deem...
- likely to be useful for many different models
- sufficiently mature and well-tested
- indecomposable into more suitable smaller components


.. _metadata:

All attributes are treated as "Variables" with metadata
-------------------------------------------------------

Although many models make an explicit distinction between *endogenous* and *exogenous variables* and *parameters,*
there seems to be no clear consensus regarding the exact criteria for such a distinction
and the exact definition of those two terms.

In copan\:CORE, we made the very pragmatic decision to treat all relevant quantities a priori in the same way,
model them as attributes of either entities or process taxons, and simply call them **variables,**
whether or not during a specific model run they turn out to be changing or constant and not changing,
or whether they are used for a bifurcation analysis in a study etc.

One reason for this is that a quantity that one model component 
uses as a "parameter" that will not be changed by this component
may easily be an endogenously changed "output" variable of another component.
Hence it is not known to a model component developer 
which of the quantities she deals with 
will turn out to be changing endogenous "variables" or constant exogenous "parameters" 
of the various models and studies that use this component.
Only a posteriori (after composition of a specific model from model components),
one might call those variables that will never be changed from their initial value during any model runs 
the "parameters" of this model.

A variable's specification will contain **metadata** such as

- a common language *name* (used in human-directed output)

- a *description* giving its (rough) definition and other relevant textual information

- a mathematical *symbol* normally used to denote it

- its `level of measurement`_ (aka scale of measure, i.e, ratio, interval, ordinal, or nominal)

.. _`level of measurement`: https://en.wikipedia.org/wiki/Level_of_measurement

- its physical or socio-economic *dimension* (e.g., length) and default unit (e.g., meters), 
  if possible following some established standard (e.g., SI units),
  but sometimes using more refined distinctions 
  (e.g., the variable "atmospheric carbon stock" has a dimension of "carbon" with default unit "tonnes carbon", 
  and the variable "human population" has a dimension of "humans" with default unit "people"),
  and, if applicable, whether the variable is *extensive* or *intensive*

- its *datatype*, a range of possible values
  (giving non-strict or strict lower and/or upper *bounds* and/or a *quantum* for interval- or ratio-scaled variables,
  or a set of *levels* for nominal- or ordinal-scaled ones, possibly including the value "none"),
  a *default* (constant or initial) value,
  and an *uninformed prior distribution* that may be used to generate random values, 
  e.g. for Monte-Carlo simulations 

- *references* (preferably URLs) of any items in existing metadata catalogs that can be (roughly) identified with the variable
   (e.g., a `CF Standard Name`_ or a `World Bank CETS code`_)

.. _`CF Standard Name`: http://cfconventions.org/standard-names.html

.. _`World Bank CETS code`: https://datahelpdesk.worldbank.org/knowledgebase/articles/201175-how-does-the-world-bank-code-its-indicators


.. [#]   Since many models dealing with processes actually happening on a continuous spatial scale
         use a more or less fine discretization of space 
         into equally or differently sized, regularly or irregularly arranged units
         (often called "grid cells", sometimes "elements", ...),
         we explicitly include an entity-type "cell" 
         although the partitioning of continuous space into cells
         may not always be related to well-distinguishable parts of space 
         but rather follow some technical criteria
         (e.g., a regular latitude-longitude grid 
         rather than an irregular grid derived from the Earth surface's topography)

.. [#]   The question where a process "belongs" will become important on the *software design* level:
         processes belonging to individual entities will be represented by 
         class attributes and instance methods of the corresponding entity-type class,
         while processes belonging to a process taxon will be represented by 
         class attributes and instance methods of the corresponding process taxon class.

