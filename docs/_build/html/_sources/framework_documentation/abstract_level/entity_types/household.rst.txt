Entity-type "Household"
=======================

Entities of the potential entity-type *household* 
may act as agents in agent-based model components representing certain social-metabolic processes.

In contrast to certain economic modeling approaches that use "representative households",
an entity of type "Household" in copan\:CORE is *not* usually meant to represent a whole class of similar households 
(e.g., all the actual households in one social stratum)
but just one specific household.
So typically a model will contain many households.
The set of all household entities contained in the model should be interpreted as being a *representative sample* of all real-world households.

Basic relationships to other entity-types
-----------------------------------------

A household will usually...

-  reside in some :doc:`cell<cell>`

-  have some :doc:`individuals<individual>` as members

In addition, a household may...

-  have one "head of household" :doc:`individual<individual>`

All these relationships may be dynamic.

