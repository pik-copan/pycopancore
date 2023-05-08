#!/bin/bash
#SBATCH --qos=short
#SBATCH --job-name=full_norm_2groups
#SBATCH --account=copan
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --output=full_norm_2groups-%j.out
#SBATCH --error=full_norm_2groups-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/results/maxploit2/full_norm_2groups

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..
cd ..
cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python pycopancore/studies/run_parallel_maxploit_mofa.py
