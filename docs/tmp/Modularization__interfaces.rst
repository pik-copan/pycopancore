Modularization, interfaces
==========================

In order to be able to taylor specific model variants to specific research questions (see below), including the first major questions of

#.  reproducing the ongoing
    great acceleration
    and



#.  identifying scenarios for a future great transformation,



#.  analyzing resilience of development pathways (as those provided by IAMs, aka optimizing on the edge)



and to study the
*structural stability*
of the model by replacing individual variants of subcomponents by other variants of the same subcomponent, a thoroughly designed modularization needs to be followed from the start, both in

#.  abstract model design and



#.  concrete software implementation.




A suitable modularization has probably more than just one level, but the levels should be compatible, preferably forming a hierarchy of components and subcomponents, each of which might represent

*   an individual
    *structural/causal equation*
    that
    *calculates*
    one specific
    *output variable*
    or its first or second time derivative (left-hand side) on the basis of zero or more specific
    *input variables *
    (occurring on the right hand side), some of which might be optional,



*   an individual
    *algebraic/implicit equation*
    that states a certain
    *relationship*
    between a set of variables or their derivatives, which could hence be named the
    *interacting variables *
    of this component (e.g. the equation stating that the wages in the energy and final sectors must be equal),



*   a
    *set*
    of such equations belonging together
    *thematically*
    (e.g. a set of ODEs representing the carbon cycle, or a set of algebraic equations representing the general equilibrium allocation of resources to production processes)



*   *what else?*




Particular care needs to be taken with components representing stochastic, discontinuous processes. E.g., the network adaptation
*might*
be represented by

#.  an “adaptation timing component” that selects the next time point at which adaptation occurs in one of several ways (output variable: yes/no whether the current time point is this time point)



#.  a “rewired link selection component” that selects the link to be rewired in one of several ways



#.  and a “rewiring component” that selects a pair of nodes to be newly connected in one of several ways



#.  or: just one component doing all of these three things.




As some processes, especially those acting on stocks, often have
*additive*
effects, the default behaviour of the model should be that if a variable occurs as output in more than one component, their output is added, as long as the component does not explicitly state that this is not considered making sense.


The
*interface*
of a component thus consists at least in naming the

*   input variables (mandatory and optional)



*   output variables and corresponding orders of time derivatives, with flags whether output may be added to other components output to the same variables



*   interacting variables and corresponding orders of time derivatives




In order for components to be linked, it is of utmost importance that a consistent set of (potential) interface variables is used, which should be designed in parallel to the components’ interfaces. For many variables, different
*levels of aggregation*
might be needed in different components, so a list like this may be helpful, indicating stocks and flows explicitly in the name:


+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **variable name (aggregation level)** | **physical**    | **description**                                                                                                                                                                                                                |
|                                       | **dimension**   |                                                                                                                                                                                                                                |
|                                       |                 |                                                                                                                                                                                                                                |
+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| population stock (cell)               | humans          | a cell’s total human population                                                                                                                                                                                                |
|                                       |                 |                                                                                                                                                                                                                                |
+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| population stock (cell, age group)    | humans          | a cell’s population of a certain age group                                                                                                                                                                                     |
|                                       |                 |                                                                                                                                                                                                                                |
+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| labour                                | time per time   | a cell’s total available labour hours per time (will be related to population, possibly by aggregating population over age groups)                                                                                             |
| stock                                 |                 |                                                                                                                                                                                                                                |
| (cell)                                |                 |                                                                                                                                                                                                                                |
|                                       |                 |                                                                                                                                                                                                                                |
+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| energy inflow (cell)                  | energy per time | ...                                                                                                                                                                                                                            |
|                                       |                 |                                                                                                                                                                                                                                |
+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| physical capital value (cell)         | monetary        | value                                                                                                                                                                                                                          |
|                                       |                 | of all machines, tools, etc. used for economic production in a cell as an exclusive good (i.e., the unit that is used in one production process/facility cannot be used simultaneously in another production process/facility) |
|                                       |                 |                                                                                                                                                                                                                                |
+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| public infrastructure value (cell)    | monetary        | value of all infrastructure (mostly networked such as transportation & communication) used as a nonexclusive public                                                                                                            |
|                                       |                 | good                                                                                                                                                                                                                           |
|                                       |                 |                                                                                                                                                                                                                                |
+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| financial capital (cell)              | monetary        |                                                                                                                                                                                                                                |
|                                       |                 |                                                                                                                                                                                                                                |
+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| managed material stock mass (cell)    | mass            | total mass of physical capital, public infrastructure, and other materials managed by society in the cell. the ratio                                                                                                           |
|                                       |                 | * (physical capital value + public infrastructure value) / managed material stock mass*                                                                                                                                        |
|                                       |                 | may be considered a material efficiency indicator                                                                                                                                                                              |
|                                       |                 |                                                                                                                                                                                                                                |
+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ...                                   |                 |                                                                                                                                                                                                                                |
|                                       |                 |                                                                                                                                                                                                                                |
+---------------------------------------+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


Aggregation needs to happen on a consistent hierarchy (which should probably match established classifications from relevant disciplines, e.g. age groups used in official statistics, geographic regions used in geosciences), so another list like this may be helpful:


+-----------------------+--------------------------------------------------------------------------------+
| **aggregation level** | **description**                                                                |
|                       |                                                                                |
+-----------------------+--------------------------------------------------------------------------------+
| cell                  | smallest geographic unit, e.g. defined by a lon/lat grid                       |
|                       |                                                                                |
+-----------------------+--------------------------------------------------------------------------------+
| age group             | interval of possible ages of a human, e.g. [0a,18a], [18a,65a], [65a,infinity] |
|                       |                                                                                |
+-----------------------+--------------------------------------------------------------------------------+
| age in yrs            | one-year intervals of possible ages of a human: [0a,1a], [1a,2a], ...          |
|                       |                                                                                |
+-----------------------+--------------------------------------------------------------------------------+
| ...                   |                                                                                |
|                       |                                                                                |
+-----------------------+--------------------------------------------------------------------------------+


In order to bridge different aggregation levels if some component outputs a different aggregation level than another needs as input, there may be specific “
*resolution components*
” whose sole job is to aggregate, disaggregate (using some heuristics?) or interpolate between aggregation levels.
