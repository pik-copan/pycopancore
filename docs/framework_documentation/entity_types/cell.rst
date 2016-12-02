Entity-type "Cell"
==================

A *cell* represents a small spatial region used for discretizing the spatial aspect 
of processes and attributes which are actually continuously distributed in space.

Cells are assumed to be connected and will usually be convex and two-dimensional,
representing parts of the Earth surface, but may also be three-dimensional if the radial dimension is relevant for modeling. 

They may be of a more or less "regular" shape and arrangement, 
e.g., represent a latitude-longitude-regular grid (with rectangular shaped cells whose area diminishes however towards the poles),
or an icosahedral grid (with roughly equally sized hexagonal cells but a small number of pentagonal cells),
or an irregular triangulation adapted to topography (with higher resolution in regions where the correlation length of the relevant natural processes is smaller). 

Since they have no real-world meaning beyond their use for discretization,
cells are not meant to be used as agents in agent-based model components
(but their residents or owners may be).


Basic relationships to other entity-types
-----------------------------------------

Each cell may...

-  have several resident :doc:`individuals<individual>` and :doc:`households<household>` 

-  belong to the territory of a single or a hierarchy of :doc:`societies<society>` 

-  contain the capital or headquarters of a :doc:`societies<society>` or some :doc:`groups<group>` 

-  be the place of business of some :doc:`firms<firm>` 

-  be owned by some :doc:`individual<individual>` or :doc:`firm<firm>` 

All these relationships may be dynamic.

Finally, a cell will...

-  have a permanent network of geographically neighbouring cells
