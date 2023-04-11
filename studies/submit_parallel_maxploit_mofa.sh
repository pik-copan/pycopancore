#!/bin/bash
#SBATCH --qos=medium
#SBATCH --job-name=injunctive_threshold5
#SBATCH --account=copan
#SBATCH --ntasks=16
#SBATCH --exclusive
#SBATCH --output=injunctive_threshold5-%j.out
#SBATCH --error=injunctive_threshold5-%j.err
#SBATCH --workdir=/p/projects/copan/users/maxbecht/results/maxploit2/injunctive_threshold

echo "------------------------------------------------------------"
echo "SLURM JOB ID: $SLURM_JOBID"
echo "$SLURM_NTASKS tasks"
echo "------------------------------------------------------------"

cd ..
cd ..
cd ..

export I_MPI_PMI_LIBRARY=/p/system/slurm/lib/libpmi.so
srun -n $SLURM_NTASKS --mpi=pmi2 python pycopancore/studies/run_parallel_maxploit_mofa.py
