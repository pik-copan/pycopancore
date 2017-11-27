Entity-types in the copan\:CORE base model
==========================================


Entity or attribute?
--------------------

We try to keep the number of explicitly considered entity types manageably small
and thus choose to model some relevant things that occur in the real world not as separate entities
but rather as *attributes* of other entities.

As a rule of thumb, things that can occur in *a priori unknown and maybe changing numbers* (e.g., individuals)
will be modeled as entities,
whereas things that typically occur *only once or only once for each entity of some type* (e.g., an individual's bank account)
are modeled as attributes of the latter entity-type.

A notable exception is the entity type *"world"*.
Although it will typically (but not necessarily) only have one instance ("the world"),
it is introduced so that all other things a model typically considers to be *singular*
(e.g., the global trade network or the well-mixed atmospheric carbon stock)
can be modelled as attributes of the world entity.

In addition to the entity-type :doc:`"world"<world>`,
the copan\:CORE base model currently provides the three main entity-types 
:doc:`"cell"<cell>`, :doc:`"social system"<social system>`, and :doc:`"individual"<individual>`
that are meant to be the main subjects and objects
of the three process taxons 
:doc:`"environment"<../process_taxonomy/environment>`, 
:doc:`"social metabolism"<../process_taxonomy/social_metabolism>`, 
and :doc:`"culture"<../process_taxonomy/culture>`,
although modelers are free to attach, say, a cultural process to a social system or cell,
or an environmental process to an indivudual, etc.

In addition to these, we may provide further entity-types in the future, such as 
:doc:`"household"<household>`, :doc:`"group"<group>` and :doc:`"firm"<firm>`
since they will likely be needed by some more detailed social-metabolic model components.

During a model run, entities may come into existence 
(individual may be born, groups and firms may be founded, social systems may merge into larger ones)
or cease to exist (individuals may die, firms may be terminated, social systems may collapse).


Basic relationships
-------------------

The following UML diagram shows the basic relationships between the entities of the different types:

.. image:: basic_relationships.png
   :scale: 20%


:download:`Here <./basic_relationships.pdf>` is the pdf version of the image.


Contents:

.. toctree::
   :maxdepth: 1

   world
   cell
   social_system
   individual
   household
   group
   firm
