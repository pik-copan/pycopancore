Optional part 8: Further exercises
----------------------------------

In the role of *model end user*:

- In the study script, introduce another parameter ``initial_high_fraction`` 
  that regulates the fraction of individuals who have a high effort initially.
- Set a fixed ``numpy.random.seed`` so that repeated runs
  give the exact same result.
- Use a python package of your taste to save some results from ``traj`` to 
  disk, and write a script that reads them and does some further plots.
- Perform a Monte-Carlo simulation in which the model is run with a hundred 
  different seeds, and plot the average trajectory of the stock surrounded by a
  band showing the variation of that trajectory over different runs.
- Perform a bifurcation analysis in which this Monte-Carlo simulation is done
  for twenty-one different values of ``initial_high_fraction`` from zero to 
  one, and plot the average and standard deviation of the final fish stock 
  (i.e. the one at time 100, where the average and standard deviation are 
  w.r.t. the 100 runs in the same Monte-Carlo simulation) vs. the value of 
  ``initial_high_fraction``.
- Vary the number of individuals per cell by reducing the number of cells, 
  keeping the total number of individuals at 100 and the total fish capacity
  of all cells together at 100. Plot some example runs, then do a Monte-Carlo
  simulation, and finally a bifurcation analysis in which you vary the number
  of cells (instead of the value of ``initial_high_fraction``).
- Make the cells heterogeneous by giving them different capacities and numbers 
  of indidivuals.

In the role of *model composer*:

- Make another model in which you simply leave out the learning component,
  and test it with a copy of the existing study script.
  
In the role of *model component developer*:

- Change ``my_exploit_growth`` so that the basic growth rate is
  an attribute of ``Cell`` rather than ``Environment``.
  
- ... (TODO!)
