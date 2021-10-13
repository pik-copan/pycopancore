Process-types
=============

Independently of a classification of processes as belonging to certain process taxa,
processes are also distinguished by how they are represented formally in a model.

In copan\:CORE, each process has a "mathematical" *process type*,
such as "ordinary differential equation", "implicit equation", "event", ...

Note that because of this requirement to have exactly one of these types,
some complex real-world processes (e.g., "off-equilibrium economic production")
whose description in a model involves more than one of these types
needs to be split up into smaller processes 
(e.g., an "reallocation of factors" process of type "ODE"
and a "usage of factors" process of type "explicit equation").

The process types may be classified into two groups,
those which influence a variable continuously over time
(such as "ODE", "explicit" and "implicit equation")
and those which do so only at discrete time points
("event" and "step").

While each variable may be influenced by several processes,
there are certain restrictions as to which process type combinations may
influence the same variable.
The main restriction is that a variable that is governed 
by a process of type "explicit equation" cannot by influenced by any other process,
but may occur in processes of type "implicit equation".
In contrast, it is possible that a variable whose continuous evolution
is governed by an "ODE" may also occur in an "implicit equation" 
and may also be changed at discrete time points by an "event" or "step")

Currently, we provide the following process types:

.. toctree::
   :maxdepth: 2

   ODE
   explicit
   implicit
   event
   step
   
Stochastic differential equations are not currently supported but may be
approximated by processes of type "step" with a small time step.
