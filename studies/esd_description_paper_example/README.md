# Introduction
Due to some issues with setting the seed for generating random numbers in the
current implementation of `pycopancore` the following scripts *qualitatively*
reproduce the results show in Figure 5 and Figure 6 of the description paper
currently available at https://arxiv.org/abs/1909.13697

# Plot figure 5
Run the following code:
```
python run_esd_example.py -p 0.25 -s 0
python run_esd_example.py -p 0.4 -s 0 -u 12 --with-social
python plot_figure5.py
```

# Plot figure 6
As of now this only works properly on the High Performance Cluster at the
Potsdam Institute for Climate Impact Research.

Follow these steps to reproduce the figure:
1. Create a temporary output directory for the results of the model
   simulations. On PIK's high performace cluster this should be somewhere under
   `/p/tmp/YOURUSERNAME/`. We call this directory `OUTPUTPATH` from here on.

2. Set the correct path `OUTPUTPATH` in line 9 of
   `submit_jobarray.sh`. 

3. Make sure the `pycopancore` repository is located in your home folder such
   that `$HOME/pycopancore/studies/esd_description_paper_example/` is a
   valid path. If `pycopancore` is located elsewhere make sure to set the
   correct paths in `submit_single_runs.py` and `submit_jobarray.sh`.

4. Use `sbatch submit_jobarray.sh` to submit the simulations to the cluster.

5. Use `collect_results.py -t OUTPUTPATH` to collect the simulation data and
   store them in a single file called `results_ensemble.p` for later
   processing.

6. Use `plot_figure6.py` to plot the results of the bifurcation analysis. The
   scripts loads `results_ensemble.p` and the simulation data without social
   processes that was created using `python run_esd_example.py -p 0.25 -s 0`
   above.

# Some further information on the files in this directory

## run_esd_example.py
Runs one simulation for a specified learning rate. As this script is intended
to run on a cluster it must be called with a `task-id` (that corresponds to the
id of the job array entry) which is then translated into a corresponding
learning rate. Secondly a seed must be specified as input argument. This script
produces large output, so it should only be used on a cluster with large
storage capacity. Use `collect_results.py` after running this script to get
data of manageable size.

## submit_jobarray.sh
Submit the simulation to the cluster. Adjust as needed.

## submit_single_runs.py
Helper scripts that calls `run_esd_example.py` 50 times in a row for the same
task id, i.e., learning rate, and different seeds. This is needed to circumvent
the limit of a maximum of 3600 single jobs per job array on PIKs high
performance cluster and the fact that a model can only be instantiated once
when using `pycopancore`.
