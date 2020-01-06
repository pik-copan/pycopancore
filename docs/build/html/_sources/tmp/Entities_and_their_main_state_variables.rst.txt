Entities and their main state variables
=======================================

There are basically two types of
*natural*
entities that come in fixed numbers (a large number of
*grid cells*
and one
*“planet”*
) and three or four types of
*social*
entities that come in variable numbers, two types of
*“agents”*
(
*“individuals” *
and
*“societies”*
) and one or two types of network
*links*
(one between “individuals”, and optionally one between “societies”). We list them in ascending order of spatial scale, including those state variables deemed important for the first version of the model (see “Interfaces” below for a longer list of potential variables for later model versions):

Individuals
-----------

By “individual” we here mean a single human or a very small group of humans such as a household or small village that has almost no spatial extent and cannot “merge” or “split” as societies can but that is rather a “member” of a society (see below).

*   The model contains a number
    *N*
    of explicitly modelled individuals which are understood as a representative
    *sample*
    of individuals from a usually much larger population
    *P >> N.*



*   Both
    *N*
    and
    *P*
    will change over time due to birth and death of explicitly modelled individuals in line with population dynamics modelled on the society level (see below).



*   Optionally, the model may only have one representative individual per cell, with a “weight” (see below) equal to that cell’s total population, but should allow for more.



*   One suggestion would be to introduce a scaling factor P = a N, such that every 1/a individual is modeled explicitly. Also the decision to recreate could be modeled on the individual level, depending on the opinion vector.




Would it be possible to have a hierarchical structure - that you have individuals belonging to e.g. socio-metabolistic classes and/or /villages/cities at the first level and then countries/regions at the second/third level?



Each explicitly modelled individual
*i*
has the following variables:

*   Spatial
    *location*

    *loc(i) = (x(i), y(i))*



*   ID of the society it belongs to (see below),
    *soc(i)*



*   Binary (yes/no) opinions
    on certain metabolic/policy questions (
    e.g. exploiting fossil fuels, harvesting more biomass for energy than for food, subsidizing renewable energy, having positive population growth, etc.
    ). These will interact with society’s actual choices (see below)



*   Aggregation weight
    *w(i)*
    due to modelling only a sample of all individuals (should basically equal
    *P(soc(i)) / N(soc(i))*
    as long as no further heterogeneity is introduced)




In a later version, one may introduce heterogeneity via parameters such as

*   gender and age (if demographics and inequality become interesting)



*   certain needs (e.g. demand for food) and dispositions for having certain opinions (e.g. level of risk-aversion, attitude towards technology in general)



*   social-metabolic and socio-cultural class / strata (e.g. Sinus bubbles, ...)




Individual links
----------------

These represent a form of friendship, trust,
economic exchange (?)
or regular interaction between individuals and carry those bilateral social processes (e.g. imitation, see below) that are not mediated via society (e.g., market processes, see below).

*   Each indiv. link is an
    undirected
    connection between two
    individuals
    .



*   Initially, the links should be drawn at random using a suitable random geometric / random spatial network model (e.g. probability of being linked is decaying exponentially or as a power law with spatial distance at some rate or exponent
    *d*
    ).



*   Over time, this parameter
    *d*
    of the spatial link length distribution may be changed either exogenously or as a function of society sizes to represent globalization which may be relevant for modelling the great acceleration.



*   Also, links will adapt in some way to the macroscopic social structure represented by the partition of individuals into societies (see below)



Cells
-----

In each grid cell
*c*
, we may have these variables:

*   *stocks*
    of metabolism-relevant resources (see below), e.g. soil and vegetation carbon stocks, lifestock, area of managed land
    , fossil fuel resources available
    , amount of public infrastructure, other material capital, financial capital



*   non-stock variables representing
    *qualitative*
    states such as soil quality
    , biosphere integrity





The possible fixed heterogeneities of grid cells were discussed already above under “fixed spatial heterogeneities”.

“Societies” (=metabolic groups)
-------------------------------

By “society” we here mean a somewhat generic type of group of humans that are metabolically strongly interacting and in that sense may be considered as “acting as one” in most respects that concern their interaction with nature. This is considered to be the most important kind of macroscopic social
organization
.

*   Each indiv. is a member of exactly one soc.: societies are non-overlapping and form a partition of the set of individuals.



*   This
    *membership*
    may change over time, e.g. when societies merge or split (see below), or due to migration (the latter not modelled initially?).



*   All indivs. living in the same grid cell belong to the same soc. since that enables an easier modelling of the relationship between soc. and nature.



*   The
    *territory*
    of a soc. is the union of all the cells where its members live, hence territories are non-overlapping but may not cover the whole planet (some cells may not belong to any territory).



*   Each soc. has some form of
    *metabolism/economy*
    that decides in some way how much of the available resources (see below) are harvested/extracted and used as input to some “production” processes resulting in population dynamics, some form of emissions/waste, optionally changes in cell attributes such as soil quality, and optionally some changes in wealth and/or
    capital
    .



*   Each soc. makes certain
    binary
    choices, e.g. about which resources or technologies to use and/or subsidize that are influenced by indiv. opinions about this.



The “planet”
------------

This would only be needed if climate processes are explicitly modelled, e.g. CO2 emissions leading to warming with metabolic impacts. If so, the main variables are probably

*   atmospheric carbon stock



*   global mean surface temperature




More advanced items here with direct relevance to planetary boundaries and the safe operating space issue:

*   carbon cycle



*   water cycle



*   nutrient cycles



*   other biogeochemical cycles



*   ...



Other entities not modelled yet but maybe later
-----------------------------------------------

*   Intermediate levels of the metabolic hierarchy, e.g. households, villages, cities



*   Groups of individuals that are not closely metabolically interdependent but may still in some respects “act as one”, e.g. society-overarching interest or lobby groups



*   Different forms of individual networks such as a distinction between acquaintance and interaction networks like in Schleussner et al.


