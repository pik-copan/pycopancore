Processes and their representation
==================================

Resources, metabolism, economy
------------------------------

In a first version, this
*could*
be modelled as follows:

*   Either a simple logistic growth equation or a simple carbon cycle model as in Anderies et al. 2013 for modelling the dynamics of the stock of exploitable biomass



*   A simple economy as in copan:GLOBAL: at each point in time, the stocks of all relevant resources (exploitable biomass, fossil carbon, renewable energy technology, labour and capital) determine in a general equilibrium fashion the harvest rate of biomass, the extraction rate of fossil fuel, the amount of renewable energy produced, the amount of final goods produced, consumed and invested, the shares of labour and capital utilized in these four production processes, and the resulting emissions and capital growth.



*   A simple population dynamics model as in copan:GLOBAL: mortality declines with well-being (mainly per capita consumption), fertility increases with well-being if small and declines with well-being if large.



This may be complemented by equations for waste / impacts on soil quality if we think soil degradation is a dominant
process
.


A major decision to be made here is whether all grid cells within a society are assumed to
*share*
all their resources and products in a basically fair or optimal way (easy to model within the general equilibrium framework) or not at all (probably leading to unrealistically large inequality between the cells of one society) or somehow differently (which would be hard to model since it would probably involve explicitly modelled
trade
). In a basically general equilibrium framework, the following subprocesses
*could*
be modelled in a straightforward manner:

*   *Migration*
    : if one assumes people are free to choose their residency within the territory of their own society and do so on the basis of income expectations (empirical studies suggest that this is indeed a major driver of migration) relatively fast, then the whole migration subcomponent can be modelled as part of the general equilibrium allocation of resources in this way: the society’s total population is distributed so that wages are the same in all cells. This leads to a set of simple algebraic equations, one per cell, which can be analytically solved if the production functions are simple enough, e.g. as in copan:GLOBAL. To exemplify this, imagine there is only one sector whose production function in each cell is Y(c) = (P(c) K(c))^½ where P(c) is cell population, assumed to be mobile, and K(c) is the cell’s physical capital, assumed to be immobile. Then
    *wage equalization*
    implies that the society’s total population P is “allocated” to cells so that P(c) is proportional to K(c) for all cells, i.e., P(c) = P K(c) / K. So if P and all K(c) change over time, the time evolution of P(c) follows from this equation. The net effect is that population moves towards “richer” cells.



*   *Trade in energy resources*
    (e.g. biomass, fossil fuel): if one assumes cells can trade this freely, then the flow of these resources can be modelled in exactly the same way as the flow of people above, with the addition that the buying cell pays the selling cell using
    *marginal cost pricing*
    . Again, the equations will be straightforward and sufficiently simple if the production function is simple enough.



*   *Capital mobility*
    : here one would probably have to distinguish between physical capital / infrastructure which is hardly mobile and financial capital which is quite mobile. When doing so, the latter can be treated in exactly the same way as labour and fuel above, by
    *equalization of capital rents*
    . All these things are formally completely analogous, which is a major appeal of this framework.



*   One could
    *switch each of the above three processes on or off*
    independently in order to represent different stages in the development of a society’s economy: maybe after merging two smaller societies they first trade their energy resources and later then allow free choice of residency and financial capital mobility. These switches could also be considered (hard) policy choices driven by opinions.



*   Instead of switching them on fully, one can also switch them on “partially” by introducing initially high and potentially declining
    *transaction/relocation costs*
    , which can also be done in the same framework.



Social dynamics on the individual, intra-societal level
-------------------------------------------------------

*   *Birth*
    at location of parents and
    *inheritance*
    of links and opinions from parents



*   Voting and other types of influence on the societal level



*   ...



Social dynamics between individuals not restricted to the same society
----------------------------------------------------------------------

*   Network
    *adaptation*
    by rewiring links from outside to inside your own society,
    but taking into account spatial link-length distribution



*   Additional random rewirings



*   Imitation or learning of opinions along network links



*   Dynamics distinguishing exchange of values, preferences, opinions, behaviors etc. along network
    links




*   The dynamics of opinions could also be linked to economic inequality between individuals. Vice versa, consumption decisions should somehow influence the metabolic dynamics.



Social dynamics on the society level / between societies
--------------------------------------------------------

*   Merging and splitting of societies (
    initiated by an individual as in Auer et al. 2015?
    )



*   Metabolic choices / policy decisions

    *   Each binary choice variable has a certain probability rate to switch depending on the share of individuals holding the opposite opinion (e.g. zero if less than 50% opposition and sigmoidally increasing towards a maximum policy change rate for 100% opposition)





*   Later maybe:

    *   within societies: capture sectoral dynamics to connect to SDG policy process (energy, health, education, ...)



    *   diffusion of knowledge about technologies



    *   trade



    *   coalitions of societies: diplomacy



    *   war



    *   colonialization






A major design question is whether we need to model links between societies explicitly (resulting in a second network) or whether we can assume that the link strength between different societies is simply implicitly given by the number of links between their
members
.
