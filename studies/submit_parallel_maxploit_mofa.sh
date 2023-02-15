#!/bin/bash
#SBATCH --qos=medium
#SBATCH --job-name=group_timescale1
#SBATCH --account=copan
#SBATCH --ntasks=32
#SBATCH --exclusive
#SBATCH --output=group_timescale1-%j.out
#SBATCH --error=group_timescale1-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/pycopancore/studies

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python run_parallel_maxploit_mofa.py
