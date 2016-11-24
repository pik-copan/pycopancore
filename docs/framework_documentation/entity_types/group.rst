Entity-type "Group"
===================

For many model components, especially those involving cultural, micro-economic, or other social processes,
the metabolic/economic/political/administrative partitioning of the global social metabolism 
into what we call :doc:`"societies"<society>` (nation states, regions, urban areas, ...)
is not sufficient and a distinction of social strata or other social groups or parties 
(e.g., "European working class", "global elite", "scientists", "climate activists", "indigenous people", "social democrats", ...)
that is transverse to the former partitioning is needed in addition.

For this, we provide the entity-type "group" 
which is meant to represent any grouping of individuals (that may come from one or several societies) 
by meaningful *cultural* or social-metabolic aspects.

In contrast to a :doc:`society<society>`, a group does *not* normally have a territory and does not even have to be otherwise localised, 
and does *not* normally have a high degree of social-metabolic integration and independence from other groups.

While societies cannot have non-trivial intersections (they can only be disjoint or containing each other completely),
groups may *overlap* in any complex ways.

Wikipedia has a nice **working definition** of what makes a group: 
"a group is defined in terms of those who identify themselves as members of the group".

Groups may act as agents in agent-based model components.


Basic relationships to other entity-types
-----------------------------------------

A group will usually...

-  have several member :doc:`individuals<individual>`

In addition, a group may...

-  have one or several "leader" :doc:`individuals<individual>` 

-  have a "headquarters" :doc:`cell<cell>`

-  have a network of links to other groups 
   (which will typically interact with the network of personal links between member individuals)

-  act as the current "elite" in some :doc:`society<society>`

All these relationships may be dynamic.

Finally, a group may...

-  be a permanent subgroup of a larger group or :doc:`society<society>` *by definition* 
   (rather than by coincidence, e.g., "scientists" are by definition a subgroup of the group "academics",
   and "German workers" may be by definition a subgroup of the society "Germany")

