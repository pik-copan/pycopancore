Entity-type "Social System"
===========================

What we call a *social system* (and many others may simply call a *society*) 
is meant to represent 
"an economic, social, industrial or cultural infrastructure" 
(see Wikipedia's definition of "society")
of considerable size 
(e.g., a nation such as the US, a country such as Scotland, an urban area such as the Greater Tokyo Area, 
or an economically very closely integrated world region such as the EU),
having a sufficiently well-defined *territory* (represented by a set of :doc:`cells<cell>`)
and encompassing all the social-metabolic and cultural processes occurring within that territory.
Social systems are *not* meant to represent a single social group or stratum,
for which one should use different entity-types (such as :doc:`group<group>`).

The social systems in a model are either all disjoint 
(e.g., representing twelve world regions, or about 200 countries),
or they will form a nested hierarchy with no nontrivial overlaps 
(e.g., representing a three-level hierarchy of world regions, countries, and urban areas),
This is important for model components that assume a hierarchical organization of political decision-making and economic and social metabolic accounting.

As the attributes of social systems will often correspond to data assembled by official statistics,
we encourage to use a partition of the world into individual social systems that is compatible to
established standard classifications such as `ISO 3166-1/2`_.

.. _`ISO 3166-1/2`: https://en.wikipedia.org/wiki/ISO_3166

Social systems will only rarely act as agents in agent-based model components 
(a better choice would be to use its "elite" group 
or "head of government" individual as agents instead).


Basic relationships to other entity-types
-----------------------------------------

A social system will usually...

-  reside on a single :doc:`world<world>`

-  have several member :doc:`individuals<individual>`

-  have several :doc:`cells<cell>` forming its territory

In addition, a social system may...

-  be a subsystem of a larger social system 
   (e.g., "UK" may be a subsystem of "EU" for some time)
   
-  have several member :doc:`households<household>`

-  have a "capital" :doc:`cell<cell>`

-  be the "legal headquarters" of several :doc:`firms<firm>`

-  have some :doc:`group<group>` acting as its "elite"

-  have one or several :doc:`individuals<individual>` acting as "head of government"

All the above relationships may be dynamic.
