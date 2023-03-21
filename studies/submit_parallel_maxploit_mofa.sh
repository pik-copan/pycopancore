#!/bin/bash
#SBATCH --qos=short
#SBATCH --job-name=descriptive_threshold_final
#SBATCH --account=copan
#SBATCH --ntasks=32
#SBATCH --exclusive
#SBATCH --output=descriptive_threshold_final-%j.out
#SBATCH --error=descriptive_threshold_final-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/results/maxploit/descriptive_threshold_final

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python p/projects/copan/users/maxbechts/pycopancore/studies/run_parallel_maxploit_mofa.py
