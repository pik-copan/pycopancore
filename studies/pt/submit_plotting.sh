#!/bin/bash
#SBATCH --qos=priority
#SBATCH --job-name=plot-full_model_new_timescales_64_4
#SBATCH --account=copan
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --workdir=/p/tmp/maxbecht/plots/full_model_new_timescales_64_4
#SBATCH --time=08:00:00

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..
cd ..
cd ..
cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python projects/copan/users/maxbecht/pycopancore/studies/pt/plot_maxploit_mofa_cluster.py
