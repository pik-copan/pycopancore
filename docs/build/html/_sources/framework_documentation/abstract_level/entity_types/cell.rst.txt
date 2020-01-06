Entity-type "Cell"
==================

A *cell* represents a small spatial region used for discretizing the spatial aspect 
of processes and attributes which are actually continuously distributed in space.

Each cells is assumed to be connected (consist of one piece)
and will usually be convex and two-dimensional,
representing a part of the Earth surface, 
but may also be three-dimensional if the radial dimension is relevant for modeling. 

They may be of a more or less "regular" shape and arrangement, 
e.g., represent a latitude-longitude-regular grid (with rectangular shaped cells whose area diminishes however towards the poles),
an icosahedral grid (with roughly equally sized hexagonal cells but a small number of pentagonal cells),
an irregular triangulation adapted to topography (with higher resolution in regions where the correlation length of the relevant environmental processes is smaller),
or a rough division of the world into a small number of boxes.

Since they typicylly have no real-world meaning beyond their use for discretization,
cells are not meant to be used as agents in agent-based model components
(but their residents or owners may be).


Basic relationships to other entity-types
-----------------------------------------

Each cell will...

-  be part of a single :doc:`world<world>` 

In addition, a cell may...

-  have a location and shape w.r.t. some coordinate system
 
-  have several resident :doc:`individuals<individual>` and :doc:`households<household>` 

-  belong to the territory of a single or a hierarchy of :doc:`social systems<social system>` 

-  be owned by some :doc:`individual<individual>` or :doc:`firm<firm>` (e.g. for modeling land use)

-  contain the capital or headquarters of a :doc:`social systems<social system>` or some :doc:`groups<group>` or :doc:`firms<firm>` 

-  be the place of business of some :doc:`firms<firm>` 

All these relationships may be dynamic.

Finally, a cell may...

-  be related to other cells in a permanent network of geographically neighbouring cells owned by its :doc:`world<world>` 
