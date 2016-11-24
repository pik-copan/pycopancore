Entity-type "Society"
=====================

What we call a *society* is meant to represent "an economic, social, industrial or cultural infrastructure" (Wikipedia)
of considerable size 
(e.g., a nation such as the US, a country such as Scotland, an urban area such as the Greater Tokyo Area, 
or an economically very closely integrated world region such as the EU),
having a well-defined *territory* (represented by a set of :doc:`cells<cell>`)
and encompassing all the social-metabolic and cultural processes occurring within that territory.
Societies are not meant to represent a single social group or stratum,
for which we provide a different entity-type (:doc:`"groups"<group>`).

The societies in a model are either all disjoint (e.g., representing twelve world regions, or 200 countries),
or they will form a nested hierarchy with no nontrivial overlaps 
(e.g., representing a three-level hierarchy of world regions, countries, and urban areas).

As the attributes of societies will often correspond to data assembled by official statistics,
we encourage to use a partition of the world into individual societies that is compatible to
established standard classifications such as `ISO 3166-1/2`_.

.. _`ISO 3166-1/2`: https://en.wikipedia.org/wiki/ISO_3166

Societies will only rarely act as agents in agent-based model components 
(a better choice would be to use its "elite" and "head of government" as agents instead).


Basic relationships to other entity-types
-----------------------------------------

A society will usually...

-  have several member :doc:`individuals<individual>` and :doc:`households<household>`

-  have several :doc:`cells<cell>` forming its territory

-  be the "legal headquarters" of several :doc:`firms<firm>`

In addition, a society may...

-  be a subsociety of a larger society 
   (e.g., "UK" may be a subsociety of "EU" for some time)
   
-  have a "capital" :doc:`cell<cell>`

-  have some :doc:`group<group>` acting as its "elite"

-  have one or several :doc:`individuals<individual>` acting as "head of government"

All (!) the above relationships may be dynamic.
