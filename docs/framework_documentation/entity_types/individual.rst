Entity-type "Individual"
========================

aka person

don't use term agent (since in copan:CORE, also societies, firms, groups, and households may act as agents in agent-based components!)

Individuals will mainly act as agents in agent-based model components.

In contrast to certain economic modeling approaches that use "representative consumers",
an entity of type "Individual" in copan\:CORE is *not* usually meant to represent a whole class of similar individuals 
(e.g., all the actual individuals of a certain profession)
but just one specific individual.
So typically a model will contain many individuals per profession.
The set of all "Individual" entities contained in the model should be interpreted as being a *representative sample* of all real-world people.


Basic relationships to other entity-types
-----------------------------------------

An individual will usually (i.e. in most models)...

-  reside in some :doc:`cell<cell>`

In addition, in many or some models, an individual may...

-  belong to one :doc:`household<household>`

-  have an employer :doc:`firm<firm>`

-  have a current spouse and (professional) supervisor individual

-  belong to some :doc:`groups<group>` and identify primarily with one of them 

-  have a network of acquaintance to other individuals 

-  act as the head of some :doc:`household<household>`, leader of some :doc:`groups<group>`, 
   CEO of some :doc:`firms<firm>`, or head of government of some :doc:`societies<society>`

All these relationships may be dynamic.

Finally, an individual may...

-  have a father and mother individual

-  have a birthplace :doc:`cell<cell>`
