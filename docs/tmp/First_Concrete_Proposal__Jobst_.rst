First Concrete Proposal (Jobst)
===============================

**Entities:**
There are individuals,
*i*
, geographically located grid cells,
*c*
, and societies,
*s*
.


At each point in time,
*t*
, In each grid
**cell**

*c*
, there is a geological (fossil) carbon stock
*G(c,t)*
and a terrestrial (plants and soil, “land”) carbon stock
*L(c,t)*
.


**Globally**
, there is an atmospheric carbon stock
*A(t)*
, a maritime carbon stock
*M(t)*
, and a renewable energy production knowledge stock
*S(t)*
. The sum of all carbon stocks is a constant,
*C*
*.


Each
**society**

*s*
has a territory
*T(s,t)*
, initially a single grid cell, and the territories are nonoverlapping.


**Metabolism: **
In each society
*s*
, there is a human population
*P(s,t)*
and a physical capital stock
*K(s,t) *
representing all long-living goods, machines, buildings, and other infrastructure. Using
*P*
(as labour) and
*K*
, society
*s*
harvests and extracts amounts
*B(s,t)*
and
*F(s,t)*
of biomass (biofuel and food) and fossil fuel per time from
*L*
and
*G*
, and produces an amount of
renewable energy

*R(s,t)*
per time. They use
*P, K, B, F,*
and
*R*
to produce an amount of
final goods

*Y(s,t)*
, measured on some common scale. Part of
*Y*
is consumed, leading to population growth, the rest is invested into physical capital.
Renewable production
*R*
leads to growth of knowledge
*S*
via learning by doing
. We need mathematical expressions for the following functions to govern this process:

*   *B = fB(P,K,L;*
    *G*
    *,S)*
    ; non-negative; monotonic and concave in
    *P,K,L*
    ; zero if one of them is zero; antitonic in
    *G,S*
    .



*   *F = fF(P,K,G;L,S)*
    ; non-negative; monotonic and concave in
    *P,K,G*
    ; zero if one of them is zero; antitonic in
    *L,S*
    .



*   *R = fR(P,K,S;G,L)*
    ; non-negative; monotonic and concave in
    *P,K,S*
    ; zero if one of them is zero; antitonic in
    *G,L*
    .



*   *Y = fY(P,K,B,F,R)*
    ; non-negative; monotonic and concave in all arguments; zero if
    *P*
    or
    *K*
    or
    *B+F+R*
    is zero. For simplicity, I suggest that the three energy forms
    *B,F,R*
    are perfect substitutes, so that
    *Y = fY(P,K,E)*
    where
    *E = eB B + eF F + R*
    is total energy flow and eB and eF are combustion efficiencies.



*   *dP/dt*
    =
    *fP(P,K,Y,T)*
    ; monotonic and concave in
    *K*
    and
    *Y*
    ; zero if
    *P*
    is zero. The dependency on
    *K*
    is suggested since the amount of built infrastructure (which is part of
    *K*
    ) probably influences the carrying capacity (e.g. via housing space); dependency on
    *T*
    may represent climate
    damages
    .



*   *dK/dt*
    =
    *fK(K,Y,T)*
    ; monotonic in
    *Y*
    ; dependency on
    *T*
    may represent climate damages.



*   *dS/dt*
    =
    *fS(S,R)*
    ; monotonic in
    *R*
    .



The copan:GLOBAL model contains relatively simple examples for all of the above functions
*fB,fF,fR,fY,fP,fK,fS*
satisfying the above requirements, so those can be used as a starting point.


**Policy (open question):**
How to incorporate opinions
*O(i)*
(see below) into these functions? The simplest way might be that for each energy form, there is a binary opinion entry encoding whether that energy form is considered acceptable, and society will consider an energy form iff a majority of its population accepts it. Another possibility would be to have a societal policy vector
*O(s)*
that changes stochastically in dependence of
*O(i)*
, e.g. switching to the majority
*O(i)*
with a probability depending on the size of the majority.


**Carbon cycle, climate, vegetation: **

*   All extracted carbon
    *B + F*
    is immediately combusted and emitted into
    *A*
    which in turn is coupled to
    *M*
    via diffusion and to
    *T*
    via the greenhouse effect, as in the Anderies and GLOBAL models.



*   Societal harvests
    *B(s)*
    and extractions
    *F(s)*
    are proportionally downscaled from society to cells, giving cell harvests
    *B(c) = B(s) L(c) / L(s)*
    and extractions
    *F(c) = F(s) G(c) / G(s)*
    .



*   Global temperature
    *T*
    is downscaled to cell temperature
    *T(c)*
    according to some fixed formula depending on cell position (e.g. simply on latitude).



*   *L(c)*
    grows according to Anderies-like equations depending on cell surface temperature
    *T(c)*
    and some other cell-dependent parameters, with a harvesting term
    *B(c)*
    , e.g. as in the GLOBAL model. Later this might be replaced by LPJ or an emulator thereof.



*   *G*
    declines according to
    *F*
    :
    *dG(c,t)/dt = – F(c,t)*




**Social dynamics:**

*   Each individual
    *i*
    lives in a cell
    *c(i,t)*
    and has a vector of opinions
    (also preferences, values, ...)

    *O(i)*
    and network neighbours
    *N(i,t)*
    . When i is born, these are drawn according to some probabilities depending on its parent's neighbours and spatial distance.



*   At each
    *t*
    , each
    *i*
    has a probability rate of “acting”, leading to a Poisson process of actions. When acting,
    *i*
    will either perform a network adaptation step, a society adaptation step, or a learning
    by
    imitation

    step
    , according to some fixed probabilities.



*   In a network adaptation step,
    *i*
    may rewire a link using as criteria opinions and the membership in societies. Since the network is spatial, the selection of new neighbours should also depend on spatial and/or network
    distance
    .



*   In a learning by imitation step,
    *i*
    draws a neighbour
    * j*
    at random and switches to
    *j*
    's opinion vector
    *O(j)*
    with a probability depending on current per-capita consumption via a common sigmoid function.




In a
**society adaptation**

step
(“coalition” formation)
,
*i*
considers either

*   convincing her cell to separate from their society, forming a new small society, or



*   merging her society with the society of some neighbour
    *j *
    of
    *i*
    , or



*   moving her cell to the society of
    *j*
    ,



always respecting that societies need to be geographically connected. For each such possible “move”,
*i*
forms expectations of welfare gains, and then performs the move that is most profitable for her
among all moves that are profitable for all people who need to agree
(i.e. for the individuals in the separating cell or in the two merging societies).


**Open question:**
How to calculate these expected gains? The simplest way would be an application of the above-sketched metabolic equations to the hypothetical new society structure and assessing the resulting per-capita consumption
*Y/P*
. This may however assume too much cognitive abilities!


**Open question:**
Since the spatial network of representative individuals
*i*
represents the whole population, the birth and death of individuals must be linked to society's population dynamics
*dP(s)/dt*
. One possibility is to have a fixed ratio between representative individuals and population, each
*i*
representing
*n*
members of the population; whenever the integer part of
*P(s)/n*
changes, one randomly drawn
*i*
dies or one is born at a random place inside the territory.


**Open question:**

When a society splits or a cell moves from one society to another, how is its capital split?
The simplest assumption is that this is in proportion to population, i.e., each member of society owns the same amount of capital.

Remarks
~~~~~~~

*   I suggest to use functions
    *fB,fF,fR,fY*
    which display increasing returns to scale, i.e., which grow by more than a factor of two if all inputs are doubled; this would give an incentive to merge small societies into larger ones and would lead to super-exponential growth in phases where resources are not yet substantially constrained
    (explaining the great acceleration).



*   Metabolic or infrastructural “complexity” is represented only in the variable
    *K*
    here, not via any explicitly modeled networks



*   Societal “complexity” is represented in the social network and the increasingly heterogeneous partition of cells into societies.



*   There is no water cycle.



*   There is no optimization assumption except in the society adaptation step.



*   There are no connections between different societies



*   There is no trade between societies
    , thus there is no possibility to use resources from other societies’ territories.


