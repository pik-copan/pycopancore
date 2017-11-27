Process-type "Ordinary Differential Equation"
=============================================

A process of type *ordinary differential equation (ODE)*
specifies additive terms for the time derivative(s) of one or more variables
which may depend on any number of other variables and on time.

Because of their modular design, in many models the time derivative of a variable
will be a sum of several such terms, contributed by several processes 
that may be part of different model components.
Hence, at each point in time, the actual time derivative of a variable
is the sum of all terms contributed by processes of type "ODE" for this variable,
if there are any.
