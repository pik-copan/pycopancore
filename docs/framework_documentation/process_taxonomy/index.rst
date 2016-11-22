Taxonomy of processes
=====================

Based on [Fischer-Kowalski20xx] and [Donges2016], we classify processes into three major *taxons*.
We give only a rough definition and abstain from defining a finer, hierarchical taxonomy,
being aware that gaining consensus among different disciplines on such a taxonomy would be unlikely,
and thus leaving the assignment of individual processes and attributes to either taxon to the respective model component developers:

TODO: Make the following definitions a little more accessible by changing the wording? Relate more clearly to the figure and add our own figure.

-  the **nature** process taxon is meant to consist of the processes from 
   material subsystems of the Earth system that have no or only negligible human-targeted physical imprints
   (e.g., "ocean-athmosphere diffusion", "growth of unmanaged vegetation", and maybe "decay of former waste dumps")
   and those of their parameters which cannot easily be attached to specific entity-types
   (e.g. a globally constant "diffusion coefficient").
   We expect most natural processes to deal primarily with the entity-types 
   :doc:`"cell"<../entity_types/cell>` ("local" processes described with spatial resolution)
   and :doc:`"world"<../entity_types/world>` ("global" processes described without spatial resolution)
   and sometimes :doc:`"society"<../entity_types/society>` ("mesoscopic" processes described at the level of a society's territory). 

-  the **social metabolism** process taxon is meant to consist of the processes from
   material subsystems with non-negligible human-targeted physical imprints
   (e.g., "harvesting", "afforestation", "emissions", "waste dumping", "land-use change", "infrastructure building", ...)
   and those of their parameters which cannot easily be attached to specific entity-types
   (e.g. a globally constant "carbon content of fossil fuels" coefficient).
   We expect most social-metabolic processes to deal primarily with the entity-types 
   :doc:`"society"<../entity_types/society>` (e.g., processes described at national or urban level),
   :doc:`"cell"<../entity_types/cell>` 
   ("local" social-metabolic processes described with additional spatial resolution for easier coupling to natural processes)
   and :doc:`"world"<../entity_types/world>` ("global" social-metabolic processes such as international trade),
   and only rarely with the entity-types
   :doc:`"firm"<../entity_types/firm>`,
   :doc:`"household"<../entity_types/household>`, 
   or even :doc:`"individual"<../entity_types/individual>` (micro-economic models)

-  the **culture** process taxon is meant to consist of all processes from immaterial subsystems
   (e.g., "opinion adoption", "learning", "voting", ...)
   and those of their parameters which cannot easily be attached to specific entity-types.
   We expect most cultural processes to deal primarily with the entity-types 
   :doc:`"individual"<../entity_types/individual>` (processes described at a "micro" level),
   :doc:`"society"<../entity_types/society>` (processes described at a "macro" level, typically national or urban),
   and :doc:`"group"<../entity_types/group>` (processes described at a "macro" level with social stratification),
   and rarely :doc:`"world"<../entity_types/world>` (international processes such as "diplomacy").

.. image:: http://www.uni-klu.ac.at/socec/eng/bilder/gr_theorie.gif

In the following subsections, these taxons are described in more detail:

.. toctree::
   :maxdepth: 2

   nature
   social_metabolism
   culture


.. [Fischer-Kowalski20xx] ...

.. [Donges2016] Donges, J. F., Lucht, W., Heitzig, J., Cornell, S., Lade, S., & Schlüter, M. (2016). A taxonomy of co-evolutionary interactions in the planetary social-ecological system as represented in models. Working Paper, Potsdam Institute for Climate Impact Research.

   