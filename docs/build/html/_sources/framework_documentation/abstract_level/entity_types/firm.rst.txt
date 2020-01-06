Entity-type "Firm"
==================

Entities of the envisioned entity-type *firm* 
are meant to represent any type of business, company, corporation, holding, bank, etc.,
that may be treated as an employer, producer of products, or provider of services 
in a micro-economic model of a social system's economy.
 
Firms are mainly meant to act as agents in agent-based model components.

In contrast to certain economic modeling approaches that use "representative firms",
an entity of type "firm" in copan\:CORE is *not* usually meant to represent a whole class of similar firms 
(e.g., all the actual firms in one sector)
but just one specific firm.
So typically a model will contain many firms per sector.
The set of all firm entities contained in the model should be interpreted as being a *representative sample* of all real-world firms.

Depending on how important the decision structures that govern a *publicly owned* business are,
that business may be modeled as an entity of type "firm" or as part of an entity of type "social system".


Basic relationships to other entity-types
-----------------------------------------

A firm will usually...

-  have their legal headquarters in some :doc:`social systems<social system>`

In addition, a firm may...

-  be (mainly) owned by some :doc:`individual<individual>` or other firm

-  have some :doc:`individual<individual>` as CEO

-  have its place of business in several :doc:`cells<cell>`

All these relationships may be dynamic.

