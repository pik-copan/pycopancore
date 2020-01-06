Process-type "Implicit Equation"
================================

A process of type *implicit equation*
specifies an equation that related several variables in some way
and thus makes sure their values respect a certain condition
(e.g. an budget equation like "supply equals demand" or an equilibrium equation
like "wage in sector A equals wage in sector B")
without determining which variables influence which others.

Depending on which other equations are contained in the final model,
an implicit equation may influence some of the occurring variables but not others.
E.g., an implicit equation of the form "supply equals demand" 
can either influence supply (if demand is set by some other process, e.g., by an explicit equation),
or can influence demand (if supply is governed by some other process, e.g., by an ODE).

Implicit equations frequently occur in economic equilibrium model components 
but may also occur in environmental model components that treat a certain equilibrating process as infinitely fast,
e.g., "surface air temperature equals surface ocean temperature".
