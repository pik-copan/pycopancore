#!/bin/bash
#SBATCH --qos=medium
#SBATCH --job-name=full_norm_coarse_sweep
#SBATCH --account=copan
#SBATCH --ntasks=32
#SBATCH --exclusive
#SBATCH --output=full_norm_coarse_sweep-%j.out
#SBATCH --error=full_norm_coarse_sweep-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/pycopancore/studies

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python run_parallel_maxploit_mofa.py
