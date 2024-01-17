#!/bin/bash
#SBATCH --qos=medium
#SBATCH --job-name=full_model_timescales_64_4_scarce
#SBATCH --account=copan
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --output=full_model_timescales_64_4_scarce%j.out
#SBATCH --error=full_model_timescales_64_4_scarce%j.err
#SBATCH --workdir=/p/tmp/maxbecht/paper/full_model_timescales_64_4_scarce


echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so

srun -n $SLURM_NTASKS --mpi=pmi2 python run_parallel_maxploit_mofa.py
