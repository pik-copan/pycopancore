#!/bin/bash
#SBATCH --qos=priority
#SBATCH --job-name=plot-full_model_thresholds_0
#SBATCH --account=copan
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --output=plot-full_model_thresholds_0-%j.out
#SBATCH --error=plot-full_model_thresholds_0-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/plots/
#SBATCH --time=02:00:00

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..
cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python pycopancore/studies/pt/plot_maxploit_mofa_cluster.py
