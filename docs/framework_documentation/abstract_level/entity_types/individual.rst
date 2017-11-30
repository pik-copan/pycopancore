Entity-type "Individual"
========================

An *individual* is a (natural) person, i.e., a single human being. 
Individuals will mainly act as agents in agent-based model components,
(but also social systems, firms, groups, and households 
may act as agents in agent-based components!)

In contrast to certain economic modeling approaches that use "representative consumers",
an entity of type "Individual" in copan\:CORE is *not* usually meant to represent a whole class of similar individuals 
(e.g., all the actual individuals of a certain profession)
but just one specific individual.
So typically a model will contain many individuals.
Still, since it is typically not sensible to model every single person on Earth,
the set of all "Individual" entities contained in the model 
should be interpreted as being a *representative sample* of all real-world people,
which is facilitated by the attribute "represented population".


Basic relationships to other entity-types
-----------------------------------------

An individual will usually...

-  reside in some :doc:`cell<cell>`

In addition, an individual may...

-  belong to one :doc:`household<household>`

-  have an employer :doc:`firm<firm>`

-  have a current spouse and (professional) supervisor individual

-  belong to some :doc:`groups<group>` and identify primarily with one of them 

-  act as the head of some :doc:`household<household>`, 
   leader of some :doc:`groups<group>`, 
   CEO of some :doc:`firms<firm>`, 
   or head of government of some :doc:`social systems<social system>`

-  be related to others via a network of acquaintances owned by the :doc:`culture<../process_taxonomy/culture>` taxon

All these relationships may be dynamic.

Finally, an individual may...

-  have a father and mother individual

-  have a birthplace :doc:`cell<cell>`
