Logics for simulation and analysis
==================================

For performing a simulation with a certain model,
one or more ``Runner`` classes are provided.
Upon instantiation, a ``Runner`` object is given a ``Model`` object.
It then provides a ``run`` method which can be invoked to run the model
for a certain model time interval and which returns a data structure 
containing the results of the run.
The latter results consist of time-series of certain requested variables for all entities and process taxa
that can then be used to analyse or plot the results.
