# Plot figure 5
Run the following code:
```
python run_esd_example.py -p 0.25
python run_esd_example.py -p 0.4 -s 10 -u 4 --with-social
python plot_figure5.py
```

# Plot figure 6
As of now this only works properly on the High Performance Cluster at the
Potsdam Institute for Climate Impact Research.

Follow these steps to reproduce the figure:
1. Create a temporary output directory for the results of the model
   simulations. On PIK's high performace cluster this should be somewhere under
   `/p/tmp/YOURUSERNAME/`.

2. Set the correct path to your desired output directory in line 9 of
   `submit_jobarray.sh`. 

3. Make sure the `pycopancore` repository is located in your home folder such
   that `$HOME/pycopancore/studies/esd_description_paper_example/` is a
   valid path. If `pycopancore` is located elsewhere make sure to set the
   correct paths in `submit_single_runs.py` and `submit_jobarray.sh`.

4. Use `sbatch submit_jobarray.sh` to submit the simulations to the cluster.

# Information on the files in this directory

## collect_results.py
Extract the results the we aim to plot in the bifurcation analysis from the
temporary output folder on the cluster. This script must be run on the cluster. 
Produces a pickle named
collected_results_from_ensemble_simulation_varying_learning_rates.p 

## plot_figure6.py
Plot bifurcation analysis. Needs
collected_results_from_ensemble_simulation_varying_learning_rates.p as input.

## run_example2_varying_learning_rate.py
Run one simulation for a specified learning rate. As this script is intended to
run on the cluster the script must be called with a task id (that corresponds
to the id of the job array entry) which is then translated into a corresponding
learning rate. Secondly a seed must be specified as input argument. This script
produces large output, so it should only be used on the cluster. Use
collect_results.py after running this script to get data of manageable size.

## submit_jobarray.sh
Submit the simulation to the cluster. Adjust as needed.

## submit_single_runs.py
Helper scripts that calls run_example2_varying_learning_rate.py 50 times in a
row for the same task id, i.e., learning rate, and different seeds. This is
needed to circumvent the limit of a maximum of 3600 single jobs per job array
and the fact that a model can only be instantiated once when using pycopancore.


